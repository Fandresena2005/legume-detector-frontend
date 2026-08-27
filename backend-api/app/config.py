"""
Configuration centralisée du backend.

IMPORTANT — Paramètres du modèle
---------------------------------
Les valeurs ci-dessous ont été déterminées de deux façons différentes :

1. VÉRIFIÉES en inspectant directement le fichier models/model.h5
   (architecture, poids, config Keras) :
   - Framework       : TensorFlow / Keras 3
   - Architecture    : EfficientNetB0 (transfer learning, base gelée)
   - Taille d'entrée : 224x224x3
   - Activation finale : sigmoid (1 neurone) -> classification binaire
   - Preprocessing   : intégré au modèle (Rescaling 1/255 + Normalization
     ImageNet mean=[0.485,0.456,0.406] std=[0.229,0.224,0.225]).
     -> Le backend doit envoyer des pixels BRUTS 0-255, sans normalisation
        manuelle. Le modèle s'en charge en interne.

2. NON VÉRIFIABLE depuis le fichier .h5 seul : l'ORDRE DES CLASSES.
   Cette information dépend uniquement des noms de dossiers utilisés
   pendant l'entraînement (via image_dataset_from_directory, qui trie les
   classes par ordre alphabétique). Ces dossiers ne sont plus disponibles.

   CLASS_NAMES ci-dessous est donc une VALEUR PAR DÉFAUT NON CONFIRMÉE.
   Sortie du modèle proche de 0 -> CLASS_NAMES[0]
   Sortie du modèle proche de 1 -> CLASS_NAMES[1]

   AVANT DE CONSIDÉRER L'API COMME FIABLE :
   Lancez `python scripts/calibrate.py` avec une image que vous savez être
   "saine" et une image que vous savez être "pourrie". Le script vous dira
   si CLASS_NAMES est dans le bon ordre et vous donnera la ligne exacte à
   mettre dans votre .env si ce n'est pas le cas.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Modèle ---
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.h5")
IMG_SIZE = (224, 224)  # Vérifié depuis model.input_shape

# --- Classes (ordre NON confirmé, voir docstring ci-dessus) ---
_raw_classes = os.getenv("CLASS_NAMES", "sain,pourri")
CLASS_NAMES = [c.strip() for c in _raw_classes.split(",")]
if len(CLASS_NAMES) != 2:
    raise ValueError(
        "CLASS_NAMES doit contenir exactement 2 valeurs séparées par une virgule "
        f"(ex: 'sain,pourri'). Valeur actuelle : {_raw_classes!r}"
    )

# --- Upload ---
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/jpg", "image/png"}
MAX_FILE_SIZE_MB = float(os.getenv("MAX_FILE_SIZE_MB", "10"))
MAX_FILE_SIZE_BYTES = int(MAX_FILE_SIZE_MB * 1024 * 1024)

# --- CORS ---
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173")
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]
