from bson import ObjectId

class PacienteRepository:
    def __init__(self, db):
        self.collection = db.db.get_collection("pacientes")

    def create(self, paciente_data: dict):
        """Crea un nuevo paciente"""
        return self.collection.insert_one(paciente_data)

    def get_all(self):
        """Obtiene todos los pacientes"""
        return list(self.collection.find())

    def get_by_id(self, paciente_id: str):
        """Obtiene un paciente por su ID"""
        if not isinstance(paciente_id, ObjectId):
            try:
                paciente_id = ObjectId(paciente_id)
            except Exception:
                pass
        return self.collection.find_one({"_id": paciente_id})

    def get_by_name(self, nombre: str):
        """Obtiene un paciente concreto dado su nombre exacto"""
        return self.collection.find_one({"nombre": nombre})


    def update(self, paciente_id: str, update_data: dict):
        """Actualiza la información de un paciente"""
        if not isinstance(paciente_id, ObjectId):
            try:
                paciente_id = ObjectId(paciente_id)
            except Exception:
                pass
        return self.collection.update_one(
            {"_id": paciente_id},
            {"$set": update_data}
        )

    def delete(self, paciente_id: str):
        """Elimina un paciente por su ID"""
        if not isinstance(paciente_id, ObjectId):
            try:
                paciente_id = ObjectId(paciente_id)
            except Exception:
                pass
        return self.collection.delete_one({"_id": paciente_id})
