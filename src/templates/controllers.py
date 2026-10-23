from bson import ObjectId
from bson.errors import InvalidId

from src.models.database import collection
from src.models.model import TraineeModel, TraineeUpdateModel


def helper_trainee(trainee) -> dict:
    """Convertir un documento MongoDB a un diccionario serializable."""
    if not trainee:
        return None
    return {
        "_id": str(trainee["_id"]),
        "document": trainee.get("document"),
        "firstname": trainee.get("firstname"),
        "lastname": trainee.get("lastname"),
        "email": trainee.get("email"),
        "age": trainee.get("age"),
        "program": trainee.get("program"),
        "record_number": trainee.get("record_number"),
    }


def create_trainee(trainee: TraineeModel):
    trainee_dict = trainee.model_dump()
    result = collection.insert_one(trainee_dict)
    new_trainee = collection.find_one({"_id": result.inserted_id})
    return helper_trainee(new_trainee)


def get_all_trainees():
    return [helper_trainee(item) for item in collection.find()]


def get_trainee_by_id(id: str):
    try:
        object_id = ObjectId(id)
    except (InvalidId, TypeError):
        return None
    return helper_trainee(collection.find_one({"_id": object_id}))


def update_trainee(id: str, data: TraineeUpdateModel):
    try:
        object_id = ObjectId(id)
    except (InvalidId, TypeError):
        return None

    data_update = {
        key: value
        for key, value in data.model_dump(exclude_unset=True).items()
        if value is not None
    }
    if data_update:
        collection.update_one({"_id": object_id}, {"$set": data_update})

    return helper_trainee(collection.find_one({"_id": object_id}))


def delete_trainee(id: str):
    try:
        object_id = ObjectId(id)
    except (InvalidId, TypeError):
        return False
    result = collection.delete_one({"_id": object_id})
    return result.deleted_count > 0
