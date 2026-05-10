from repositorio.paciente_repository import PacienteRepository
from repositorio.tension_repository import TensionRepository
from servicios.paciente_service import PacienteService
from servicios.tension_service import TensionService
from controladores.paciente_controller import PacienteController
from controladores.tension_controller import TensionController


class ApplicationManager:
    """Centralized facade managing all repositories, services, and controllers"""

    def __init__(self, db):
        self.db = db
        # Instantiate repositories once
        self._paciente_repo = PacienteRepository(db)
        self._tension_repo = TensionRepository(db)
        # Instantiate services once with injected repos
        self._paciente_service = PacienteService(self._paciente_repo, self._tension_repo)
        self._tension_service = TensionService(self._tension_repo, self._paciente_repo)
        # Instantiate controllers once with services and repos
        self._paciente_controller = PacienteController(self._paciente_service, self._tension_repo)
        self._tension_controller = TensionController(self._tension_service, self._tension_repo)

    @property
    def paciente_controller(self):
        """Returns the pre-configured PacienteController"""
        return self._paciente_controller

    @property
    def tension_controller(self):
        """Returns the pre-configured TensionController"""
        return self._tension_controller