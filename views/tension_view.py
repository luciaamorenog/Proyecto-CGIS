import tkinter as tk
from tkinter import ttk, messagebox
from controladores.tension_controller import TensionController

class TensionView(tk.Frame):
    def __init__(self, parent, db, paciente_id=None, on_volver=None, on_volver_inicio=None, on_ir_alta_tension=None):
        super().__init__(parent, bg="#18708C")
        self.controller = TensionController(db)
        self.paciente_id_filtro = paciente_id
        self.on_volver = on_volver
        self.on_volver_inicio = on_volver_inicio
        self.on_ir_alta_tension = on_ir_alta_tension
        
        tk.Label(self, text="GESTIÓN DE TENSIÓN ARTERIAL", font=("Arial", 14, "bold"), bg="#004B63", fg="white").pack(pady=10, fill="x")

        # Botones de Acción
        btn_frame = tk.Frame(self, bg="#18708C")
        btn_frame.pack(pady=10)

        if self.on_ir_alta_tension:
            tk.Button(btn_frame, text="➕ Añadir Tensión", bg="green", fg="white", font=("Arial", 10, "bold"),
                      command=lambda: self.on_ir_alta_tension(self.paciente_id_filtro)).grid(row=0, column=0, padx=5)
        
        tk.Button(btn_frame, text="🗑️ Baja (elimina vistas)", bg="red", fg="white", font=("Arial", 10, "bold"), 
                  command=self.eliminar).grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text="🔄 Refrescar Listado", command=self.listar).grid(row=0, column=2, padx=5)
        
        if self.on_volver:
            tk.Button(btn_frame, text="Volver a Pacientes", bg="gray", fg="white", 
                      command=self.on_volver).grid(row=0, column=3, padx=5)
                      
        if self.on_volver_inicio:
            tk.Button(btn_frame, text="🏠 Inicio", bg="gray", fg="white", 
                      command=self.on_volver_inicio).grid(row=0, column=4, padx=5)

        # Lista de tensiones
        self.tree = ttk.Treeview(self, columns=("ID Pac", "Sist", "Diast", "Fecha", "Valoración"), show="headings", displaycolumns=("Sist", "Diast", "Fecha", "Valoración"))
        self.tree.heading("ID Pac", text="ID Paciente")
        self.tree.heading("Sist", text="Sistólica")
        self.tree.heading("Diast", text="Diastólica")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Valoración", text="Valoración")
        self.tree.pack(fill="both", expand=True, pady=10)
        
        # Cargar lista inicialmente
        self.listar()

    def eliminar(self):
        item = self.tree.selection()
        if not item:
             messagebox.showwarning("Aviso", "Seleccione un registro en la tabla")
             return
             
        # El ID de tensión está en el primer índice o podemos buscar por idPaciente si la lógica era "eliminar_todas"
        if self.paciente_id_filtro:
             res = self.controller.eliminar_por_paciente(self.paciente_id_filtro)
             if res and res.deleted_count > 0:
                 messagebox.showinfo("Éxito", f"{res.deleted_count} registros eliminados")
                 self.listar()
             else:
                 messagebox.showwarning("Aviso", "No se encontraron registros del paciente filtrado")
        else:
             # Necesitamos algo robusto si no hay filtro (borrar individualmente). 
             # Pero the original codebase always deleted by id_paciente from entry box. 
             messagebox.showwarning("Aviso", "Para eliminar registros, debe hacerlo filtrando por paciente primero.")


    def listar(self):
        # Limpiar tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if self.paciente_id_filtro:
            self.tensiones_actuales = self.controller.listar_por_paciente(self.paciente_id_filtro)
        else:
            self.tensiones_actuales = self.controller.listar()
            
        for idx, ten in enumerate(self.tensiones_actuales):
            fecha_str = ten.get("fecha", "").strftime("%Y-%m-%d %H:%M:%S") if ten.get("fecha") else ""
            self.tree.insert("", "end", iid=str(idx), values=(ten.get("idPaciente", ""), ten.get("sistolica", ""), ten.get("diastolica", ""), fecha_str, ten.get("valoracion", "")))