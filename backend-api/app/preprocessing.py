"""
Prétraitement de l'image, strictement identique à ce qu'attend le modèle.

Vérifié en inspectant le modèle (voir config.py) :
- taille attendue : 224x224
- 3 canaux (RGB)
- pixels BRUTS 0-255 en float32 : NE PAS diviser par 255 ni normaliser
  manuellement, le modèle contient déjà ses propres couches Rescaling et
  Normalization (poids ImageNet), appliquées automatiquement lors de
  model.predict().
"""
import io
import numpy as np
from PIL import Image, UnidentifiedImageError

from app.config import IMG_SIZE


class ImageValidationError(Exception):
    """Levée quand l'image envoyée n'est pas exploitable."""


def load_and_preprocess_image(file_bytes: bytes) -> np.ndarray:
    if not file_bytes:
        raise ImageValidationError("Le fichier envoyé est vide.")

    try:
        img = Image.open(io.BytesIO(file_bytes))
        img.load()  # force la lecture complète, détecte les fichiers corrompus
    except UnidentifiedImageError as exc:
        raise ImageValidationError("Le fichier envoyé n'est pas une image valide.") from exc
    except Exception as exc:
        raise ImageValidationError("Le fichier envoyé n'est pas une image valide.") from exc

    # Gère RGB, RGBA (transparence) et niveaux de gris en les uniformisant en RGB
    if img.mode != "RGB":
        img = img.convert("RGB")

    img = img.resize(IMG_SIZE, resample=Image.BILINEAR)

    img_array = np.asarray(img, dtype=np.float32)  # pixels bruts 0-255, pas de /255 ici
    img_array = np.expand_dims(img_array, axis=0)  # (1, 224, 224, 3)

    return img_array
