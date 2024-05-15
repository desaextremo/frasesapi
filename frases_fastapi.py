'''Versión 2

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
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


#Llamamos a FastAPI, y desde este momento haremos referencia a este mediante la variable 'app'
app = FastAPI()

# Permitir solicitudes desde todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto a los orígenes que desees permitir
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


#Definir función 'anotada' para consultar una frase aleatoria
@app.get("/getfrase")
def seleccionar_frase():
    nombre_archivo = "frases.txt"

    #abrir archivo
    archivo = open(nombre_archivo,"r",encoding="utf8")

    #carga el contenido del archivo en una lista
    frases = archivo.readlines()

    ##cierro el archivo
    archivo.close()
    
    #Seleccionar una frase aleatoriamente de la lista
    return random.choice(frases)
