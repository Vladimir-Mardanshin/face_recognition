import os
import click
import tqdm
import cv2
from utils.files import list_all_files
from preprocessing.insightface.src.mtcnn_detector import MtcnnDetector
from preprocessing.insightface.src import face_preprocess


def preprocess(det, img):
    detected = det.detect_face(img, det_type=0)
    if detected is None:
        return None

    bbox, points = detected
    if bbox.shape[0] == 0:
        return None

    points = points[0, :].reshape((2, 5)).T
    image = face_preprocess.preprocess(img, bbox, points, image_size="112,112")
    return image


import os
import click
import tqdm
import cv2
from utils.files import list_all_files
from preprocessing.insightface.src.mtcnn_detector import MtcnnDetector
from preprocessing.insightface.src import face_preprocess


def preprocess(det, img):
    detected = det.detect_face(img, det_type=0)
    if detected is None:
        return None

    bbox, points = detected
    if bbox.shape[0] == 0:
        return None

    points = points[0, :].reshape((2, 5)).T
    image = face_preprocess.preprocess(img, bbox, points, image_size="112,112")
    return image


import os
import cv2
import tqdm
from utils.files import list_all_files
from preprocessing.insightface.src.mtcnn_detector import MtcnnDetector
from preprocessing.insightface.src import face_preprocess

def main_align(result_dir, source_dir, model_path='_models/mtcnn-model/'):
    os.makedirs(result_dir, exist_ok=True)

    # Инициализация MTCNN
    det = MtcnnDetector(
        model_folder=model_path,
        accurate_landmark=True,
        minsize=50,
        threshold=[0.6, 0.7, 0.8]
    )

    filenames = list_all_files(source_dir)
    print(f"[INFO] Найдено файлов: {len(filenames)}")

    for filename in tqdm.tqdm(filenames):
        img = cv2.imread(filename)
        if img is None:
            print(f"[WARN] Не удалось загрузить: {filename}")
            continue

        detected = det.detect_face(img)
        if detected is None:
            print(f"[INFO] Лица не найдены: {filename}")
            continue

        bboxes, landmarks = detected
        if bboxes is None or len(bboxes) == 0:
            print(f"[INFO] Лица не найдены: {filename}")
            continue

        base_name = os.path.splitext(os.path.basename(filename))[0]

        for i in range(len(bboxes)):
            bbox = bboxes[i]
            landmark = landmarks[i].reshape((2, 5)).T  # Преобразуем landmark к (5,2)

            try:
                aligned_face = face_preprocess.preprocess(
                    img, bbox, landmark, image_size='112,112'
                )
            except Exception as e:
                print(f"[WARN] Ошибка выравнивания: {e}")
                continue

            out_name = f"{base_name}_face{i}.jpg"
            out_path = os.path.join(result_dir, out_name)
            cv2.imwrite(out_path, aligned_face)
            print(f"[✓] Сохранено выровненное лицо: {out_path}")
