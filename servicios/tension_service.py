from repositorio.paciente_repository import PacienteRepository
from repositorio.tension_repository import TensionRepository

class TensionService:
    def __init__(self, tension_repo: TensionRepository, paciente_repo: PacienteRepository = None):
        self.tension_repo = tension_repo
        # Es opcional, lo usamos para posibles validaciones cruzadas
        self.paciente_repo = paciente_repo  

    def crear_tension(self, tension_data: dict):
        """
        Operación de Composición/Regla de negocio: 
        Permite validar lógicas previas antes de insertar, por ejemplo 
        calcular de manera computada si la presión captada está o no en un rango saludable.
        """
        # Regla de negocio de ejemplo (Composición con cálculos internos)
        sistolica = tension_data.get("sistolica", 0)
        diastolica = tension_data.get("diastolica", 0)
        
        # Inyecta el campo valorEnRango basado en reglas de negocio en vez de fiarse del frontend ciegamente
        tension_data["valorEnRango"] = (90 <= sistolica <= 120) and (60 <= diastolica <= 80)

        # Si tuviéramos un paciente_repo, podríamos verificar que la id del paciente existe primero:
        # if self.paciente_repo:
        #    if not self.paciente_repo.get_by_id(tension_data.get("idPaciente")):
        #         raise ValueError("El paciente al que se intenta vincular la tensión no existe")

        return self.tension_repo.create(tension_data)

    def obtener_todas(self):
        """Obtiene el historial completo de tensiones de todos"""
        return self.tension_repo.get_all()

    def obtener_por_paciente(self, id_paciente: str):
        """Obtiene un resumen del historial filtrado"""
        return self.tension_repo.get_by_paciente_id(id_paciente)
        
    def eliminar_tension(self, tension_id: str):
        """Eliminación directa"""
        return self.tension_repo.delete(tension_id)
        
    def eliminar_tensiones_por_paciente(self, id_paciente: str):
        """Eliminación agrupada delegada al repositorio"""
        return self.tension_repo.delete_by_paciente_id(id_paciente)
