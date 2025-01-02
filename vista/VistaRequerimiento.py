import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

class VistaRequerimiento:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Registrar Requerimiento")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f4f4f9")

        # Título
        self.titulo_label = tk.Label(self.root, text="Registrar Requerimiento", font=("Arial", 18, "bold"), bg="#2e7d32", fg="white", pady=10)
        self.titulo_label.pack(fill=tk.X)

        # Frame para los campos de entrada
        self.frame_entrada = tk.Frame(self.root, bg="#f4f4f9", padx=10, pady=10)
        self.frame_entrada.pack(fill=tk.X)

        # Crear campos
        self.fecha_entry = self._crear_campo("Fecha:", 0)
        self.fecha_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        self.criterio_combobox = self._crear_combobox("Criterio:", 1, ["Programada", "Normal", "Urgente"], default_value="Programada")
        self.producto_combobox = self._crear_combobox("Producto:", 2)
        self.cantidad_entry = self._crear_campo("Cantidad:", 3)
        self.proveedor_combobox = self._crear_combobox("Proveedor:", 4)
        self.uso_combobox = self._crear_combobox("Uso:", 5)
        self.almacen_combobox = self._crear_combobox("Almacén:", 6)
        self.maquinaria_combobox = self._crear_combobox("Maquinaria:", 7)
        self.precio_unitario_entry = self._crear_campo("Precio Unitario:", 8)

        # Botones
        self._crear_boton("Agregar Producto", 9, self.agregar_producto, "#4CAF50")
        self._crear_boton("Guardar Requerimiento", None, self.guardar_requerimiento, "#4CAF50")

        # Label para el total
        self.total_label = tk.Label(self.root, text="Total del Requerimiento: $0.00", font=("Arial", 14, "bold"), bg="#f4f4f9", fg="#000")
        self.total_label.pack(pady=10)

        # Tabla para productos agregados
        self._crear_tabla()

        # Inicializar listas y cargar datos
        self.productos_temporales = []
        self.total_requerimiento = 0.0
        self.cargar_productos()
        self.cargar_proveedores()
        self.cargar_usos()
        self.cargar_almacenes()
        self.cargar_maquinarias()

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
        columnas = ("Producto", "Cantidad", "Proveedor", "Uso", "Almacén", "Maquinaria", "Precio Unitario", "Precio Total")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def cargar_productos(self):
        productos = self.controlador.listar_productos()
        self.producto_combobox['values'] = [f"{prod[1]} - {prod[2]}" for prod in productos]

    def cargar_proveedores(self):
        proveedores = self.controlador.listar_proveedores()
        self.proveedor_combobox['values'] = [f"{prov[1]}" for prov in proveedores]

    def cargar_usos(self):
        usos = self.controlador.listar_usos()
        self.uso_combobox['values'] = [f"{uso[1]}" for uso in usos]

    def cargar_almacenes(self):
        almacenes = self.controlador.listar_almacenes()
        self.almacen_combobox['values'] = [f"{alm[1]}" for alm in almacenes]

    def cargar_maquinarias(self):
        maquinarias = self.controlador.listar_maquinarias()
        self.maquinaria_combobox['values'] = [f"{maq[1]} - {maq[2]} - {maq[3]}" for maq in maquinarias]

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
        """Muestra la ventana de requerimientos."""
        self.root.mainloop()