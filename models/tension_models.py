from datetime import datetime


class TensionModel:
    def __init__(self, db):
        self.collection = db.db.get_collection("tensiones")

    def crear_tension(self, id_paciente, sistolica, diastolica, metodo, sitio, brazalete, dispositivo, estado, fecha, valoracion, valor_en_rango):
        # Convertir string a objeto datetime para MongoDB
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

    def obtener_todas(self):
        return list(self.collection.find())