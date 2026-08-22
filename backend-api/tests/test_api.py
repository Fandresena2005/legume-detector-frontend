import io
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:  # déclenche le lifespan (chargement du modèle)
        yield c


def _make_test_image(fmt="JPEG", size=(300, 300)) -> bytes:
    img = Image.new("RGB", size, color=(120, 180, 90))
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    buf.seek(0)
    return buf.read()


def test_root_returns_running_status(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "running"


def test_predict_with_valid_image_returns_prediction_and_confidence(client):
    image_bytes = _make_test_image("JPEG")
    response = client.post(
        "/predict",
        files={"file": ("test.jpg", image_bytes, "image/jpeg")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert "prediction" in body
    assert "confidence" in body
    assert 0 <= body["confidence"] <= 100


def test_predict_with_png_image_is_accepted(client):
    image_bytes = _make_test_image("PNG")
    response = client.post(
        "/predict",
        files={"file": ("test.png", image_bytes, "image/png")},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_predict_rejects_unsupported_extension(client):
    response = client.post(
        "/predict",
        files={"file": ("test.txt", b"not an image", "text/plain")},
    )
    assert response.status_code == 400
    body = response.json()
    assert body["status"] == "error"


def test_predict_rejects_empty_file(client):
    response = client.post(
        "/predict",
        files={"file": ("empty.jpg", b"", "image/jpeg")},
    )
    assert response.status_code == 400
    assert response.json()["status"] == "error"


def test_predict_rejects_corrupted_image(client):
    response = client.post(
        "/predict",
        files={"file": ("fake.jpg", b"this is not real image data", "image/jpeg")},
    )
    assert response.status_code == 400
    assert response.json()["status"] == "error"
