import tkinter as tk
from tkinter import ttk, messagebox
from controladores.paciente_controller import PacienteController

class PacienteView(tk.Frame):
    def __init__(self, parent, db, on_ver_tensiones=None, on_volver_inicio=None, on_ir_alta_paciente=None):
        super().__init__(parent, bg="#18708C")
        self.controller = PacienteController(db)
        self.on_ver_tensiones = on_ver_tensiones
        self.on_volver_inicio = on_volver_inicio
        self.on_ir_alta_paciente = on_ir_alta_paciente
        
        tk.Label(self, text="GESTIÓN DE PACIENTES", font=("Arial", 14, "bold"), bg="#004B63", fg="white").pack(pady=10, fill="x")

        # Botones de Acción
        btn_frame = tk.Frame(self, bg="#18708C")
        btn_frame.pack(pady=10)

        if self.on_ir_alta_paciente:
            tk.Button(btn_frame, text="➕ Añadir Nuevo", bg="green", fg="white", font=("Arial", 10, "bold"),
                      command=self.on_ir_alta_paciente).grid(row=0, column=0, padx=5)
        
        tk.Button(btn_frame, text="🗑️ Baja Paciente", bg="red", fg="white", font=("Arial", 10, "bold"),
                  command=self.eliminar).grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text="📋 Ver Ficha", bg="#008CBA", fg="white", font=("Arial", 10, "bold"), command=self.ver_ficha).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="🔄 Refrescar", bg="#FF9800", fg="white", font=("Arial", 10, "bold"), command=self.listar).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Ordenar por Apellido", command=self.ordenar_por_apellido).grid(row=0, column=4, padx=5)

        if self.on_volver_inicio:
            tk.Button(btn_frame, text="🏠 Inicio", bg="gray", fg="white", 
                      command=self.on_volver_inicio).grid(row=0, column=5, padx=5)


        # Lista de pacientes
        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Apellido", "Género", "Fecha"), show="headings", displaycolumns=("Nombre", "Apellido", "Género", "Fecha"))
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Género", text="Género")
        self.tree.heading("Fecha", text="Fecha Nacimiento")
        self.tree.pack(fill="both", expand=True, pady=10)
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # Cargar lista inicialmente
        self.listar()

    def on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.abrir_tensiones()

    def abrir_tensiones(self):
        item = self.tree.selection()
        if item and self.on_ver_tensiones:
            paciente_id = self.tree.item(item[0], "values")[0]
            self.on_ver_tensiones(paciente_id)
        elif not item:
            messagebox.showwarning("Aviso", "Selecciona un paciente primero en la lista (clic o doble clic)")

    def ver_ficha(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un paciente en la lista para ver su ficha")
            return
            
        paciente_id = self.tree.item(item[0], "values")[0]
        paciente_nombre = self.tree.item(item[0], "values")[1]
        paciente = self.controller.obtener(paciente_id)
        
        # Fallback for older schemas where name is used as ID or ID wasn't returned appropriately
        if not paciente:
            paciente = self.controller.paciente_repo.get_by_name(paciente_nombre)
            
        if not paciente:
            messagebox.showerror("Error", "No se encontró la información del paciente")
            return
            
        # Crear ventana Toplevel para mostrar la ficha
        ficha_win = tk.Toplevel(self)
        nombre_completo = f"{paciente.get('nombre', '')} {paciente.get('apellido', '')}".strip()
        ficha_win.title(f"Ficha de Paciente - {nombre_completo}")
        ficha_win.geometry("550x550")
        ficha_win.configure(bg="#F0F0F0")
        ficha_win.transient(self.winfo_toplevel())  # Asegura que se abra encima pero atada a la principal
        ficha_win.grab_set()  # Modal
        
        # Título
        tk.Label(ficha_win, text=f"FICHA: {nombre_completo.upper()}", font=("Arial", 14, "bold"), bg="#004B63", fg="white").pack(pady=10, fill="x")
        
        # Crear Notebook para las pestañas
        notebook = ttk.Notebook(ficha_win)
        notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # ----- PESTAÑA 1: DATOS PERSONALES -----
        tab_personales = tk.Frame(notebook, bg="#F0F0F0")
        notebook.add(tab_personales, text="Datos Personales")
        
        detalles_frame = tk.Frame(tab_personales, bg="#F0F0F0", padx=20, pady=10)
        detalles_frame.pack(fill="both", expand=True)
        
        campos = [
            ("ID", str(paciente.get("_id", "N/A"))),
            ("Nombre", paciente.get("nombre", "")),
            ("Apellidos", paciente.get("apellido", "No especificado")),
            ("Género", paciente.get("género", "No especificado")),
            ("Fecha Nacimiento", paciente.get("fechaNacimiento", "").strftime("%d/%m/%Y") if hasattr(paciente.get("fechaNacimiento"), 'strftime') else paciente.get("fechaNacimiento", "No indicada")),
            ("Edad", self._calcular_edad(paciente.get("fechaNacimiento"))),
            ("Teléfono", paciente.get("telefono", "No especificado")),
            ("Email", paciente.get("correo", paciente.get("email", "No especificado"))),
            ("Dirección", paciente.get("direccion", "No especificada")),
            ("Observaciones", paciente.get("notas", paciente.get("observaciones", "Sin observaciones importantes")))
        ]
        
        for i, (label_text, valor) in enumerate(campos):
            tk.Label(detalles_frame, text=f"{label_text}:", font=("Arial", 10, "bold"), bg="#F0F0F0", anchor="e", width=15).grid(row=i, column=0, sticky="e", pady=8, padx=5)
            tk.Label(detalles_frame, text=str(valor), font=("Arial", 10), bg="#F0F0F0", anchor="w", wraplength=250, justify="left").grid(row=i, column=1, sticky="w", pady=8, padx=5)

        # ----- PESTAÑA 2: HISTORIAL DE TENSIONES -----
        tab_tensiones = tk.Frame(notebook, bg="#F0F0F0")
        notebook.add(tab_tensiones, text="Historial de Tensión")
        
        # Obtener tensiones del paciente
        id_pac_str = str(paciente.get("_id", paciente_nombre))
        tensiones = self.controller.obtener_tensiones(id_pac_str)
        # Fallback si las tensiones estuvieran referenciadas por nombre
        if not tensiones:
             tensiones = self.controller.obtener_tensiones(paciente_nombre)

        if not tensiones:
            tk.Label(tab_tensiones, text="No hay registros de tensión médica para este paciente.", font=("Arial", 11, "italic"), bg="#F0F0F0", fg="#555").pack(pady=40)
        else:
            # Treeview de tensiones en la pestaña
            col_tens = ("Fecha", "Sistólica", "Diastólica", "Frec. Card.", "Estado")
            tree_tens = ttk.Treeview(tab_tensiones, columns=col_tens, show="headings", height=10)
            
            for col in col_tens:
                tree_tens.heading(col, text=col)
                w = 120 if col == "Fecha" else 80
                tree_tens.column(col, width=w, anchor="center")
            
            # Scrollbar para la tabla
            scroll_tens = ttk.Scrollbar(tab_tensiones, orient="vertical", command=tree_tens.yview)
            tree_tens.configure(yscrollcommand=scroll_tens.set)
            
            scroll_tens.pack(side="right", fill="y", pady=10)
            tree_tens.pack(fill="both", expand=True, padx=10, pady=10)

            # Poblar la tabla de tensiones
            for t in tensiones:
                fecha_t = t.get("fecha", "")
                if hasattr(fecha_t, "strftime"):
                    fecha_t = fecha_t.strftime("%d/%m/%Y %H:%M")
                sist = t.get("sistolica", "-")
                diast = t.get("diastolica", "-")
                fc = t.get("frecuenciaCardiaca", "-")
                en_rango = t.get("valorEnRango")
                estado = "Dentro de rango" if en_rango else "Fuera de rango"
                
                tree_tens.insert("", "end", values=(fecha_t, sist, diast, fc, estado))

        # Botón cerrar
        btn_cerrar = tk.Frame(ficha_win, bg="#F0F0F0")
        btn_cerrar.pack(fill="x", pady=10)
        tk.Button(btn_cerrar, text="Cerrar Ficha", command=ficha_win.destroy, width=15, bg="#004B63", fg="white", font=("Arial", 10, "bold")).pack()

    def _calcular_edad(self, fecha_nacimiento):
        from datetime import datetime
        if not fecha_nacimiento:
            return "Indeterminada"
        
        if isinstance(fecha_nacimiento, str):
            try:
                # Try parsing if it's string format occasionally stored
                fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
            except ValueError:
                return "Formato desconocido"
                
        if isinstance(fecha_nacimiento, datetime):
            hoy = datetime.now()
            edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            return f"{edad} años"
            
        return "Indeterminada"

    def eliminar(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecciona un paciente en la tabla con el ratón primero para poder eliminarlo.")
            return
            
        pac_nombre = self.tree.item(item[0], "values")[1] # 1 es el slot designado para visualizar el nombre en el render value.
        res = self.controller.eliminar_por_nombre(pac_nombre)
        
        if res.get("exito", False) and res.get("paciente_borrado", 0) > 0:
            messagebox.showinfo("Éxito", "Paciente y sus registros asociados eliminados correctamente")
            self.listar()  # Recargar lista tras borrar.
        else:
            messagebox.showwarning("Aviso", "Hubo un error del sistema o no se encontró internamente a este paciente.")

    def listar(self):
        # Limpiar tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        pacientes = self.controller.listar()
        self._poblar_tree(pacientes)

    def ordenar_por_apellido(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        pacientes = self.controller.listar()
        # Ordenar por apellido
        pacientes_ordenados = sorted(
            pacientes, 
            key=lambda p: str(p.get("apellido", "")).lower() if p.get("apellido") else str(p.get("nombre", "")).lower()
        )
        self._poblar_tree(pacientes_ordenados)

    def _poblar_tree(self, lista_pacientes):
        for pac in lista_pacientes:
            fecha_str = pac.get("fechaNacimiento", "").strftime("%Y-%m-%d") if pac.get("fechaNacimiento") else ""
            pac_id = str(pac.get("_id", pac.get("nombre", "")))
            self.tree.insert("", "end", values=(pac_id, pac.get("nombre", ""), pac.get("apellido", ""), pac.get("género", ""), fecha_str))