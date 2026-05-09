from pydantic import BaseModel, Field, ValidationError, validator
from typing import Optional
import re

class PacienteCreate(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre del paciente")
    apellidos: str = Field(..., min_length=1, description="Apellidos del paciente")
    genero: str = Field(..., min_length=1, description="Género del paciente")
    fecha_nac: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$', description="Fecha de nacimiento en formato YYYY-MM-DD")

    @validator('nombre', 'apellidos')
    def validar_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('Este campo no puede estar vacío')
        return v.strip()

    @validator('fecha_nac')
    def validate_fecha_nac(cls, v):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
            raise ValueError('La fecha debe tener el formato YYYY-MM-DD')
        return v