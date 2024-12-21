import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import openpyxl

class VistaProductos:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Inventario de Productos")
        self.root.geometry("1400x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#e8f4f8")  # Fondo más claro

        # Título estilizado
        self.titulo_label = tk.Label(
            self.root, text="Inventario de Productos",
            font=("Arial", 18, "bold"), bg="#007ACC", fg="white", pady=10
        )
        self.titulo_label.pack(fill=tk.X)

        # Frame para Filtros
        self.frame_filtros = tk.Frame(self.root, bg="#e8f4f8")
        self.frame_filtros.pack(fill=tk.X, padx=10, pady=10)

        # Filtro por familia
        tk.Label(
            self.frame_filtros, text="Filtrar por Familia:",
            font=("Arial", 12, "bold"), bg="#e8f4f8", fg="#333333"
        ).pack(side=tk.LEFT, padx=5)

        self.familia_combobox = ttk.Combobox(
            self.frame_filtros, state="readonly",
            font=("Arial", 12), width=30
        )
        self.familia_combobox.pack(side=tk.LEFT, padx=10)

        # Botón de Filtrar
        self.boton_filtrar = tk.Button(
            self.frame_filtros, text="Filtrar", font=("Arial", 12, "bold"),
            bg="#4CAF50", fg="white", command=self.filtrar_por_familia,
            relief="groove", bd=2
        )
        self.boton_filtrar.pack(side=tk.LEFT, padx=10)

        # Botón de Restablecer
        self.boton_resetear = tk.Button(
            self.frame_filtros, text="Restablecer", font=("Arial", 12, "bold"),
            bg="#f44336", fg="white", command=self.listar_productos,
            relief="groove", bd=2
        )
        self.boton_resetear.pack(side=tk.LEFT, padx=10)

        # Botón de Exportar
        self.boton_exportar = tk.Button(
            self.frame_filtros, text="Exportar a Excel", font=("Arial", 12, "bold"),
            bg="#007ACC", fg="white", command=self.exportar_a_excel,
            relief="groove", bd=2
        )
        self.boton_exportar.pack(side=tk.LEFT, padx=10)

        # Frame contenedor para la tabla
        self.frame_tabla = tk.Frame(self.root, bg="white", bd=2, relief="ridge")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configuración de la tabla
        columnas = (
            "ID", "Part Name", "Descripción", "Marca", "Proveedor", "Familia",
            "Unidad de Medida", "Cantidad", "Precio", "Almacén"
        )
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=20)

        # Estilo de encabezados de la tabla
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="#007ACC")
        style.configure("Treeview", font=("Arial", 11), rowheight=25)

        # Encabezados de la tabla
        for col in columnas:
            self.tree.heading(col, text=col)

        # Configurar las columnas
        self.tree.column("ID", anchor="center", width=60)
        self.tree.column("Part Name", anchor="center", width=150)
        self.tree.column("Descripción", anchor="w", width=300)
        self.tree.column("Marca", anchor="center", width=120)
        self.tree.column("Proveedor", anchor="center", width=150)
        self.tree.column("Familia", anchor="center", width=120)
        self.tree.column("Unidad de Medida", anchor="center", width=120)
        self.tree.column("Cantidad", anchor="center", width=100)
        self.tree.column("Precio", anchor="center", width=100)
        self.tree.column("Almacén", anchor="center", width=150)

        # Scrollbars
        scroll_y = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self.frame_tabla, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Evento para seleccionar producto
        self.tree.bind("<Double-1>", self.mostrar_entradas_salidas)

        # Cargar productos
        self.listar_productos()
        self.cargar_familias()

    def mostrar_inventario(self):
        self.root.mainloop()

    def listar_productos(self):
        productos = self.controlador.listar_productos()
        if productos:
            self.actualizar_lista_productos(productos)

    def cargar_familias(self):
        familias = self.controlador.listar_familias()
        self.familia_combobox["values"] = [familia[1] for familia in familias]
        if familias:
            self.familia_combobox.current(0)

    def filtrar_por_familia(self):
        familia_seleccionada = self.familia_combobox.get()
        productos = self.controlador.listar_productos_por_familia(familia_seleccionada)
        self.actualizar_lista_productos(productos)

    def actualizar_lista_productos(self, productos):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for producto in productos:
            # Convertir los valores a cadenas y reemplazar comas para evitar conflictos
            valores = tuple(str(valor).replace(",", " ") if valor is not None else "" for valor in producto)

            try:
                self.tree.insert("", tk.END, values=valores)
            except Exception as e:
                print(f"Error insertando producto: {producto} - {e}")


    def mostrar_entradas_salidas(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            producto_id = self.tree.item(selected_item[0])["values"][0]  # ID del producto
            self.abrir_ventana_entradas_salidas(producto_id)

    def abrir_ventana_entradas_salidas(self, producto_id):
        """Abre una ventana con el historial de entradas y salidas para un producto."""
        ventana_historial = tk.Toplevel(self.root)
        ventana_historial.title("Historial de Entradas y Salidas")
        ventana_historial.geometry("800x400")
        ventana_historial.configure(bg="#f4f4f9")

        # Título de la ventana
        tk.Label(
            ventana_historial, text="Historial de Entradas y Salidas",
            font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", pady=10
        ).pack(fill=tk.X)

        # Crear un frame para la tabla
        frame_tabla = tk.Frame(ventana_historial, bg="white", bd=2, relief="ridge")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear la tabla
        columnas = ("Tipo", "Fecha", "Cantidad", "Detalles")
        tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)

        # Encabezados de la tabla
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)

        # Scrollbars
        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Obtener registros
        registros = self.controlador.obtener_historial_producto(producto_id)

        # Insertar datos en la tabla
        if registros:
            entradas = registros["entradas"]
            salidas = registros["salidas"]

            # Agregar entradas
            for entrada in entradas:
                fecha, cantidad = entrada
                tree.insert("", tk.END, values=("Entrada", fecha, cantidad, "-"))

            # Agregar salidas
            for salida in salidas:
                fecha, cantidad, tipo, modelo, marca = salida
                detalles = f"{tipo} {modelo} {marca}"
                tree.insert("", tk.END, values=("Salida", fecha, cantidad, detalles))
        else:
            tree.insert("", tk.END, values=("No hay datos", "", "", ""))

        # Botón para cerrar la ventana
        tk.Button(
            ventana_historial, text="Cerrar", font=("Arial", 12), bg="#f44336", fg="white",
            command=ventana_historial.destroy
        ).pack(pady=10)


    def exportar_a_excel(self):
        productos = [self.tree.item(child)["values"] for child in self.tree.get_children()]
        if not productos:
            messagebox.showwarning("Advertencia", "No hay datos para exportar.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos de Excel", "*.xlsx")],
        )
        if not filepath:
            return

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Inventario de Productos"

        # Escribir encabezados
        headers = [col for col in self.tree["columns"]]
        sheet.append(headers)

        # Escribir datos
        for producto in productos:
            sheet.append(producto)

        # Guardar archivo
        workbook.save(filepath)
        messagebox.showinfo("Éxito", f"Datos exportados exitosamente a {filepath}")
