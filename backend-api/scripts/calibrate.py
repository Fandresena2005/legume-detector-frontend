"""
Script de calibration — à lancer UNE FOIS avant de faire confiance à l'API.

L'ordre des classes (CLASS_NAMES dans .env / config.py) n'a pas pu être
déterminé depuis le fichier model.h5 seul : cette info dépendait des noms
de dossiers utilisés pendant l'entraînement, qui ne sont plus disponibles.

Ce script vous fait tester le modèle avec une image dont vous connaissez
l'état réel, et vous dit si CLASS_NAMES est dans le bon ordre.

Usage :
    python scripts/calibrate.py chemin/vers/image_saine.jpg sain
    python scripts/calibrate.py chemin/vers/image_pourrie.jpg pourri
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.config import CLASS_NAMES  # noqa: E402
from app import model as model_module  # noqa: E402
from app.preprocessing import load_and_preprocess_image  # noqa: E402


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    image_path, known_label = sys.argv[1], sys.argv[2]

    if not os.path.isfile(image_path):
        print(f"Fichier introuvable : {image_path}")
        sys.exit(1)

    with open(image_path, "rb") as f:
        contents = f.read()

    model_module.load_model()
    img_array = load_and_preprocess_image(contents)
    result = model_module.predict(img_array)

    print(f"\nImage         : {image_path}")
    print(f"Label attendu : {known_label}")
    print(f"Label prédit  : {result['prediction']} (confiance {result['confidence']}%)")
    print(f"Probabilités  : {result['probabilities']}")
    print(f"CLASS_NAMES actuel dans config : {CLASS_NAMES}")

    if result["prediction"] == known_label:
        print("\n✅ La prédiction correspond au label attendu. CLASS_NAMES semble correct.")
    else:
        swapped = list(reversed(CLASS_NAMES))
        print(
            "\n⚠️  La prédiction NE correspond PAS au label attendu.\n"
            f"L'ordre des classes est probablement inversé.\n"
            f"Mettez ceci dans votre .env :\n\n"
            f"CLASS_NAMES={','.join(swapped)}\n"
        )
    print(
        "\nPour une calibration fiable, testez au moins une image de chaque classe "
        "(une clairement saine, une clairement pourrie)."
    )


if __name__ == "__main__":
    main()
