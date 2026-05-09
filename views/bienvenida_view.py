import tkinter as tk

class BienvenidaView(tk.Frame):
    def __init__(self, parent, on_ir_pacientes, on_ir_tensiones):
        super().__init__(parent, bg="#18708C")
        
        # Etiqueta de bienvenida central
        lbl_titulo = tk.Label(self, text="Bienvenido al Sistema Médico", font=("Arial", 22, "bold"), bg="#18708C", fg="white")
        lbl_titulo.pack(pady=(120, 50)) 

        # Contenedor de botones
        frame_botones = tk.Frame(self, bg="#18708C")
        frame_botones.pack()

        btn_pacientes = tk.Button(frame_botones, text="🏢 Gestión de Pacientes", font=("Arial", 14, "bold"), 
                                  bg="#004B63", fg="white", width=25, height=2, 
                                  command=on_ir_pacientes)
        btn_pacientes.pack(pady=15)

        btn_tensiones = tk.Button(frame_botones, text="❤️ Gestión de Tensiones", font=("Arial", 14, "bold"), 
                                  bg="#004B63", fg="white", width=25, height=2, 
                                  command=on_ir_tensiones)
        btn_tensiones.pack(pady=15)
