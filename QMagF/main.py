import numpy as np
import shutil
from flask_cors import CORS

np.bool = np.bool_
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from preprocessing.embed import main_embed, search_from_image
from flask import send_from_directory
import re

UPLOAD_FOLDER = 'inputImage'
ALIGNED_FOLDER = 'alignedImage'
STATIC_FOLDER = 'static'
SEARCH_FOLDER = 'uploads'

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)
os.makedirs(SEARCH_FOLDER, exist_ok=True)


def custom_secure_filename(filename):
    filename = re.sub(r'[^\w\s.-]', '', filename, flags=re.UNICODE)
    filename = filename.strip()
    return filename


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(SEARCH_FOLDER, filename)


@app.route('/static/<filename>')
def static_file(filename):
    return send_from_directory(STATIC_FOLDER, filename)


@app.route('/all-images', methods=['GET'])
def get_all_images():
    try:
        files = os.listdir(STATIC_FOLDER)
        images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        return jsonify({'images': images})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def save_image(file, subfolder):
    filename = secure_filename(file.filename)
    file_path = os.path.join(subfolder, filename)
    file.save(file_path)
    return file_path, filename


@app.route('/add-image', methods=['POST'])
def add_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    filename = custom_secure_filename(file.filename)

    file_bytes = file.read()

    for folder in [UPLOAD_FOLDER, STATIC_FOLDER]:
        path = os.path.join(folder, filename)
        with open(path, 'wb') as f:
            f.write(file_bytes)

    main_embed(source_dir=UPLOAD_FOLDER, result_dir=ALIGNED_FOLDER)

    return jsonify({'message': 'Изображение добавлено в базу'})


@app.route('/search-image', methods=['POST'])
def search_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']

    input_path, filename = save_image(file, UPLOAD_FOLDER)

    shutil.copy(input_path, os.path.join(SEARCH_FOLDER, filename))

    results = search_from_image(source_dir=UPLOAD_FOLDER, result_dir=ALIGNED_FOLDER, return_result=True)

    if not results:
        return jsonify({'message': 'Лица не распознаны'})

    recognized = []
    for r in results:
        if r.get('match_name') and r.get('score', 0) > 0.5:
            recognized.append({
                'file': os.path.basename(r['path']),
                'name': r['match_name'],
                'score': round(r['score'], 2)
            })

    if recognized:
        return jsonify({'recognized': recognized})
    else:
        return jsonify({'message': 'Лица не распознаны'})


if __name__ == "__main__":
    app.run(port=5001, debug=False)
