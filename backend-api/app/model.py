"""
Chargement et inférence du modèle Keras (EfficientNetB0, .h5).

Le modèle est chargé une seule fois via `load_model()`, appelé au démarrage
du serveur (voir main.py, événement startup). Toutes les requêtes /predict
réutilisent ensuite la même instance en mémoire.
"""
import logging
import numpy as np
import tensorflow as tf

from app.config import MODEL_PATH, CLASS_NAMES

logger = logging.getLogger(__name__)

_model: tf.keras.Model | None = None


def load_model() -> None:
    """Charge le modèle en mémoire. À appeler une seule fois, au démarrage."""
    global _model
    if _model is not None:
        return
    try:
        _model = tf.keras.models.load_model(MODEL_PATH)
        logger.info("Modèle chargé depuis %s", MODEL_PATH)
    except Exception as exc:
        logger.exception("Échec du chargement du modèle")
        raise RuntimeError("Impossible de charger le modèle d'IA.") from exc


def is_model_loaded() -> bool:
    return _model is not None


def predict(img_array: np.ndarray) -> dict:
    """
    Exécute une inférence sur un batch d'une seule image.

    img_array doit déjà être prétraité par preprocessing.py :
    shape (1, 224, 224, 3), dtype float32, valeurs de pixels BRUTES 0-255
    (le modèle normalise en interne, voir config.py).

    Retourne un dict {prediction, confidence, probabilities}.
    """
    if _model is None:
        raise RuntimeError("Le modèle n'est pas encore chargé.")

    try:
        raw_output = _model.predict(img_array, verbose=0)
    except Exception as exc:
        logger.exception("Erreur pendant l'inférence")
        raise RuntimeError("Erreur pendant la prédiction du modèle.") from exc

    # Sortie sigmoid unique : proba de la classe CLASS_NAMES[1]
    proba_class_1 = float(raw_output[0][0])
    proba_class_0 = 1.0 - proba_class_1

    if proba_class_1 >= 0.5:
        predicted_class = CLASS_NAMES[1]
        confidence = proba_class_1
    else:
        predicted_class = CLASS_NAMES[0]
        confidence = proba_class_0

    return {
        "prediction": predicted_class,
        "confidence": round(confidence * 100, 2),
        "probabilities": {
            CLASS_NAMES[0]: round(proba_class_0 * 100, 2),
            CLASS_NAMES[1]: round(proba_class_1 * 100, 2),
        },
    }
