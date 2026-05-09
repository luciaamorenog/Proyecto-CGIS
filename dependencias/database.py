from pymongo import MongoClient


class Database:
    def __init__(self):
        # Utiliza la dependencia externa para traer el objeto DB (db_pipymongo)

        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["myapp"]  # Asegúrate de que el nombre coincida con el de tu base de datos

        if self.db is not None:
            self.pacientes = self.db["pacientes"]
            self.tensiones = self.db["tensiones"]
        else:
            print("AVISO: No se pudo inyectar la BBDD a los modelos.")

    # --- Lógica de Pacientes ---
    def obtener_pacientes(self):
        return list(self.pacientes.find())

    def alta_paciente(self, data):
        return self.pacientes.insert_one(data)

    def baja_paciente(self, id_pac):
        return self.pacientes.delete_one({"id": id_pac})

    # --- Lógica de Tensión ---
    def obtener_tensiones(self):
        return list(self.tensiones.find())

    def alta_tension(self, data):
        return self.tensiones.insert_one(data)
    
    def baja_tension(self, id_pac): # Borra por id de paciente asociado
        return self.tensiones.delete_many({"idPaciente": id_pac})

