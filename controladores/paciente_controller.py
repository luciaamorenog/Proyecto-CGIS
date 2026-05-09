from repositorio.paciente_repository import PacienteRepository
from repositorio.tension_repository import TensionRepository
from servicios.paciente_service import PacienteService


class PacienteController:
    def __init__(self, db):
        self.paciente_repo = PacienteRepository(db)
        self.tension_repo = TensionRepository(db)
        self.service = PacienteService(self.paciente_repo, self.tension_repo)

    def crear(self, paciente_data: dict):
        return self.service.crear_paciente(paciente_data)

    def guardar(self, paciente_data: dict):
        return self.crear(paciente_data)

    def listar(self):
        return self.service.obtener_todos()

    def obtener(self, paciente_id: str):
        return self.service.obtener_por_id(paciente_id)

    def actualizar(self, paciente_id: str, update_data: dict):
        return self.service.actualizar_paciente(paciente_id, update_data)

    def eliminar_por_id(self, paciente_id: str):
        return self.service.eliminar_paciente_y_sus_registros_por_id(paciente_id)

    def eliminar_por_nombre(self, nombre: str):
        return self.service.eliminar_paciente_y_sus_registros_por_nombre(nombre)

    def obtener_tensiones(self, paciente_id: str):
        return self.tension_repo.get_by_paciente_id(paciente_id)
