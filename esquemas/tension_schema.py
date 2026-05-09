from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from datetime import datetime

class TensionCreate(BaseModel):
    idPaciente: str = Field(..., min_length=1, description="ID del paciente asociado")
    sistolica: int = Field(..., gt=0, lt=300, description="Presión sistólica")
    diastolica: int = Field(..., gt=0, lt=200, description="Presión diastólica")
    metodo: Optional[str] = ""
    sitio: Optional[str] = ""
    brazalete: Optional[str] = ""
    dispositivo: Optional[str] = ""
    estado: Optional[str] = ""
    fecha: datetime = Field(default_factory=datetime.now)
    valoracion: Optional[str] = ""
