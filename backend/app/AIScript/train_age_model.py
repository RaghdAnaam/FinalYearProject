import os
import random

import certifi
import cv2
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import Sequence
from tqdm import tqdm


# Help urllib/Keras verify HTTPS downloads on macOS/Homebrew Python.
os.environ.setdefault("SSL_CERT_FILE", certifi.where())
os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())

# === CONFIGURATION ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 12
SEED = 42
DATASET_PATH = "/Users/raghdanaam/Downloads/archive/UTKFace"
MODEL_SAVE_PATH = os.path.join(SCRIPT_DIR, "face_analysis_model.keras")
CASCADE_PATH = os.path.join(SCRIPT_DIR, "haarcascade_frontalface.xml")


random.seed(SEED)
np.random.seed(SEED)
tf.keras.utils.set_random_seed(SEED)

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)


def parse_age_from_filename(filename):
    """UTKFace filenames start with age, e.g. 26_1_0_....jpg."""
    try:
        age = int(filename.split("_")[0])
    except (TypeError, ValueError, IndexError):
        return None

    if 1 <= age <= 100:
        return age
    return None


def detect_face(image):
    """Return the largest detected face crop, or None if Haar cannot find one."""
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
    """Resize, convert OpenCV BGR to RGB, then apply EfficientNet preprocessing."""
    face = cv2.resize(face, (IMG_SIZE, IMG_SIZE))
    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    face = preprocess_input(face.astype("float32"))
    return face


def get_age_bucket(age):
    """Use decade buckets so rare ages get more weight during training."""
    return min(age // 10, 9)


def compute_sample_weights(ages):
    """Inverse-frequency sample weights normalized around 1.0."""
    buckets = np.array([get_age_bucket(age) for age in ages])
    unique, counts = np.unique(buckets, return_counts=True)
    count_by_bucket = dict(zip(unique, counts))
    num_buckets = len(unique)
    total = len(ages)

    weights = np.array(
        [
            total / (num_buckets * count_by_bucket[get_age_bucket(age)])
            for age in ages
        ],
        dtype="float32",
    )
    return weights / np.mean(weights)


def collect_utkface_records(dataset_path):
    records = []
    files = sorted(os.listdir(dataset_path))

    for filename in tqdm(files, desc="Indexing UTKFace files"):
        age = parse_age_from_filename(filename)
        if age is None:
            continue

        img_path = os.path.join(dataset_path, filename)
        if os.path.isfile(img_path):
            records.append((img_path, age))

    if not records:
        raise RuntimeError(f"No usable UTKFace files found in {dataset_path}")

    return records


def augment_image(image):
    if random.random() < 0.5:
        image = cv2.flip(image, 1)

    brightness = random.uniform(0.85, 1.15)
    image = np.clip(image.astype("float32") * brightness, 0, 255).astype("uint8")

    angle = random.uniform(-12.0, 12.0)
    h, w = image.shape[:2]
    matrix = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    image = cv2.warpAffine(
        image,
        matrix,
        (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT_101,
    )

    return image


class UTKFaceAgeSequence(Sequence):
    def __init__(
        self,
        records,
        batch_size=BATCH_SIZE,
        sample_weights=None,
        augment=False,
        shuffle=True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.records = list(records)
        self.batch_size = batch_size
        self.sample_weights = sample_weights
        self.augment = augment
        self.shuffle = shuffle
        self.indices = np.arange(len(self.records))
        self.on_epoch_end()

    def __len__(self):
        return int(np.ceil(len(self.records) / self.batch_size))

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __getitem__(self, batch_index):
        start = batch_index * self.batch_size
        end = min(start + self.batch_size, len(self.records))
        batch_indices = self.indices[start:end]

        images, ages, weights = [], [], []
        for record_index in batch_indices:
            img_path, age = self.records[record_index]
            image = cv2.imread(img_path)
            if image is None:
                continue

            face = detect_face(image)
            if face is None:
                face = image

            if self.augment:
                face = augment_image(face)

            images.append(preprocess_face_for_model(face))
            ages.append(age / 100.0)

            if self.sample_weights is not None:
                weights.append(self.sample_weights[record_index])

        X = np.array(images, dtype="float32")
        y = np.array(ages, dtype="float32").reshape(-1, 1)

        if self.sample_weights is not None:
            return X, y, np.array(weights, dtype="float32")
        return X, y


def build_model(freeze_backbone=True):
    """Build an age-only EfficientNet regression model."""
    base_model = EfficientNetB0(
        weights="imagenet",
        include_top=False,
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
    )
    base_model.trainable = not freeze_backbone

    x = GlobalAveragePooling2D()(base_model.output)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.35)(x)
    x = Dense(64, activation="relu")(x)
    output = Dense(1, activation="sigmoid", name="age")(x)

    model = Model(inputs=base_model.input, outputs=output)
    model.compile(
        optimizer=Adam(learning_rate=1e-4),
        loss=tf.keras.losses.Huber(delta=0.1),
        metrics=["mae"],
    )
    return model, base_model


def main():
    if not os.path.isdir(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

    print("Indexing dataset...")
    records = collect_utkface_records(DATASET_PATH)
    age_buckets = [get_age_bucket(age) for _, age in records]
    try:
        train_records, val_records = train_test_split(
            records,
            test_size=0.2,
            random_state=SEED,
            stratify=age_buckets,
        )
    except ValueError:
        train_records, val_records = train_test_split(
            records,
            test_size=0.2,
            random_state=SEED,
        )
    print(f"Training images: {len(train_records)}")
    print(f"Validation images: {len(val_records)}")

    train_ages = np.array([age for _, age in train_records])
    train_sample_weights = compute_sample_weights(train_ages)

    print("Building a new age-only model...")
    model, base_model = build_model(freeze_backbone=True)

    train_sequence = UTKFaceAgeSequence(
        train_records,
        sample_weights=train_sample_weights,
        augment=True,
        shuffle=True,
    )
    val_sequence = UTKFaceAgeSequence(val_records, augment=False, shuffle=False)

    callbacks = [
        EarlyStopping(
            monitor="val_loss",
            patience=3,
            restore_best_weights=True,
            verbose=1,
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            min_lr=1e-6,
            verbose=1,
        ),
    ]

    print("Phase 1: training age head with frozen EfficientNet backbone...")
    model.fit(
        train_sequence,
        validation_data=val_sequence,
        epochs=EPOCHS,
        callbacks=callbacks,
    )

    print("\nPhase 2: fine-tuning the last 30 EfficientNet layers...")
    base_model.trainable = True
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=Adam(learning_rate=1e-5),
        loss=tf.keras.losses.Huber(delta=0.1),
        metrics=["mae"],
    )

    model.fit(
        train_sequence,
        validation_data=val_sequence,
        epochs=max(3, EPOCHS // 2),
        callbacks=callbacks,
    )

    print(f"Saving final model to {MODEL_SAVE_PATH}")
    model.save(MODEL_SAVE_PATH)
    print("Training complete.")


if __name__ == "__main__":
    main()
