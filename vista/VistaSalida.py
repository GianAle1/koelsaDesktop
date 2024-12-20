import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

class VistaSalida:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Registrar Salida de Productos")
        self.root.geometry("800x600")
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

        # Fecha
        tk.Label(self.frame_entrada, text="Fecha:", font=("Arial", 12), bg="#f4f4f9").grid(row=0, column=0, sticky="w", padx=5)
        self.fecha_entry = tk.Entry(self.frame_entrada, font=("Arial", 12), width=20)
        self.fecha_entry.grid(row=0, column=1, padx=5)
        self.fecha_entry.insert(0, date.today().strftime('%Y-%m-%d'))

        # Responsable
        tk.Label(self.frame_entrada, text="Responsable:", font=("Arial", 12), bg="#f4f4f9").grid(row=1, column=0, sticky="w", padx=5)
        self.responsable_entry = tk.Entry(self.frame_entrada, font=("Arial", 12), width=40)
        self.responsable_entry.grid(row=1, column=1, padx=5)

        # Maquinaria
        tk.Label(self.frame_entrada, text="Maquinaria:", font=("Arial", 12), bg="#f4f4f9").grid(row=2, column=0, sticky="w", padx=5)
        self.maquinaria_combobox = ttk.Combobox(self.frame_entrada, font=("Arial", 12), state="readonly", width=40)
        self.maquinaria_combobox.grid(row=2, column=1, padx=5)

        # Producto
        tk.Label(self.frame_entrada, text="Producto:", font=("Arial", 12), bg="#f4f4f9").grid(row=3, column=0, sticky="w", padx=5)
        self.producto_combobox = ttk.Combobox(self.frame_entrada, font=("Arial", 12), state="readonly", width=40)
        self.producto_combobox.grid(row=3, column=1, padx=5)

        # Cantidad
        tk.Label(self.frame_entrada, text="Cantidad:", font=("Arial", 12), bg="#f4f4f9").grid(row=4, column=0, sticky="w", padx=5)
        self.cantidad_entry = tk.Entry(self.frame_entrada, font=("Arial", 12), width=20)
        self.cantidad_entry.grid(row=4, column=1, padx=5)

        # Botón para agregar a la lista
        self.agregar_button = tk.Button(
            self.frame_entrada, text="Agregar Producto", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.agregar_producto
        )
        self.agregar_button.grid(row=5, column=1, sticky="e", pady=10)

        # Tabla para productos agregados
        self.frame_tabla = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas = ("Producto", "Cantidad")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=10)
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.column("Producto", anchor="center", width=300)
        self.tree.column("Cantidad", anchor="center", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Botón para eliminar producto
        self.eliminar_button = tk.Button(
            self.root, text="Eliminar Producto", font=("Arial", 12), bg="#f44336", fg="white", command=self.eliminar_producto
        )
        self.eliminar_button.pack(pady=10)

        # Botón para guardar la salida
        self.guardar_button = tk.Button(
            self.root, text="Guardar Salida", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.guardar_salida
        )
        self.guardar_button.pack(pady=10)

        # Cargar datos iniciales
        self.productos_temporales = []
        self.cargar_maquinarias()
        self.cargar_productos()

   # vista/VistaSalida.py
    def cargar_maquinarias(self):
        """Carga las maquinarias en el combobox."""
        maquinarias = self.controlador.listar_maquinarias()
        if maquinarias:
            self.maquinaria_combobox['values'] = [
                f"{maq[0]} - {maq[1]} {maq[2]} ({maq[3]})" for maq in maquinarias
            ]
        else:
            self.maquinaria_combobox['values'] = []

    def cargar_productos(self):
        productos = self.controlador.listar_productos()
        self.producto_combobox['values'] = [producto[2] for producto in productos]

    def agregar_producto(self):
        producto_seleccionado = self.producto_combobox.get()
        cantidad = self.cantidad_entry.get()

        if not producto_seleccionado or not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Debe seleccionar un producto y una cantidad válida.")
            return

        self.productos_temporales.append((producto_seleccionado, int(cantidad)))
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for producto, cantidad in self.productos_temporales:
            self.tree.insert("", tk.END, values=(producto, cantidad))

    def eliminar_producto(self):
        selected_item = self.tree.selection()
        if selected_item:
            for item in selected_item:
                values = self.tree.item(item, "values")
                producto, cantidad = values[0], int(values[1])
                self.productos_temporales = [
                    prod for prod in self.productos_temporales if not (prod[0] == producto and prod[1] == cantidad)
                ]
                self.tree.delete(item)
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto para eliminar.")

    def guardar_salida(self):
        fecha = self.fecha_entry.get()
        responsable = self.responsable_entry.get()
        maquinaria = self.maquinaria_combobox.get()

        if not maquinaria or not responsable:
            messagebox.showerror("Error", "Debe seleccionar una maquinaria y un responsable.")
            return

        if not self.productos_temporales:
            messagebox.showerror("Error", "Debe agregar al menos un producto a la salida.")
            return

        idmaquinaria = int(maquinaria.split()[0])  # Suponiendo que el ID está al inicio
        salida_id = self.controlador.guardar_salida(idmaquinaria, fecha, responsable, self.productos_temporales)
        if salida_id:
            messagebox.showinfo("Éxito", f"Salida registrada con ID: {salida_id}")
            self.productos_temporales = []
            self.actualizar_tabla()
        else:
            messagebox.showerror("Error", "Ocurrió un error al guardar la salida.")
