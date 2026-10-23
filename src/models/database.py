"""Configuración de MongoDB.

La URI se lee de .env o de las variables de entorno. La API puede iniciar
sin MongoDB disponible; las operaciones de datos mostrarán un error 503.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

# Cargar el archivo .env ubicado en la raíz del proyecto, no según el cwd.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

# Aceptar ambos nombres para conservar compatibilidad con la configuración previa.
MONGO_URI = os.getenv("MONGO_URI") or os.getenv("MONGO_URL") or "mongodb+srv://joseismaeldiazvidarte_db_user:mael123@cluster0.21ngghq.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client.dataapren
collection = db.trainee

# No se realiza una conexión de red al importar el módulo. Esto permite que
# / y /docs arranquen incluso si MongoDB no está disponible.
