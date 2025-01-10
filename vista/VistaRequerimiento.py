import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

class VistaRequerimiento:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Registrar Requerimiento")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f4f4f9")

        # Título
        self.titulo_label = tk.Label(
            self.root, text="Registrar Requerimiento", font=("Arial", 18, "bold"),
            bg="#2e7d32", fg="white", pady=10
        )
        self.titulo_label.pack(fill=tk.X)

        # Frame principal para contener dos columnas
        self.main_frame = tk.Frame(self.root, bg="#f4f4f9", padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame izquierdo: Información general
        self.left_frame = tk.Frame(self.main_frame, bg="#f4f4f9")
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame derecho: Detalle del producto
        self.right_frame = tk.Frame(self.main_frame, bg="#f4f4f9")
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        # Información general
        tk.Label(self.left_frame, text="Información General", font=("Arial", 14, "bold"), bg="#f4f4f9").grid(row=0, column=0, columnspan=2, pady=10)

        self.fecha_entry = self._crear_campo(self.left_frame, "Fecha:", 1)
        self.fecha_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        self.criterio_combobox = self._crear_combobox(self.left_frame, "Criterio:", 2, ["Programada", "Normal", "Urgente"], default_value="Programada")

        # Detalle del producto
        tk.Label(self.right_frame, text="Detalle del Producto", font=("Arial", 14, "bold"), bg="#f4f4f9").grid(row=0, column=0, columnspan=2, pady=10)

        self.producto_combobox = self._crear_combobox(self.right_frame, "Producto:", 1)
        self.cantidad_entry = self._crear_campo(self.right_frame, "Cantidad:", 2)
        self.precio_unitario_entry = self._crear_campo(self.right_frame, "Precio Unitario:", 3)
        self.proveedor_combobox = self._crear_combobox(self.right_frame, "Proveedor:", 4)
        self.uso_combobox = self._crear_combobox(self.right_frame, "Uso:", 5)
        self.almacen_combobox = self._crear_combobox(self.right_frame, "Almacén:", 6)
        self.maquinaria_combobox = self._crear_combobox(self.right_frame, "Maquinaria:", 7)

        # Botones de acción
        self.action_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.action_frame.pack(fill=tk.X, pady=10)

        self._crear_boton("Agregar Producto", self.action_frame, self.agregar_producto, "#4CAF50", 0)
        self._crear_boton("Guardar Requerimiento", self.action_frame, self.guardar_requerimiento, "#2e7d32", 1)

        # Tabla de productos agregados
        self.table_frame = tk.Frame(self.root, bg="white", bd=2, relief="ridge")
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columnas = ("Producto", "Cantidad", "Proveedor", "Uso", "Almacén", "Maquinaria", "Precio Unitario", "Precio Total")
        self.tree = ttk.Treeview(self.table_frame, columns=columnas, show="headings", height=10)

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Total del requerimiento
        self.total_label = tk.Label(self.root, text="Total del Requerimiento: $0.00", font=("Arial", 14, "bold"), bg="#f4f4f9", fg="#000")
        self.total_label.pack(pady=10)

        # Inicializar listas y cargar datos
        self.productos_temporales = []
        self.total_requerimiento = 0.0
        self.cargar_productos()
        self.cargar_proveedores()
        self.cargar_usos()
        self.cargar_almacenes()
        self.cargar_maquinarias()

    def _crear_campo(self, frame, texto, row):
        tk.Label(frame, text=texto, font=("Arial", 12), bg="#f4f4f9").grid(row=row, column=0, sticky="w", padx=5, pady=5)
        entry = tk.Entry(frame, font=("Arial", 12), width=30)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    def _crear_combobox(self, frame, texto, row, values=None, default_value=None):
        tk.Label(frame, text=texto, font=("Arial", 12), bg="#f4f4f9").grid(row=row, column=0, sticky="w", padx=5, pady=5)
        combobox = ttk.Combobox(frame, font=("Arial", 12), state="readonly", width=28)
        if values:
            combobox['values'] = values
        if default_value:
            combobox.set(default_value)
        combobox.grid(row=row, column=1, padx=5, pady=5)
        return combobox

    def _crear_boton(self, texto, frame, command, bg_color, col):
        boton = tk.Button(frame, text=texto, font=("Arial", 12), bg=bg_color, fg="white", command=command)
        boton.grid(row=0, column=col, padx=10)

    def cargar_productos(self):
        productos = self.controlador.listar_productos()
        self.producto_combobox['values'] = [f"{prod[0]} - {prod[1]} - {prod[2]}" for prod in productos]

    def cargar_proveedores(self):
        proveedores = self.controlador.listar_proveedores()
        self.proveedor_combobox['values'] = [f"{prov[0]} - {prov[1]}" for prov in proveedores]

    def cargar_usos(self):
        usos = self.controlador.listar_usos()
        self.uso_combobox['values'] = [f"{uso[0]} - {uso[1]}" for uso in usos]

    def cargar_almacenes(self):
        almacenes = self.controlador.listar_almacenes()
        self.almacen_combobox['values'] = [f"{alm[0]} - {alm[1]}" for alm in almacenes]

    def cargar_maquinarias(self):
        maquinarias = self.controlador.listar_maquinarias()
        self.maquinaria_combobox['values'] = [f"{maq[0]} - {maq[1]} - {maq[2]} - {maq[3]}" for maq in maquinarias]

    def agregar_producto(self):
        producto = self.producto_combobox.get()
        cantidad = self.cantidad_entry.get()
        proveedor = self.proveedor_combobox.get()
        uso = self.uso_combobox.get()
        almacen = self.almacen_combobox.get()
        maquinaria = self.maquinaria_combobox.get()
        precio_unitario = self.precio_unitario_entry.get()

        if not producto or not cantidad.isdigit() or not proveedor or not uso or not almacen or not maquinaria or not precio_unitario:
            messagebox.showerror("Error", "Todos los campos son obligatorios y válidos.")
            return

        precio_total = int(cantidad) * float(precio_unitario)
        self.productos_temporales.append((producto, int(cantidad), proveedor, uso, almacen, maquinaria, float(precio_unitario), precio_total))
        self.total_requerimiento += precio_total
        self.actualizar_tabla()
        self.actualizar_total_label()

    def actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for prod in self.productos_temporales:
            self.tree.insert("", tk.END, values=prod)

    def actualizar_total_label(self):
        self.total_label.config(text=f"Total del Requerimiento: ${self.total_requerimiento:.2f}")

    def guardar_requerimiento(self):
        fecha = self.fecha_entry.get()
        criterio = self.criterio_combobox.get()

        if not criterio:
            messagebox.showerror("Error", "El criterio es obligatorio.")
            return

        productos_para_bd = [
            {
                "id_producto": prod[0].split(" - ")[0],
                "cantidad": prod[1],
                "id_proveedor": prod[2].split(" - ")[0],
                "id_uso": prod[3].split(" - ")[0],
                "id_almacen": prod[4].split(" - ")[0],
                "id_maquinaria": prod[5].split(" - ")[0],
                "precio_unitario": prod[6],
                "precio_total": prod[7],
            }
            for prod in self.productos_temporales
        ]

        id_requerimiento = self.controlador.guardar_requerimiento(fecha, criterio, productos_para_bd)
        if id_requerimiento:
            messagebox.showinfo("Éxito", f"Requerimiento registrado con ID: {id_requerimiento}")
            self.productos_temporales = []
            self.total_requerimiento = 0.0
            self.actualizar_tabla()
            self.actualizar_total_label()
        else:
            messagebox.showerror("Error", "No se pudo registrar el requerimiento.")

    def mostrar_requerimiento(self):
        self.root.mainloop()
