import os

import cv2
import numpy as np
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.models import load_model
from tqdm import tqdm


IMG_SIZE = 224
SEED = 42
MAX_SAMPLES = 1000

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_SAVE_PATH = os.path.join(SCRIPT_DIR, "face_analysis_model.keras")
CASCADE_PATH = os.path.join(SCRIPT_DIR, "haarcascade_frontalface.xml")
DATASET_PATH = "/Users/raghdanaam/Downloads/archive/UTKFace"

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)


def parse_age_from_filename(filename):
    try:
        age = int(filename.split("_")[0])
    except (TypeError, ValueError, IndexError):
        return None

    if 1 <= age <= 100:
        return age
    return None


def detect_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50),
    )

    if len(faces) == 0:
        return None

    x, y, w, h = max(faces, key=lambda rect: rect[2] * rect[3])
    return image[y : y + h, x : x + w]


def preprocess_face_for_model(face):
    face = cv2.resize(face, (IMG_SIZE, IMG_SIZE))
    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    face = preprocess_input(face.astype("float32"))
    return face


def load_test_data(dataset_path):
    images, ages = [], []
    files = sorted(os.listdir(dataset_path))
    rng = np.random.default_rng(SEED)
    rng.shuffle(files)

    for filename in tqdm(files, desc="Loading test images"):
        age = parse_age_from_filename(filename)
        if age is None:
            continue

        image = cv2.imread(os.path.join(dataset_path, filename))
        if image is None:
            continue

        face = detect_face(image)
        if face is None:
            face = image

        images.append(preprocess_face_for_model(face))
        ages.append(age)

        if len(images) >= MAX_SAMPLES:
            break

    if not images:
        raise RuntimeError(f"No usable test images found in {dataset_path}")

    return np.array(images, dtype="float32"), np.array(ages, dtype="float32")


def main():
    if not os.path.exists(MODEL_SAVE_PATH):
        raise FileNotFoundError(f"Model not found: {MODEL_SAVE_PATH}")

    print("Loading model...")
    model = load_model(MODEL_SAVE_PATH, compile=False)

    print("Loading test data...")
    X, true_age = load_test_data(DATASET_PATH)

    print("Running inference...")
    predictions = model.predict(X, batch_size=32, verbose=1)
    predicted_age = np.clip(np.ravel(predictions), 0.0, 1.0) * 100.0

    mae = mean_absolute_error(true_age, predicted_age)
    rmse = root_mean_squared_error(true_age, predicted_age)
    within_5 = np.mean(np.abs(true_age - predicted_age) <= 5.0) * 100.0
    within_10 = np.mean(np.abs(true_age - predicted_age) <= 10.0) * 100.0

    print(f"Samples evaluated: {len(true_age)}")
    print(f"Age MAE: {mae:.2f} years")
    print(f"Age RMSE: {rmse:.2f} years")
    print(f"Within 5 years: {within_5:.2f}%")
    print(f"Within 10 years: {within_10:.2f}%")
    print("First 10 true ages:", true_age[:10].astype(int).tolist())
    print("First 10 predicted ages:", np.round(predicted_age[:10], 1).tolist())


if __name__ == "__main__":
    main()
