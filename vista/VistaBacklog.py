import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date


class VistaBacklog:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Gestión de Backlogs")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f4f4f9")

        # Título
        self.titulo_label = tk.Label(
            self.root,
            text="Registrar Backlog",
            font=("Arial", 18, "bold"),
            bg="#2e7d32",
            fg="white",
            pady=10,
        )
        self.titulo_label.pack(fill=tk.X)

        # Frame principal
        self.main_frame = tk.Frame(self.root, bg="#f4f4f9", padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame izquierdo: Información general
        self.frame_general = tk.LabelFrame(
            self.main_frame, text="Información General", bg="#f4f4f9", font=("Arial", 14)
        )
        self.frame_general.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame derecho: Detalles del producto
        self.frame_detalles = tk.LabelFrame(
            self.main_frame, text="Detalles del Producto", bg="#f4f4f9", font=("Arial", 14)
        )
        self.frame_detalles.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Frame tabla
        self.frame_tabla = tk.LabelFrame(
            self.main_frame, text="Lista de Detalles", bg="#f4f4f9", font=("Arial", 14)
        )
        self.frame_tabla.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Configuración de columnas
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        # Campos de información general
        self.fecha_entry = self._crear_campo(self.frame_general, "Fecha:", 0)
        self.fecha_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.horometro_entry = self._crear_campo(self.frame_general, "Horómetro:", 1)
        self.prioridad_combobox = self._crear_combobox(
            self.frame_general,
            "Prioridad:",
            2,
            ["Emergencia", "Urgente", "Corto Plazo", "Largo Plazo"],
            default_value="Urgente",
        )
        self.ubicacion_combobox = self._crear_combobox(
            self.frame_general,
            "Ubicación:",
            3,
            ["Taller Lima", "Chicama", "Shougang SM", "Cañete", "Huarmey"],  # Sin errores
            default_value="Taller Lima"
        )
        self.recurso_humano_combobox = self._crear_combobox(
            self.frame_general,
            "Recurso Humano:",
            4,
            ["Mecanico", "Electricista", "Soldador", "Gruero", "Rigger"],
            default_value="Mecanico",
        )
        self.cantidad_recurso_entry = self._crear_campo(
            self.frame_general, "Cantidad de Recursos:", 5
        )
        self.equipo_soporte_combobox = self._crear_combobox(
            self.frame_general,
            "Equipo Soporte:",
            6,
            ["Grua", "Maquina Soldar", "Compresora", "Luminaria", "Montacarga/Manipulador", "Herramientas/Otros"],
            default_value="Herramientas/Otros",
        )
        self.detalle_text = self._crear_textarea(self.frame_general, "Detalle:", 7)
        self.hora_entry = self._crear_campo(self.frame_general, "Horas:", 8)
        self.elaborado_por_entry = self._crear_campo(self.frame_general, "Elaborado por:", 9)
        self.revisado_por_entry = self._crear_campo(self.frame_general, "Revisado por:", 10)
        self.aprobado_por_entry = self._crear_campo(self.frame_general, "Aprobado por:", 11)

        # Campos de detalles del producto
        self.smcs_entry = self._crear_campo(self.frame_detalles, "SMCS:", 0)
        self.producto_combobox = self._crear_combobox(self.frame_detalles, "Producto:", 1)
        self.marca_combobox = self._crear_combobox(self.frame_detalles, "Marca:", 2)
        self.detalle_producto_text = self._crear_textarea(
            self.frame_detalles, "Detalle del Producto:", 3
        )
        self.precio_entry = self._crear_campo(self.frame_detalles, "Precio:", 4)
        self.cantidad_necesaria_entry = self._crear_campo(
            self.frame_detalles, "Cantidad Necesaria:", 5
        )
        self.stock_entry = self._crear_campo(self.frame_detalles, "Stock:", 6)

        # Botones
        self.boton_agregar_detalle = tk.Button(
            self.main_frame,
            text="Agregar Detalle",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self.agregar_detalle,
        )
        self.boton_agregar_detalle.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
        self.boton_guardar_backlog = tk.Button(
            self.main_frame,
            text="Guardar Backlog",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self.guardar_backlog,
        )
        self.boton_guardar_backlog.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

        # Tabla para los detalles
        self._crear_tabla()

        # Inicializar listas y cargar datos
        self.detalles_temporales = []
        self.cargar_productos()
        self.cargar_marcas()

    def _crear_campo(self, frame, texto, row):
        tk.Label(frame, text=texto, font=("Arial", 12), bg="#f4f4f9").grid(row=row, column=0, sticky="w", padx=5)
        entry = tk.Entry(frame, font=("Arial", 12), width=30)
        entry.grid(row=row, column=1, padx=5, pady=2)
        return entry

    def _crear_combobox(self, frame, texto, row, values=None, default_value=None):
        tk.Label(frame, text=texto, font=("Arial", 12), bg="#f4f4f9").grid(row=row, column=0, sticky="w", padx=5)
        combobox = ttk.Combobox(frame, font=("Arial", 12), state="readonly", width=28)
        if values:
            combobox['values'] = values
        if default_value:
            combobox.set(default_value)
        combobox.grid(row=row, column=1, padx=5, pady=2)
        return combobox

    def _crear_textarea(self, frame, texto, row):
        tk.Label(frame, text=texto, font=("Arial", 12), bg="#f4f4f9").grid(row=row, column=0, sticky="nw", padx=5)
        text = tk.Text(frame, font=("Arial", 12), width=30, height=4)
        text.grid(row=row, column=1, padx=5, pady=2)
        return text

    def _crear_tabla(self):
        columnas = (
            "SMCS",
            "Producto",
            "Marca",
            "Detalle",
            "Precio",
            "Cantidad Necesaria",
            "Stock",
        )
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def cargar_productos(self):
        productos = self.controlador.listar_productos()
        self.producto_combobox['values'] = [f"{prod[0]} - {prod[1]} - {prod[2]}" for prod in productos]

    def cargar_marcas(self):
        marcas = self.controlador.listar_marcas()
        self.marca_combobox['values'] = [f"{marca[0]} - {marca[1]}" for marca in marcas]

    def agregar_detalle(self):
        smcs = self.smcs_entry.get()
        producto = self.producto_combobox.get()
        marca = self.marca_combobox.get()
        detalle = self.detalle_producto_text.get("1.0", tk.END).strip()
        precio = self.precio_entry.get()
        cantidad_necesaria = self.cantidad_necesaria_entry.get()
        stock = self.stock_entry.get()

        # Validar campos obligatorios
        if not all([smcs, producto, marca, detalle, precio, cantidad_necesaria, stock]):
            messagebox.showerror("Error", "Todos los campos de detalle son obligatorios.")
            return

        # Validar valores numéricos
        try:
            float(precio)
            int(cantidad_necesaria)
            int(stock)
        except ValueError:
            messagebox.showerror("Error", "Precio, cantidad necesaria y stock deben ser números válidos.")
            return

        # Crear el detalle como un diccionario
        nuevo_detalle = {
            "smcs": smcs,
            "idproducto": producto.split(" - ")[0],
            "idmarca": marca.split(" - ")[0],
            "detalle": detalle,
            "precio": precio,
            "necesita": cantidad_necesaria,
            "stock": stock
        }

        self.detalles_temporales.append(nuevo_detalle)  # Agregar como diccionario
        self.tree.insert("", tk.END, values=(smcs, producto, marca, detalle, precio, cantidad_necesaria, stock))


    def guardar_backlog(self):
        backlog_data = {
            "fecha": self.fecha_entry.get(),
            "horometro": self.horometro_entry.get(),
            "prioridad": self.prioridad_combobox.get(),
            "ubicacion": self.ubicacion_combobox.get(),
            "detalle": self.detalle_text.get("1.0", tk.END).strip(),
            "hora": self.hora_entry.get(),
            "recurso_humano": self.recurso_humano_combobox.get(),
            "cantidad_recurso": self.cantidad_recurso_entry.get(),
            "equipo_soporte": self.equipo_soporte_combobox.get(),
            "elaborado_por": self.elaborado_por_entry.get(),
            "revisado_por": self.revisado_por_entry.get(),
            "aprobado_por": self.aprobado_por_entry.get(),
        }

        if not all(backlog_data.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios para el backlog.")
            return

        id_backlog = self.controlador.guardar_backlog(backlog_data, self.detalles_temporales)
        if id_backlog:
            messagebox.showinfo("Éxito", f"Backlog registrado con ID: {id_backlog}")
            self.detalles_temporales = []
            self.tree.delete(*self.tree.get_children())
        else:
            messagebox.showerror("Error", "No se pudo registrar el backlog.")

    def mostrar_backlogs(self):
        """Mantiene la ventana de Backlogs en ejecución."""
        self.root.mainloop()
