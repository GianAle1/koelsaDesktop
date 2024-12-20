import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date


class VistaSalida:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Registrar Salida de Productos")
        self.root.geometry("900x600")  # Ajustar el tamaño para más espacio
        self.root.configure(bg="#f4f4f9")

        # Título
        self.titulo_label = tk.Label(
            self.root, text="Registrar Salida de Productos",
            font=("Arial", 18, "bold"), bg="#2e7d32", fg="white", pady=10
        )
        self.titulo_label.pack(fill=tk.X)

        # Frame para los campos de entrada
        self.frame_entrada = tk.Frame(self.root, bg="#f4f4f9", padx=10, pady=10)
        self.frame_entrada.pack(fill=tk.X)

        # Inicializar atributos para entradas
        self.fecha_entry = None
        self.responsable_entry = None
        self.maquinaria_combobox = None
        self.producto_combobox = None
        self.cantidad_entry = None

        # Crear campos
        self.fecha_entry = self._crear_campo("Fecha:", 0)
        self.fecha_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        self.responsable_entry = self._crear_campo("Responsable:", 1)
        self.maquinaria_combobox = self._crear_combobox("Maquinaria:", 2)
        self.producto_combobox = self._crear_combobox("Producto:", 3)
        self.cantidad_entry = self._crear_campo("Cantidad:", 4)

        # Botón para agregar a la lista
        self._crear_boton("Agregar Producto", 5, self.agregar_producto, "#4CAF50")

        # Tabla para productos agregados
        self._crear_tabla()

        # Botón para eliminar producto
        self._crear_boton("Eliminar Producto", None, self.eliminar_producto, "#f44336", pady=10)

        # Botón para guardar la salida
        self._crear_boton("Guardar Salida", None, self.guardar_salida, "#4CAF50", pady=10)

        # Inicializar listas y cargar datos
        self.productos_temporales = []
        self.cargar_maquinarias()
        self.cargar_productos()

    def _crear_campo(self, texto, row):
        """Crea un campo de entrada con una etiqueta."""
        tk.Label(self.frame_entrada, text=texto, font=("Arial", 12), bg="#f4f4f9").grid(row=row, column=0, sticky="w", padx=5)
        entry_var = tk.Entry(self.frame_entrada, font=("Arial", 12), width=40)
        entry_var.grid(row=row, column=1, padx=5)
        return entry_var

    def _crear_combobox(self, texto, row):
        """Crea un combobox con una etiqueta."""
        tk.Label(self.frame_entrada, text=texto, font=("Arial", 12), bg="#f4f4f9").grid(row=row, column=0, sticky="w", padx=5)
        combobox = ttk.Combobox(self.frame_entrada, font=("Arial", 12), state="readonly", width=40)
        combobox.grid(row=row, column=1, padx=5)
        return combobox

    def _crear_boton(self, texto, row, command, bg_color, pady=0):
        """Crea un botón."""
        boton = tk.Button(
            self.root, text=texto, font=("Arial", 12), bg=bg_color, fg="white", command=command
        )
        boton.pack(pady=pady)
        return boton

    def _crear_tabla(self):
        """Crea la tabla para los productos agregados."""
        self.frame_tabla = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas = ("Producto", "Cantidad", "ID Maquinaria")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=10)
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("ID Maquinaria", text="ID Maquinaria")
        self.tree.column("Producto", anchor="center", width=300)
        self.tree.column("Cantidad", anchor="center", width=100)
        self.tree.column("ID Maquinaria", anchor="center", width=150)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def cargar_maquinarias(self):
        maquinarias = self.controlador.listar_maquinarias()
        self.maquinaria_combobox['values'] = [
            f"{maq[0]} - {maq[1]} {maq[2]} ({maq[3]})" for maq in maquinarias
        ] if maquinarias else []

    def cargar_productos(self):
        productos = self.controlador.listar_productos()
        self.producto_combobox['values'] = [producto[2] for producto in productos]

    def agregar_producto(self):
        producto_seleccionado = self.producto_combobox.get()
        cantidad = self.cantidad_entry.get()
        maquinaria_seleccionada = self.maquinaria_combobox.get()

        if not producto_seleccionado or not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Debe seleccionar un producto y una cantidad válida.")
            return

        if not maquinaria_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una maquinaria.")
            return

        idmaquinaria = int(maquinaria_seleccionada.split()[0])  # Suponiendo que el ID está al inicio
        self.productos_temporales.append((producto_seleccionado, int(cantidad), idmaquinaria))
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for producto, cantidad, idmaquinaria in self.productos_temporales:
            self.tree.insert("", tk.END, values=(producto, cantidad, idmaquinaria))

    def eliminar_producto(self):
        selected_item = self.tree.selection()
        if selected_item:
            for item in selected_item:
                values = self.tree.item(item, "values")
                producto, cantidad, idmaquinaria = values[0], int(values[1]), int(values[2])
                self.productos_temporales = [
                    prod for prod in self.productos_temporales if not (
                        prod[0] == producto and prod[1] == cantidad and prod[2] == idmaquinaria)
                ]
                self.tree.delete(item)
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto para eliminar.")

    def guardar_salida(self):
        fecha = self.fecha_entry.get()
        responsable = self.responsable_entry.get()

        if not responsable:
            messagebox.showerror("Error", "Debe ingresar un responsable.")
            return

        if not self.productos_temporales:
            messagebox.showerror("Error", "Debe agregar al menos un producto a la salida.")
            return

        salida_id = self.controlador.guardar_salida(fecha, responsable, self.productos_temporales)
        if salida_id:
            messagebox.showinfo("Éxito", f"Salida registrada con ID: {salida_id}")
            self.productos_temporales = []
            self.actualizar_tabla()
        else:
            messagebox.showerror("Error", "Ocurrió un error al guardar la salida.")