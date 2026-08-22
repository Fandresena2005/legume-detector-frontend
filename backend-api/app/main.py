import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import (
    ALLOWED_ORIGINS,
    ALLOWED_EXTENSIONS,
    ALLOWED_CONTENT_TYPES,
    MAX_FILE_SIZE_BYTES,
    MAX_FILE_SIZE_MB,
)
from app import model as model_module
from app.preprocessing import load_and_preprocess_image, ImageValidationError
from app.schemas import PredictionResponse, RootResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Chargé une seule fois au démarrage, pas à chaque requête.
    model_module.load_model()
    yield


app = FastAPI(
    title="Fruit & Vegetable Detection API",
    description="Détecte si un fruit ou légume est sain ou pourri à partir d'une image.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def _error_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"status": "error", "message": message})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Ex: aucun fichier envoyé sur /predict. On garde le format d'erreur uniforme
    # plutôt que le format brut de FastAPI/Pydantic.
    return _error_response(400, "Requête invalide : vérifiez qu'un fichier a bien été envoyé.")


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Ne jamais exposer les détails internes / chemins système au client.
    logger.exception("Erreur non gérée sur %s", request.url.path)
    return _error_response(500, "Une erreur interne est survenue.")


@app.get("/", response_model=RootResponse)
async def root():
    return RootResponse()


@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    if not model_module.is_model_loaded():
        return _error_response(503, "Le modèle n'est pas encore prêt. Réessayez dans un instant.")

    if not file or not file.filename:
        return _error_response(400, "Aucun fichier n'a été envoyé.")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return _error_response(
            400,
            f"Format de fichier non supporté ({ext or 'inconnu'}). "
            f"Formats acceptés : {', '.join(sorted(ALLOWED_EXTENSIONS))}.",
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        return _error_response(400, "Le type de fichier envoyé n'est pas une image valide.")

    contents = await file.read()

    if not contents:
        return _error_response(400, "Le fichier envoyé est vide.")

    if len(contents) > MAX_FILE_SIZE_BYTES:
        return _error_response(
            400, f"Le fichier dépasse la taille maximale autorisée ({MAX_FILE_SIZE_MB} Mo)."
        )

    try:
        img_array = load_and_preprocess_image(contents)
    except ImageValidationError as exc:
        return _error_response(400, str(exc))
    except Exception:
        logger.exception("Erreur de preprocessing")
        return _error_response(500, "Erreur lors du traitement de l'image.")

    try:
        result = model_module.predict(img_array)
    except Exception:
        logger.exception("Erreur d'inférence")
        return _error_response(500, "Erreur lors de la prédiction.")

    return {"status": "success", **result}
