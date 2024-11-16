'''Versión 3

Usar FastApi para exponer nuestros métodos a internet

1 importar paquete random
2 Definir método 'anotado' para consultar una frase aleatoria
  
	leer todo el contenido del archivo de frases
	Seleccionar aleatoriamente una frase del listado
	Retornarla
	random.choice(lista)
	
3 Configurar seguridad CORS
4 Probar aplicación con servidor uvicorn
'''
import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/getfrase")
def seleccionar_frase():
    nombre_archivo = "frases.txt"
    try:
        with open(nombre_archivo, "r") as file:
            frases = [line.strip() for line in file if line.strip()]
        
        if not frases:
            return {"message": "No hay frases disponibles."}

        return {"frase": random.choice(frases)}  # Retorna una frase en formato JSON

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo de frases no encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al leer las frases.")
