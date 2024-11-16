import pytest
from fastapi.testclient import TestClient
from frases_fastapi import app
import os

client = TestClient(app)

def test_get_frase():
    response = client.get("/getfrase")
    assert response.status_code == 200
    frase_data = response.json()

    # Verificar si el archivo frases.txt contiene frases
    if "frase" in frase_data:
        assert isinstance(frase_data["frase"], str)
        assert len(frase_data["frase"]) > 0
    else:
        # En caso de que no haya frases disponibles
        assert frase_data == {"message": "No hay frases disponibles."}

def test_empty_file():
    # Guarda el contenido original de frases.txt
    with open("frases.txt", "r") as f:
        original_content = f.read()

    # Simular un archivo vacío
    with open("frases.txt", "w") as f:
        f.write("")
    
    response = client.get("/getfrase")
    assert response.status_code == 200
    assert response.json() == {"message": "No hay frases disponibles."}

    # Restaurar el contenido original de frases.txt
    with open("frases.txt", "w") as f:
        f.write(original_content)

def test_file_not_found():
    # Simular un archivo inexistente renombrándolo temporalmente
    if os.path.exists("frases.txt"):
        os.rename("frases.txt", "frases_backup.txt")

    response = client.get("/getfrase")
    assert response.status_code == 404
    assert response.json() == {"detail": "Archivo de frases no encontrado."}

    # Restaurar el archivo después de la prueba
    if os.path.exists("frases_backup.txt"):
        os.rename("frases_backup.txt", "frases.txt")

def test_randomness():
    # Realiza cinco solicitudes y obtiene las frases si están disponibles
    responses = {
        client.get("/getfrase").json().get("frase")
        for _ in range(5)
        if client.get("/getfrase").json().get("frase") is not None
    }
    assert len(responses) > 1, "Se espera al menos dos frases diferentes en el archivo para probar la aleatoriedad."

def test_concurrent_requests():
    responses = [client.get("/getfrase") for _ in range(10)]
    assert all(response.status_code == 200 for response in responses)
    assert all("frase" in response.json() or "message" in response.json() for response in responses)
