from bson import ObjectId

class TensionRepository:
    def __init__(self, db):
        self.collection = db.db.get_collection("tensiones")

    def create(self, tension_data: dict):
        """Crea un nuevo registro de tensión"""
        return self.collection.insert_one(tension_data)

    def get_all(self):
        """Obtiene todos los registros de tensión"""
        return list(self.collection.find())

    def get_by_id(self, tension_id: str):
        """Obtiene un registro de tensión por su ID"""
        if not isinstance(tension_id, ObjectId):
            try:
                tension_id = ObjectId(tension_id)
            except Exception:
                pass
        return self.collection.find_one({"_id": tension_id})

    def get_by_paciente_id(self, id_paciente: str):
        """Obtiene todos los registros de tensión de un paciente específico"""
        return list(self.collection.find({"idPaciente": id_paciente}))

    def update(self, tension_id: str, update_data: dict):
        """Actualiza la información de un registro de tensión"""
        if not isinstance(tension_id, ObjectId):
            try:
                tension_id = ObjectId(tension_id)
            except Exception:
                pass
        return self.collection.update_one(
            {"_id": tension_id},
            {"$set": update_data}
        )

    def delete(self, tension_id: str):
        """Elimina un registro de tensión por su ID"""
        if not isinstance(tension_id, ObjectId):
            try:
                tension_id = ObjectId(tension_id)
            except Exception:
                pass
        return self.collection.delete_one({"_id": tension_id})

    def delete_by_paciente_id(self, id_paciente: str):
        """Elimina todos los registros de tensión médica asociados a un paciente"""
        return self.collection.delete_many({"idPaciente": id_paciente})

