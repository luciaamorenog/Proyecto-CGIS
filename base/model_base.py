# proyecto/base/model_base.py
class ModelBase:
    def __init__(self, db, coleccion_nombre):
        # Todas las clases usarán esta misma forma de conectar
        self.collection = db.db.get_collection(coleccion_nombre)

    def obtener_todos(self):
        return list(self.collection.find())

    def eliminar_por_nombre(self, nombre):
        return self.collection.delete_one({"nombre": nombre})