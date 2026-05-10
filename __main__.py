import tkinter as tk
from tkinter import ttk

from datetime import datetime
from dependencias.database import Database
from aplicacion.application_manager import ApplicationManager
from views.paciente_view import PacienteView
from views.tension_view import TensionView
from views.bienvenida_view import BienvenidaView
from views.alta_paciente_view import AltaPacienteView
from views.alta_tension_view import AltaTensionView

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Médico PyMongo")
        self.config(bg="#18708C")
        self.geometry("700x500")

        # Configurar estilos globales de los Treeview
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview.Heading", background="#004B63", foreground="white", font=("Arial", 10, "bold"))

        self.db_gestor = Database()
        self.app_manager = ApplicationManager(self.db_gestor)
        
        # Contenedor dinámico
        self.contenedor = tk.Frame(self, bg="#18708C")
        self.contenedor.pack(fill="both", expand=True)
        
        self._configurar_menu()
        self.mostrar_bienvenida() # Vista inicial

    def _configurar_menu(self):
        barra_menu = tk.Menu(self)
        self.config(menu=barra_menu)
        
        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Secciones", menu=menu_archivo)
        menu_archivo.add_command(label="Inicio", command=self.mostrar_bienvenida)
        menu_archivo.add_command(label="Pacientes", command=self.mostrar_pacientes)
        menu_archivo.add_command(label="Tensión Arterial", command=self.mostrar_tension)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.quit)

    def limpiar_pantalla(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def mostrar_bienvenida(self):
        self.limpiar_pantalla()
        BienvenidaView(self.contenedor, on_ir_pacientes=self.mostrar_pacientes, on_ir_tensiones=self.mostrar_tension).pack(fill="both", expand=True)

    def mostrar_pacientes(self):
        self.limpiar_pantalla()
        PacienteView(self.contenedor, self.app_manager, on_ver_tensiones=self.mostrar_tension_paciente, on_ir_alta_paciente=self.mostrar_alta_paciente, on_volver_inicio=self.mostrar_bienvenida).pack(fill="both", expand=True)

    def mostrar_alta_paciente(self):
        self.limpiar_pantalla()
        AltaPacienteView(self.contenedor, self.app_manager, on_volver_lista=self.mostrar_pacientes).pack(fill="both", expand=True)

    def mostrar_tension(self):
        self.limpiar_pantalla()
        TensionView(self.contenedor, self.app_manager, on_volver=self.mostrar_pacientes, on_volver_inicio=self.mostrar_bienvenida, on_ir_alta_tension=self.mostrar_alta_tension).pack(fill="both", expand=True)

    def mostrar_tension_paciente(self, paciente_id):
        self.limpiar_pantalla()
        TensionView(self.contenedor, self.app_manager, paciente_id=paciente_id, on_volver=self.mostrar_pacientes, on_volver_inicio=self.mostrar_bienvenida, on_ir_alta_tension=self.mostrar_alta_tension).pack(fill="both", expand=True)
        
    def mostrar_alta_tension(self, paciente_id=None):
        self.limpiar_pantalla()
        AltaTensionView(self.contenedor, self.app_manager, paciente_id=paciente_id, on_volver_lista=lambda: self.mostrar_tension_paciente(paciente_id) if paciente_id else self.mostrar_tension()).pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()