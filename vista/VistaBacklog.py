import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
#Recuerda que hay solo una Vista para backlog y backlogDetalle
class VistaBacklog:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Gestión de Backlogs")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f4f4f9")

        # Título
        self.titulo_label = tk.Label(self.root, text="Gestión de Backlogs", font=("Arial", 18, "bold"), bg="#2e7d32", fg="white", pady=10)
        self.titulo_label.pack(fill=tk.X)

        # Frame para los campos de entrada
        self.frame_entrada = tk.Frame(self.root, bg="#f4f4f9", padx=10, pady=10)
        self.frame_entrada.pack(fill=tk.X)

        # Crear campos
        self.fecha_entry = self._crear_campo("Fecha:", 0)
        self.fecha_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        self.horometro_entry = self._crear_campo("Horómetro:", 1)
        self.prioridad_combobox = self._crear_combobox("Prioridad:", 2, ["Emergencia", "Urgente", "Corto Plazo", "Largo Plazo"], default_value="Urgente")
        self.ubicacion_combobox = self._crear_combobox("Ubicación:", 3, ["Taller Lima", "Chicama", "Shougang SM", "Cañete", "Huarmey"], default_value="Taller Lima")
        self.recurso_humano_combobox = self._crear_combobox("Recurso Humano:", 4, ["Mecanico", "Electricista", "Soldador", "Gruero", "Rigger"], default_value="Mecanico")
        self.cantidad_recurso_entry = self._crear_campo("Cantidad de Recursos:", 5)
        self.equipo_soporte_combobox = self._crear_combobox("Equipo Soporte:", 6, ["Grua", "Maquina Soldar", "Compresora", "Luminaria", "Montacarga/Manipulador", "Herramientas/Otros"], default_value="Herramientas/Otros")

        # Botones
        self._crear_boton("Agregar Backlog", 7, self.agregar_backlog, "#4CAF50")
        self._crear_boton("Guardar Backlog", None, self.guardar_backlog, "#4CAF50")

        # Tabla para backlogs
        self._crear_tabla()

        # Inicializar lista y cargar datos
        self.backlogs_temporales = []
        self.cargar_backlogs()

    def _crear_campo(self, texto, row):
        tk.Label(self.frame_entrada, text=texto, font=("Arial", 12), bg="#f4f4f9").grid(row=row, column=0, sticky="w", padx=5)
        entry = tk.Entry(self.frame_entrada, font=("Arial", 12), width=40)
        entry.grid(row=row, column=1, padx=5)
        return entry

    def _crear_combobox(self, texto, row, values=None, default_value=None):
        tk.Label(self.frame_entrada, text=texto, font=("Arial", 12), bg="#f4f4f9").grid(row=row, column=0, sticky="w", padx=5)
        combobox = ttk.Combobox(self.frame_entrada, font=("Arial", 12), state="readonly", width=40)
        if values:
            combobox['values'] = values
        if default_value:
            combobox.set(default_value)
        combobox.grid(row=row, column=1, padx=5)
        return combobox

    def _crear_boton(self, texto, row, command, bg_color, pady=0):
        boton = tk.Button(self.root, text=texto, font=("Arial", 12), bg=bg_color, fg="white", command=command)
        boton.pack(pady=pady)
        return boton

    def _crear_tabla(self):
        self.frame_tabla = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        columnas = ("ID", "Fecha", "Horómetro", "Prioridad", "Ubicación", "Recurso Humano", "Cantidad Recursos", "Equipo Soporte")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def cargar_backlogs(self):
        backlogs = self.controlador.listar_backlogs()
        for backlog in backlogs:
            self.tree.insert("", tk.END, values=backlog)

    def agregar_backlog(self):
        fecha = self.fecha_entry.get()
        horometro = self.horometro_entry.get()
        prioridad = self.prioridad_combobox.get()
        ubicacion = self.ubicacion_combobox.get()
        recurso_humano = self.recurso_humano_combobox.get()
        cantidad_recurso = self.cantidad_recurso_entry.get()
        equipo_soporte = self.equipo_soporte_combobox.get()

        if not fecha or not horometro.isdigit() or not cantidad_recurso.isdigit():
            messagebox.showerror("Error", "Por favor, complete todos los campos obligatorios con valores válidos.")
            return

        nuevo_backlog = (fecha, int(horometro), prioridad, ubicacion, recurso_humano, int(cantidad_recurso), equipo_soporte)
        self.backlogs_temporales.append(nuevo_backlog)
        self.tree.insert("", tk.END, values=nuevo_backlog)

    def guardar_backlog(self):
        for backlog in self.backlogs_temporales:
            fecha, horometro, prioridad, ubicacion, recurso_humano, cantidad_recurso, equipo_soporte = backlog
            self.controlador.guardar_backlog(fecha, horometro, prioridad, ubicacion, recurso_humano, cantidad_recurso, equipo_soporte)

        messagebox.showinfo("Éxito", "Backlogs guardados correctamente.")
        self.backlogs_temporales.clear()
        self.tree.delete(*self.tree.get_children())

    def mostrar_backlogs(self):
        self.root.mainloop()

