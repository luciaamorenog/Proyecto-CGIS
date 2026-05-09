import tkinter as tk
from tkinter import messagebox
from views.paciente_view import PacienteView

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Salud")
        self.geometry("800x600")

        # Contenedor principal donde cargaremos las vistas
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self._crear_menu()
        self.mostrar_pacientes() # Vista por defecto

    def _crear_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        opciones_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Gestión", menu=opciones_menu)
        
        opciones_menu.add_command(label="Pacientes", command=self.mostrar_pacientes)
        opciones_menu.add_command(label="Tensión Arterial", command=self.mostrar_tension)
        opciones_menu.add_separator()
        opciones_menu.add_command(label="Salir", command=self.quit)

    def limpiar_contenedor(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def mostrar_pacientes(self):
        self.limpiar_contenedor()
        PacienteView(self.container).pack(fill="both", expand=True)

    #def mostrar_tension(self):
      #  self.limpiar_contenedor()
     #   TensionView(self.container).pack(fill="both", expand=True)