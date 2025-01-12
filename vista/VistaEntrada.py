import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import date

class VistaEntrada:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Registrar Entrada de Producto")
        self.root.geometry("800x600")
        self.root.configure(bg="#f4f4f9")

        # Título
        self.titulo_label = tk.Label(
            self.root, text="Registrar Entrada de Producto",
            font=("Arial", 18, "bold"), bg="#4CAF50", fg="white", pady=10
        )
        self.titulo_label.pack(fill=tk.X)

        # Frame para la entrada
        self.frame_entrada = tk.Frame(self.root, bg="#f4f4f9", padx=10, pady=10)
        self.frame_entrada.pack(fill=tk.X)

        # Fecha
        tk.Label(self.frame_entrada, text="Fecha:", font=("Arial", 12), bg="#f4f4f9").grid(row=0, column=0, sticky="w", padx=5)
        self.fecha_entry = tk.Entry(self.frame_entrada, font=("Arial", 12), width=20)
        self.fecha_entry.grid(row=0, column=1, padx=5)
        self.fecha_entry.insert(0, date.today().strftime('%Y-%m-%d'))

        # Producto
        tk.Label(self.frame_entrada, text="Producto:", font=("Arial", 12), bg="#f4f4f9").grid(row=1, column=0, sticky="w", padx=5)
        self.producto_combobox = ttk.Combobox(self.frame_entrada, font=("Arial", 12), state="readonly", width=40)
        self.producto_combobox.grid(row=1, column=1, padx=5)

        # Cantidad
        tk.Label(self.frame_entrada, text="Cantidad:", font=("Arial", 12), bg="#f4f4f9").grid(row=2, column=0, sticky="w", padx=5)
        self.cantidad_entry = tk.Entry(self.frame_entrada, font=("Arial", 12), width=20)
        self.cantidad_entry.grid(row=2, column=1, padx=5)

        # Botón para agregar a la lista temporal
        self.agregar_button = tk.Button(
            self.frame_entrada, text="Agregar", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.agregar_producto
        )
        self.agregar_button.grid(row=3, column=1, sticky="e", pady=10)

        # Tabla para los productos agregados
        self.frame_tabla = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas = ("Producto", "Cantidad")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=10)
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.column("Producto", anchor="center", width=200)
        self.tree.column("Cantidad", anchor="center", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Botón para eliminar producto
        self.eliminar_button = tk.Button(
            self.root, text="Eliminar Producto", font=("Arial", 12), bg="#f44336", fg="white", command=self.eliminar_producto
        )
        self.eliminar_button.pack(pady=10)

        # Botón para guardar la entrada
        self.guardar_button = tk.Button(
            self.root, text="Guardar Entrada", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.guardar_entrada
        )
        self.guardar_button.pack(pady=10)

        # Cargar productos al combobox
        self.cargar_productos()

        # Lista temporal para los productos
        self.productos_temporales = []

    def abrir_ventana_entrada_productos(self):
        ventana_entrada = tk.Toplevel(self.root)  # Usa Toplevel para ventanas secundarias
        ventana_entrada = VistaEntrada(ventana_entrada, self.controlador)

    def eliminar_producto(self):
        # Obtener el producto seleccionado en la tabla
        selected_item = self.tree.selection()
        if selected_item:
            for item in selected_item:
                # Extraer los valores del producto seleccionado
                values = self.tree.item(item, "values")
                producto, cantidad = values[0], int(values[1])

                # Eliminar el producto de la lista temporal
                self.productos_temporales = [
                    prod for prod in self.productos_temporales if not (prod[0] == producto and prod[1] == cantidad)
                ]

                # Eliminar el producto de la tabla visual
                self.tree.delete(item)

            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto para eliminar.")

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

    def guardar_entrada(self):
        fecha = self.fecha_entry.get()
        if not self.productos_temporales:
            messagebox.showerror("Error", "Debe agregar al menos un producto a la entrada.")
            return

        entrada_id = self.controlador.guardar_entrada(fecha, self.productos_temporales)
        if entrada_id:
            messagebox.showinfo("Éxito", f"Entrada registrada con ID: {entrada_id}")
            self.productos_temporales = []
            self.actualizar_tabla()

            # Actualizar la vista de productos
            if hasattr(self.controlador, "vista_productos"):
                self.controlador.vista_productos.listar_productos()
        else:
            messagebox.showerror("Error", "Ocurrió un error al guardar la entrada.")
