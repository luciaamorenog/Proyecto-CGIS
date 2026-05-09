from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def conectar_db():
    try:
        # 1. Crear el cliente
        cliente = MongoClient("mongodb://127.0.0.1:27017/", serverSelectionTimeoutMS=2000)
        
        # 2. Intentar una operación simple para verificar la conexión
        cliente.admin.command('ping')
        
        print("¡Conexión exitosa a MongoDB!")
        
        # 3. Seleccionar la base de datos
        db = cliente["db_pymongo"]
        return db
        
    except ConnectionFailure:
        print("Error: No se pudo conectar al servidor de MongoDB.")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
