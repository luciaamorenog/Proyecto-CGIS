import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pydantic import ValidationError

from controladores.tension_controller import TensionController
from esquemas.tension_schema import TensionCreate

class AltaTensionView(tk.Frame):
    def __init__(self, parent, db, paciente_id=None, on_volver_lista=None):
        super().__init__(parent, bg="#18708C")
        self.controller = TensionController(db)
        
        self.paciente_id = paciente_id
        self.on_volver_lista = on_volver_lista

        tk.Label(self, text="NUEVO REGISTRO DE TENSIÓN", font=("Arial", 14, "bold"), bg="#004B63", fg="white").pack(pady=10, fill="x")

        form_frame = tk.Frame(self, bg="#18708C")
        form_frame.pack(pady=20)

        # Campos Pydantic y Tkinter
        tk.Label(form_frame, bg="#18708C", fg="white", text="ID / Nombre del Paciente (*):").grid(row=0, column=0, sticky="e", pady=5)
        self.ent_id_pac = tk.Entry(form_frame, width=30)
        self.ent_id_pac.grid(row=0, column=1, pady=5)
        if self.paciente_id:
            self.ent_id_pac.insert(0, str(self.paciente_id))

        tk.Label(form_frame, bg="#18708C", fg="white", text="Sistólica (Ej. 120) (*):").grid(row=1, column=0, sticky="e", pady=5)
        self.ent_sistolica = tk.Entry(form_frame, width=30)
        self.ent_sistolica.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, bg="#18708C", fg="white", text="Diastólica (Ej. 80) (*):").grid(row=2, column=0, sticky="e", pady=5)
        self.ent_diastolica = tk.Entry(form_frame, width=30)
        self.ent_diastolica.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, bg="#18708C", fg="white", text="Método:").grid(row=3, column=0, sticky="e", pady=5)
        self.ent_metodo = tk.Entry(form_frame, width=30)
        self.ent_metodo.grid(row=3, column=1, pady=5)

        tk.Label(form_frame, bg="#18708C", fg="white", text="Sitio (Ej. Brazo izquierdo):").grid(row=4, column=0, sticky="e", pady=5)
        self.ent_sitio = tk.Entry(form_frame, width=30)
        self.ent_sitio.grid(row=4, column=1, pady=5)

        tk.Label(form_frame, bg="#18708C", fg="white", text="Brazalete:").grid(row=5, column=0, sticky="e", pady=5)
        self.ent_brazalete = tk.Entry(form_frame, width=30)
        self.ent_brazalete.grid(row=5, column=1, pady=5)

        tk.Label(form_frame, bg="#18708C", fg="white", text="Dispositivo:").grid(row=6, column=0, sticky="e", pady=5)
        self.ent_dispositivo = tk.Entry(form_frame, width=30)
        self.ent_dispositivo.grid(row=6, column=1, pady=5)

        tk.Label(form_frame, bg="#18708C", fg="white", text="Estado:").grid(row=7, column=0, sticky="e", pady=5)
        self.ent_estado = tk.Entry(form_frame, width=30)
        self.ent_estado.grid(row=7, column=1, pady=5)

        tk.Label(form_frame, bg="#18708C", fg="white", text="Fecha (YYYY-MM-DD HH:MM:SS):").grid(row=8, column=0, sticky="e", pady=5)
        self.ent_fecha = tk.Entry(form_frame, width=30)
        self.ent_fecha.grid(row=8, column=1, pady=5)
        self.ent_fecha.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        tk.Label(form_frame, bg="#18708C", fg="white", text="Valoración:").grid(row=9, column=0, sticky="e", pady=5)
        self.ent_valoracion = tk.Entry(form_frame, width=30)
        self.ent_valoracion.grid(row=9, column=1, pady=5)

        # Controles
        btn_frame = tk.Frame(self, bg="#18708C")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="✅ Guardar Tensión", bg="green", fg="white", font=("Arial", 11, "bold"),
                  command=self.guardar).grid(row=0, column=0, padx=10)
        
        if self.on_volver_lista:
            tk.Button(btn_frame, text="Volver Adelante", bg="gray", fg="white", font=("Arial", 11),
                      command=self.on_volver_lista).grid(row=0, column=1, padx=10)

    def guardar(self):
        try:
            # Recolectar datos y preparar para Pydantic
            raw_data = {
                "idPaciente": self.ent_id_pac.get().strip(),
                "sistolica": self.ent_sistolica.get().strip() or 0,
                "diastolica": self.ent_diastolica.get().strip() or 0,
                "metodo": self.ent_metodo.get().strip(),
                "sitio": self.ent_sitio.get().strip(),
                "brazalete": self.ent_brazalete.get().strip(),
                "dispositivo": self.ent_dispositivo.get().strip(),
                "estado": self.ent_estado.get().strip(),
                "fecha": self.ent_fecha.get().strip() or datetime.now(),
                "valoracion": self.ent_valoracion.get().strip()
            }
            
            # Validación mediante Pydantic
            t_schema = TensionCreate(**raw_data)
            
            # Si Pydantic lo valida bien, volcamos el modelo validad en dict
            # Utilizar model_dump() (Pydantic v2) en vez de dict()
            tension_dict = t_schema.model_dump()
            
            self.controller.guardar(tension_dict)
            messagebox.showinfo("Éxito", "Tensión registrada correctamente en la base de datos.")
            
            if self.on_volver_lista:
                self.on_volver_lista()
                
        except ValidationError as ve:
            # Filtrar errores de Pydantic
            msg = "Error en los datos:\n"
            for error in ve.errors():
                campo = error["loc"][0]
                desc = error["msg"]
                msg += f"- {campo}: {desc}\n"
            messagebox.showerror("Error de Validación", msg)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado al guardar:\n{str(e)}")
