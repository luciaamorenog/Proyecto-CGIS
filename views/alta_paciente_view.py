import tkinter as tk
from tkinter import ttk, messagebox
from controladores.paciente_controller import PacienteController

class AltaPacienteView(tk.Frame):
    def __init__(self, parent, db, on_volver_lista=None):
        super().__init__(parent, bg="#18708C")
        self.controller = PacienteController(db)
        self.on_volver_lista = on_volver_lista
        
        tk.Label(self, text="NUEVO ALTA DE PACIENTE", font=("Arial", 16, "bold"), bg="#004B63", fg="white").pack(pady=20, fill="x")

        # Formulario principal centrado
        form_frame = tk.Frame(self, bg="#18708C")
        form_frame.pack(pady=20)

        # Campos
        tk.Label(form_frame, bg="#18708C", fg="white", font=("Arial", 12), text="Nombre:").grid(row=1, column=0, pady=10, sticky="e")
        self.ent_nombre = tk.Entry(form_frame, font=("Arial", 12), width=25)
        self.ent_nombre.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(form_frame, bg="#18708C", fg="white", font=("Arial", 12), text="Apellido:").grid(row=2, column=0, pady=10, sticky="e")
        self.ent_apellido = tk.Entry(form_frame, font=("Arial", 12), width=25)
        self.ent_apellido.grid(row=2, column=1, pady=10, padx=10)

        # Selector de género bloqueado a valores rígidos
        tk.Label(form_frame, bg="#18708C", fg="white", font=("Arial", 12), text="Género:").grid(row=3, column=0, pady=10, sticky="e")
        self.ent_genero = ttk.Combobox(form_frame, values=["Masculino", "Femenino"], state="readonly", font=("Arial", 12), width=23)
        self.ent_genero.grid(row=3, column=1, pady=10, padx=10)
        self.ent_genero.set("Masculino") # Default

        tk.Label(form_frame, bg="#18708C", fg="white", font=("Arial", 12), text="Fecha Nacimiento (YYYY-MM-DD):").grid(row=4, column=0, pady=10, sticky="e")
        self.ent_fecha = tk.Entry(form_frame, font=("Arial", 12), width=25)
        self.ent_fecha.grid(row=4, column=1, pady=10, padx=10)

        # Control de Botones de Salida
        btn_frame = tk.Frame(self, bg="#18708C")
        btn_frame.pack(pady=30)

        tk.Button(btn_frame, text="✅ Guardar Paciente", bg="green", fg="white", font=("Arial", 12, "bold"),
                  command=self.guardar, width=20, cursor="hand2").grid(row=0, column=0, padx=15)
        
        if self.on_volver_lista:
            tk.Button(btn_frame, text="❌ Volver atrás", bg="red", fg="white", font=("Arial", 12, "bold"),
                      command=self.on_volver_lista, width=20, cursor="hand2").grid(row=0, column=1, padx=15)

    def guardar(self):
        try:
            from datetime import datetime
            fecha_dt = datetime.strptime(self.ent_fecha.get(), "%Y-%m-%d")
            
            paciente_data = {
                "nombre": self.ent_nombre.get(),
                "apellido": self.ent_apellido.get(),
                "género": self.ent_genero.get(),
                "fechaNacimiento": fecha_dt
            }
            self.controller.guardar(paciente_data)
            messagebox.showinfo("Éxito", "Paciente guardado correctamente en la Base de Datos")
            
            # Navegar automáticamente a la lista si hay éxito
            if self.on_volver_lista:
                self.on_volver_lista()
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
