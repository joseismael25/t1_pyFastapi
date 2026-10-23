from fastapi import FastAPI, HTTPException, status
from pymongo.errors import PyMongoError

from src.models.model import TraineeModel, TraineeUpdateModel
from src.templates.controllers import (
    create_trainee,
    delete_trainee,
    get_all_trainees,
    get_trainee_by_id,
    update_trainee,
)

app = FastAPI(
    title="Gestión de datos de aprendices",
    description="API para registrar, consultar, actualizar y eliminar aprendices.",
    version="1.0.0",
)


@app.get("/", tags=["Inicio"])
def root():
    return {"mensaje": "La API de aprendices está funcionando", "docs": "/docs"}


@app.post("/Trainees/", response_description="Registrar un aprendiz", status_code=status.HTTP_201_CREATED)
def create_trainee_api(trainee: TraineeModel):
    try:
        return create_trainee(trainee)
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="No se pudo acceder a MongoDB. Revisa la URI y la conexión.") from exc


@app.get("/Trainees/", response_description="Listar todos los aprendices")
def get_all_trainee_api():
    try:
        return get_all_trainees()
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="No se pudo acceder a MongoDB. Revisa la URI y la conexión.") from exc


@app.get("/Trainees/{id}", response_description="Obtener aprendiz por ID")
def get_trainee_by_id_api(id: str):
    try:
        trainee = get_trainee_by_id(id)
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="No se pudo acceder a MongoDB. Revisa la URI y la conexión.") from exc
    if trainee is None:
        raise HTTPException(status_code=404, detail="Aprendiz no encontrado o ID inválido")
    return trainee


@app.put("/Trainees/{id}", response_description="Actualizar un aprendiz")
def update_trainee_api(id: str, data: TraineeUpdateModel):
    try:
        trainee = update_trainee(id, data)
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="No se pudo acceder a MongoDB. Revisa la URI y la conexión.") from exc
    if trainee is None:
        raise HTTPException(status_code=404, detail="Aprendiz no encontrado o ID inválido")
    return trainee


@app.delete("/Trainees/{id}", status_code=status.HTTP_204_NO_CONTENT, response_description="Eliminar un aprendiz")
def delete_trainee_api(id: str):
    try:
        deleted = delete_trainee(id)
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="No se pudo acceder a MongoDB. Revisa la URI y la conexión.") from exc
    if not deleted:
        raise HTTPException(status_code=404, detail="Aprendiz no encontrado o ID inválido")
    return None
