from datetime import datetime


class PacienteModel:
    def __init__(self, db):
        self.collection = db.db.get_collection("pacientes")

    def crear_paciente(self, nombre, apellidos, genero, fecha_nac):
        # Convertir string a objeto datetime para MongoDB
        fecha_dt = datetime.strptime(fecha_nac, "%Y-%m-%d")
        documento = {
            "nombre": nombre,
            "apellidos": apellidos,
            "género": genero,
            "fechaNacimiento": fecha_dt
        }
        return self.collection.insert_one(documento)

    def eliminar_paciente(self, nombre):
        return self.collection.delete_one({"nombre": nombre})

    def obtener_todos(self):
        return list(self.collection.find())