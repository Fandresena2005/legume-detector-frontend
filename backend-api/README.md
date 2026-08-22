# Fruit & Vegetable Detection API

Backend FastAPI qui reçoit une image de fruit/légume et prédit s'il est **sain** ou **pourri**, avec un score de confiance.

## ⚠️ À faire avant la mise en production : calibrer l'ordre des classes

Le modèle fourni (`models/model.h5`) a été analysé en détail (architecture, taille d'entrée, preprocessing) directement depuis le fichier `.h5`, sans rien supposer. Voir le détail complet en commentaire dans `app/config.py`.

**Une seule information n'a pas pu être récupérée** : l'ordre des classes (quelle sortie du modèle correspond à "sain" et laquelle à "pourri"). Cette information dépendait des noms de dossiers utilisés pendant l'entraînement, qui ne sont plus disponibles.

Une valeur par défaut (`sain,pourri`) est utilisée dans `.env.example`, **non confirmée**. Avant de faire confiance aux résultats de l'API :

```bash
python scripts/calibrate.py chemin/vers/image_saine_connue.jpg sain
python scripts/calibrate.py chemin/vers/image_pourrie_connue.jpg pourri
```

Le script vous dira si l'ordre est correct, et sinon vous donnera la ligne exacte à mettre dans `.env`.

## 1. Installer Python

Assurez-vous d'avoir Python 3.11 ou supérieur :

```bash
python --version
```

Si ce n'est pas le cas, téléchargez-le depuis [python.org](https://www.python.org/downloads/).

## 2. Créer un environnement virtuel

```bash
python -m venv venv
```

Activation :

- **Windows** : `venv\Scripts\activate`
- **macOS / Linux** : `source venv/bin/activate`

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

> Le fichier utilise `tensorflow-cpu`. Si vous avez un GPU compatible CUDA, remplacez-le par `tensorflow` dans `requirements.txt` pour de meilleures performances.

## 4. Placer le modèle

Le modèle `model.h5` doit se trouver dans `models/model.h5` (déjà en place si vous utilisez ce dossier tel quel). Si vous changez son emplacement, mettez à jour `MODEL_PATH` dans votre `.env`.

## 5. Configurer les variables d'environnement

```bash
cp .env.example .env
```

Puis éditez `.env` selon vos besoins (voir la section calibration ci-dessus pour `CLASS_NAMES`).

## 6. Démarrer le serveur

```bash
uvicorn app.main:app --reload
```

Le serveur démarre sur `http://127.0.0.1:8000`. Le modèle est chargé une seule fois au démarrage (pas à chaque requête).

## 7. Tester l'API

### Via la documentation interactive

Ouvrez `http://127.0.0.1:8000/docs` dans votre navigateur (Swagger UI). Vous pouvez y envoyer une image directement depuis l'interface.

Une version alternative de la documentation est disponible sur `http://127.0.0.1:8000/redoc`.

### Via curl

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -F "file=@chemin/vers/votre_image.jpg"
```

Réponse attendue :

```json
{
  "status": "success",
  "prediction": "sain",
  "confidence": 94.72,
  "probabilities": {
    "sain": 94.72,
    "pourri": 5.28
  }
}
```

### Vérifier que le serveur tourne

```bash
curl http://127.0.0.1:8000/
```

```json
{"message": "Fruit & Vegetable Detection API", "status": "running"}
```

## 8. Connecter le frontend (React/Vite)

Le fichier `.env` contient `ALLOWED_ORIGINS`, qui détermine quelles origines peuvent appeler l'API (CORS). Par défaut :

```
http://localhost:3000
http://localhost:5173
```

Depuis votre frontend :

```javascript
const formData = new FormData();
formData.append("file", imageFile); // imageFile = File venant d'un <input type="file">

const response = await fetch("http://127.0.0.1:8000/predict", {
  method: "POST",
  body: formData,
});

const result = await response.json();
// { status: "success", prediction: "sain", confidence: 94.72, probabilities: {...} }
```

Si votre frontend tourne sur un autre port, ajoutez-le à `ALLOWED_ORIGINS` dans `.env`.

## 9. Lancer les tests

```bash
pip install pytest httpx
pytest tests/ -v
```

Les tests vérifient : le démarrage de l'API, l'endpoint `/`, l'envoi d'une image valide, le rejet d'un mauvais format, et la présence de `prediction`/`confidence` dans la réponse.

## Structure du projet

```text
backend/
├── app/
│   ├── main.py           # Endpoints FastAPI, CORS, gestion des erreurs
│   ├── model.py           # Chargement et inférence du modèle
│   ├── preprocessing.py   # Redimensionnement image, conversion RGB
│   ├── config.py          # Configuration centralisée (voir docstring)
│   └── schemas.py         # Modèles Pydantic des réponses
├── models/
│   └── model.h5            # Le modèle entraîné
├── scripts/
│   └── calibrate.py        # Script pour vérifier l'ordre des classes
├── tests/
│   └── test_api.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Détails techniques du modèle (vérifiés)

- **Framework** : TensorFlow / Keras 3
- **Architecture** : EfficientNetB0 (transfer learning, base gelée à l'entraînement)
- **Entrée** : images 224×224×3 (RGB)
- **Sortie** : 1 neurone, activation sigmoid → classification binaire
- **Preprocessing** : intégré au modèle (couches `Rescaling` + `Normalization` avec statistiques ImageNet). Le backend envoie donc des pixels **bruts 0–255**, sans normalisation manuelle — toute normalisation supplémentaire côté backend fausserait les prédictions.

## Erreurs gérées

L'API ne renvoie jamais de détails internes (chemins système, stack traces) au client. Toutes les erreurs suivent ce format :

```json
{
  "status": "error",
  "message": "Description compréhensible de l'erreur."
}
```

Cas couverts : fichier absent, fichier vide, format non supporté, image corrompue/invalide, fichier trop volumineux, erreur de preprocessing, erreur du modèle non chargé, erreur pendant la prédiction.
