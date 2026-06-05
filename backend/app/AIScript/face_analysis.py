import base64
import logging
import os

import cv2
import numpy as np
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.models import load_model


logging.getLogger("tensorflow").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASCADE_PATH = os.path.join(BASE_DIR, "AIScript", "haarcascade_frontalface.xml")
MODEL_PATH = os.path.join(BASE_DIR, "AIScript", "face_analysis_model.keras")

IMG_SIZE = 224
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
_model = None


def _clamp(value, min_val=0.0, max_val=100.0):
    return float(max(min_val, min(max_val, value)))


def _score(value):
    return int(round(_clamp(value)))


def get_model():
    """Lazy-load the age model so the backend can import before training exists."""
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Age model not found at {MODEL_PATH}. Run train_age_model.py first."
            )
        _model = load_model(MODEL_PATH, compile=False)
    return _model


def decode_b64_image(b64_string):
    """Decode a base64 string or bytes object into an OpenCV BGR image."""
    try:
        img_data = base64.b64decode(b64_string)
        np_arr = np.frombuffer(img_data, np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception as exc:
        logger.exception("Error decoding base64 image: %s", exc)
        return None


def detect_face(image):
    """Detect faces and return the largest cropped face."""
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


def preprocess_image(image):
    """Preprocess an OpenCV BGR face crop for the age model."""
    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = preprocess_input(image.astype("float32"))
    return np.expand_dims(image, axis=0)


def _face_skin_roi(face):
    """Use the central face area to reduce hair/background edge noise."""
    h, w = face.shape[:2]
    y1, y2 = int(h * 0.18), int(h * 0.88)
    x1, x2 = int(w * 0.14), int(w * 0.86)
    roi = face[y1:y2, x1:x2]
    return roi if roi.size else face


def estimate_skin_metrics(face):
    """
    Estimate non-labeled skin metrics directly from the image.

    UTKFace does not contain hydration, fine-line, or texture labels. These
    values are therefore transparent image-quality/skin-surface proxies, not
    neural predictions or medical measurements.
    """
    roi = cv2.resize(_face_skin_roi(face), (IMG_SIZE, IMG_SIZE))
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray_blur, 45, 135)
    edge_density = np.mean(edges > 0)

    laplacian_var = cv2.Laplacian(gray_blur, cv2.CV_64F).var()
    local_contrast = float(np.std(gray_blur))
    brightness = float(np.mean(hsv[:, :, 2]))

    fine_lines = _score((edge_density / 0.12) * 100.0)

    texture_from_laplacian = np.log1p(laplacian_var) / np.log1p(900.0)
    texture_from_contrast = local_contrast / 55.0
    texture = _score(
        (0.7 * _clamp(texture_from_laplacian, 0.0, 1.0)
         + 0.3 * _clamp(texture_from_contrast, 0.0, 1.0))
        * 100.0
    )

    smoothness = 100.0 - fine_lines
    low_contrast_score = 100.0 - _score((local_contrast / 65.0) * 100.0)
    brightness_score = 100.0 - _score((abs(brightness - 170.0) / 170.0) * 100.0)
    hydration = _score(
        0.55 * smoothness
        + 0.25 * low_contrast_score
        + 0.20 * brightness_score
    )

    return {
        "hydration": hydration,
        "fine_lines": fine_lines,
        "texture": texture,
    }


def predict_age(face):
    model = get_model()
    input_image = preprocess_image(face)
    prediction = model.predict(input_image, verbose=0)
    age_normalized = float(np.ravel(prediction)[0])
    return int(np.clip(round(age_normalized * 100.0), 1, 100))


def analyze_face(b64_string):
    """Detect a face, predict age, and estimate proxy skin metrics."""
    image = decode_b64_image(b64_string)
    if image is None:
        return {"error": "Invalid image file"}

    face = detect_face(image)
    if face is None:
        return {"error": "No face detected"}

    try:
        age_years = predict_age(face)
    except FileNotFoundError as exc:
        return {"error": str(exc)}

    metrics = estimate_skin_metrics(face)
    logger.info(
        "[ANALYZE] age=%s hydration=%s fine_lines=%s texture=%s",
        age_years,
        metrics["hydration"],
        metrics["fine_lines"],
        metrics["texture"],
    )

    return {
        "age": age_years,
        **metrics,
    }
