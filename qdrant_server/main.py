from flask import Flask, request, jsonify
from qdrant_client_wrapper import setup_collection, save_embedding, search_embedding, get_all_embeddings
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

setup_collection()


@app.route("/add", methods=["POST"])
def add():
    data = request.json
    name = data.get("name")
    embedding = data.get("embedding")

    if not name or not embedding:
        return jsonify({"error": "Missing 'name' or 'embedding'"}), 400

    save_embedding(name, embedding)
    return jsonify({"status": "ok", "message": f"Embedding for '{name}' saved."})


@app.route("/search", methods=["POST"])
def search():
    data = request.json
    embedding = data.get("embedding")

    if not embedding:
        return jsonify({"error": "Missing 'embedding'"}), 400

    results = search_embedding(embedding, top_k=1)
    if not results:
        return jsonify({"result": None})

    top = results[0]
    return jsonify({
        "match_name": top.payload.get("name"),
        "score": top.score
    })


@app.route("/all", methods=["GET"])
def get_all():
    points = get_all_embeddings()
    return jsonify(points)


if __name__ == "__main__":
    app.run(debug=True)
