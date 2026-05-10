from repositorio.paciente_repository import PacienteRepository
from repositorio.tension_repository import TensionRepository
from servicios.tension_service import TensionService


class TensionController:
    def __init__(self, tension_service, tension_repo):
        self.tension_repo = tension_repo
        self.service = tension_service

    def crear(self, tension_data: dict):
        return self.service.crear_tension(tension_data)

    def guardar(self, tension_data: dict):
        return self.crear(tension_data)

    def listar(self):
        return self.service.obtener_todas()

    def listar_por_paciente(self, id_paciente: str):
        return self.service.obtener_por_paciente(id_paciente)

    def actualizar(self, tension_id: str, update_data: dict):
        return self.tension_repo.update(tension_id, update_data)

    def eliminar(self, tension_id: str):
        return self.service.eliminar_tension(tension_id)

    def eliminar_por_paciente(self, id_paciente: str):
        return self.service.eliminar_tensiones_por_paciente(id_paciente)
