from datetime import datetime


# proyecto/models/tension_models.py
from datetime import datetime
from base.model_base import ModelBase  # Heredamos de la clase principal

class TensionModel(ModelBase):
    def __init__(self, db):
        # Le decimos a la clase principal que use la colección "tensiones"
        super().__init__(db, "tensiones")

    def crear_tension(self, id_paciente, sistolica, diastolica, metodo, sitio, brazalete, dispositivo, estado, fecha, valoracion, valor_en_rango):
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
        documento = {
            "idPaciente": id_paciente,
            "sistolica": sistolica,
            "diastolica": diastolica,
            "metodo": metodo,
            "sitio": sitio,
            "brazalete": brazalete,
            "dispositivo": dispositivo,
            "estado": estado,
            "fecha": fecha_dt,
            "valoracion": valoracion,
            "valorEnRango": valor_en_rango
        }
        return self.collection.insert_one(documento)

    def eliminar_tension_por_paciente(self, id_paciente):
        return self.collection.delete_many({"idPaciente": id_paciente})

    def obtener_por_paciente(self, id_paciente):
        return list(self.collection.find({"idPaciente": id_paciente}))

    