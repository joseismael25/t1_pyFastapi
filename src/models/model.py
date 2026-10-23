from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TraineeModel(BaseModel):
    """Datos requeridos para registrar un aprendiz."""

    model_config = ConfigDict(str_strip_whitespace=True)

    document: str = Field(min_length=1)
    firstname: str = Field(min_length=1)
    lastname: str = Field(min_length=1)
    email: EmailStr
    age: int = Field(ge=0)
    program: str = Field(min_length=1)
    record_number: int = Field(ge=0)


class TraineeUpdateModel(BaseModel):
    """Campos opcionales para actualizar un aprendiz."""

    model_config = ConfigDict(str_strip_whitespace=True)

    firstname: Optional[str] = Field(default=None, min_length=1)
    lastname: Optional[str] = Field(default=None, min_length=1)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(default=None, ge=0)
    program: Optional[str] = Field(default=None, min_length=1)
    record_number: Optional[int] = Field(default=None, ge=0)


# Compatibilidad con nombres antiguos que pudiera usar código del proyecto.
traineeModel = TraineeModel
traineeUpdateModel = TraineeUpdateModel
