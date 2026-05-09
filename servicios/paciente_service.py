from repositorio.paciente_repository import PacienteRepository
from repositorio.tension_repository import TensionRepository

class PacienteService:
    def __init__(self, paciente_repo: PacienteRepository, tension_repo: TensionRepository):
        self.paciente_repo = paciente_repo
        self.tension_repo = tension_repo

    def crear_paciente(self, paciente_data: dict):
        """Crea un nuevo paciente utilizando el repositorio."""
        return self.paciente_repo.create(paciente_data)

    def obtener_todos(self):
        """Retorna todos los pacientes."""
        return self.paciente_repo.get_all()

    def obtener_por_id(self, paciente_id: str):
        """Retorna un paciente dado su identificador único."""
        return self.paciente_repo.get_by_id(paciente_id)
        
    def actualizar_paciente(self, paciente_id: str, update_data: dict):
        """Actualiza un paciente existente."""
        return self.paciente_repo.update(paciente_id, update_data)

    def eliminar_paciente_y_sus_registros_por_id(self, paciente_id: str):
        """
        Operación de composición:
        Elimina todas las tensiones registradas de un paciente y posteriormente elimina al paciente de la base de datos.
        Esto preserva la integridad referencial a nivel lógico en la app (evita registros de tensión huérfanos).
        """
        # 1. Eliminar datos dependientes en cascada (historial de tensión)
        tensiones_eliminadas = self.tension_repo.delete_by_paciente_id(paciente_id)
        
        # 2. Eliminar la entidad paciente principal
        paciente_eliminado = self.paciente_repo.delete(paciente_id)
        
        return {
            "estado": "exito",
            "tensiones_borradas": tensiones_eliminadas.deleted_count if tensiones_eliminadas else 0,
            "paciente_borrado": paciente_eliminado.deleted_count if paciente_eliminado else 0
        }

    def eliminar_paciente_y_sus_registros_por_nombre(self, nombre: str):
        """
        Operación de composición similar adaptada para el UI donde se borra al paciente por el nombre.
        Garantiza que la eliminación por nombre no deje un historial huérfano.
        """
        paciente = self.paciente_repo.get_by_name(nombre)
        if paciente:
            # Dado que el ID del paciente suele ser lo que se guarda como referencia en "tensiones"
            paciente_id = str(paciente["_id"]) 
            # 1. Borrar todas sus tensiones referenciadas
            tensiones_eliminadas = self.tension_repo.delete_by_paciente_id(paciente_id)
            # También borrar referenciadas usando el nombre si se estuviera guardando el nombre explícitamente allí.
            # Alternativamente si el UI de tensión guarda el ID literal que era el nombre antes, aseguramos por idPaciente=nombre
            self.tension_repo.delete_by_paciente_id(nombre) 

            # 2. Eliminar de verdad al paciente
            paciente_eliminado = self.paciente_repo.delete(paciente["_id"])
            
            return {
                "exito": True,
                "paciente_borrado": paciente_eliminado.deleted_count,
            }
        return {"exito": False, "paciente_borrado": 0}
