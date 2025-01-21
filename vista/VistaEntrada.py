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

        # Precio
        tk.Label(self.frame_entrada, text="Precio:", font=("Arial", 12), bg="#f4f4f9").grid(row=3, column=0, sticky="w", padx=5)
        self.precio_entry = tk.Entry(self.frame_entrada, font=("Arial", 12), width=20)
        self.precio_entry.grid(row=3, column=1, padx=5)

        # Botón para agregar a la lista temporal
        self.agregar_button = tk.Button(
            self.frame_entrada, text="Agregar", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.agregar_producto
        )
        self.agregar_button.grid(row=4, column=1, sticky="e", pady=10)

        # Tabla para los productos agregados
        self.frame_tabla = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas = ("Producto", "Cantidad", "Precio", "SMCS", "SAP", "ad1", "ad2", "ad3")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=10)

        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("SMCS", text="SMCS")
        self.tree.heading("SAP", text="SAP")
        self.tree.heading("ad1", text="ad1")
        self.tree.heading("ad2", text="ad2")
        self.tree.heading("ad3", text="ad3")

        self.tree.column("Producto", anchor="center", width=200)
        self.tree.column("Cantidad", anchor="center", width=100)
        self.tree.column("Precio", anchor="center", width=100)
        self.tree.column("SMCS", anchor="center", width=100)
        self.tree.column("SAP", anchor="center", width=100)
        self.tree.column("ad1", anchor="center", width=100)
        self.tree.column("ad2", anchor="center", width=100)
        self.tree.column("ad3", anchor="center", width=100)

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

    def cargar_productos(self):
        try:
            productos = self.controlador.listar_productos()
            if productos:
                self.producto_combobox['values'] = [
                    f"{producto[0]} - {producto[1]} - {producto[2]} - {producto[3]}" for producto in productos
                ]
                self.productos_info = {producto[0]: producto for producto in productos}
            else:
                self.producto_combobox['values'] = []
                self.productos_info = {}
                print("No se encontraron productos en la base de datos.")
        except Exception as e:
            print(f"Error al cargar productos: {e}")

    def agregar_producto(self):
        producto_seleccionado = self.producto_combobox.get()
        cantidad = self.cantidad_entry.get()
        precio = self.precio_entry.get()

        if not producto_seleccionado or not cantidad.isdigit() or int(cantidad) <= 0 or not precio.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Debe seleccionar un producto, ingresar una cantidad válida y un precio válido.")
            return

        id_producto = int(producto_seleccionado.split(" - ")[0])
        smcs = self.productos_info[id_producto][4]
        sap = self.productos_info[id_producto][5]

        self.productos_temporales.append((id_producto, int(cantidad), float(precio), smcs, sap))
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for id_producto, cantidad, precio, smcs, sap in self.productos_temporales:
            self.tree.insert("", tk.END, values=(id_producto, cantidad, f"{precio:.2f}", smcs, sap))

    def guardar_entrada(self):
        fecha = self.fecha_entry.get()
        if not self.productos_temporales:
            messagebox.showerror("Error", "Debe agregar al menos un producto a la entrada.")
            return

        try:
            # Llama al controlador para guardar la entrada y actualizar los precios
            exito = self.controlador.guardar_entrada(fecha, self.productos_temporales)
            if exito:
                messagebox.showinfo("Éxito", "Entrada registrada y precios actualizados correctamente.")
                self.productos_temporales = []  # Limpia la lista temporal
                self.actualizar_tabla()  # Refresca la tabla
            else:
                messagebox.showerror("Error", "Ocurrió un error al guardar la entrada.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar la entrada: {e}")

    def eliminar_producto(self):
        selected_item = self.tree.selection()
        if selected_item:
            for item in selected_item:
                values = self.tree.item(item, "values")
                id_producto, cantidad, precio = values[0], int(values[1]), float(values[2])

                # Eliminar el producto de la lista temporal
                self.productos_temporales = [
                    prod for prod in self.productos_temporales if not (prod[0] == int(id_producto) and prod[1] == cantidad and prod[2] == precio)
                ]
                self.tree.delete(item)

            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto para eliminar.")
