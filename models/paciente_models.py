from datetime import datetime


# proyecto/models/paciente_models.py
from datetime import datetime
from base.model_base import ModelBase # Importamos la base

class PacienteModel(ModelBase):
    def __init__(self, db):
        # Llamamos al padre y le decimos que use la colección "pacientes"
        super().__init__(db, "pacientes")

    def crear_paciente(self, nombre, apellidos, genero, fecha_nac):
        fecha_dt = datetime.strptime(fecha_nac, "%Y-%m-%d")
        documento = {
            "nombre": nombre,
            "apellidos": apellidos,
            "genero": genero,
            "fechaNacimiento": fecha_dt
        }
        return self.collection.insert_one(documento)