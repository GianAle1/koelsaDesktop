import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import openpyxl
from datetime import datetime 
class VistaProductos:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Inventario de Productos")
        self.root.geometry("1400x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#e8f4f8")

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

        # Botón para mostrar todas las entradas y salidas
        self.boton_todas_entradas_salidas = tk.Button(
            self.frame_filtros, text="Mostrar Todas las Entradas y Salidas", font=("Arial", 12, "bold"),
            bg="#007ACC", fg="white", command=self.mostrar_todas_entradas_salidas,
            relief="groove", bd=2
        )
        self.boton_todas_entradas_salidas.pack(side=tk.LEFT, padx=10)


        # Frame contenedor para la tabla
        self.frame_tabla = tk.Frame(self.root, bg="white", bd=2, relief="ridge")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas = (
            "ID Producto", "Part Name", "Descripción", "Marca", "Familia",
            "Unidad de Medida", "Cantidad", "Precio", "Código Interno", "Ubicación", "Almacén"
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
        self.tree.column("ID Producto", anchor="center", width=60)
        self.tree.column("Part Name", anchor="center", width=150)
        self.tree.column("Descripción", anchor="w", width=300)
        self.tree.column("Marca", anchor="center", width=120)
        self.tree.column("Familia", anchor="center", width=120)
        self.tree.column("Unidad de Medida", anchor="center", width=120)
        self.tree.column("Cantidad", anchor="center", width=100)
        self.tree.column("Precio", anchor="center", width=100)
        self.tree.column("Código Interno", anchor="center", width=100)
        self.tree.column("Ubicación", anchor="center", width=100)
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
        """Lista los productos desde la base de datos y actualiza la tabla."""
        productos = self.controlador.listar_productos()
        if productos:
            self.actualizar_lista_productos(productos)
        else:
            self.actualizar_lista_productos([])

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
        """Actualiza la lista de productos en la tabla."""
        # Elimina todos los elementos existentes en la tabla
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Inserta los productos actualizados
        for producto in productos:
            valores = tuple(str(valor).replace(",", " ") if valor is not None else "" for valor in producto)
            self.tree.insert("", tk.END, values=valores)

    def mostrar_entradas_salidas(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            producto_id = self.tree.item(selected_item[0])["values"][0]  # ID del producto
            self.abrir_ventana_entradas_salidas(producto_id)

    def abrir_ventana_entradas_salidas(self, producto_id):
        ventana_historial = tk.Toplevel(self.root)
        ventana_historial.title("Historial de Entradas y Salidas del Producto")
        ventana_historial.geometry("1000x500")
        ventana_historial.configure(bg="#f4f4f9")

        tk.Label(
            ventana_historial, text="Historial de Entradas y Salidas del Producto",
            font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", pady=10
        ).pack(fill=tk.X)

        frame_tabla = tk.Frame(ventana_historial, bg="white", bd=2, relief="ridge")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas = ("ID Producto", "Part Name", "Codigo Interno", "Descripción", "Precio Entrada",
                    "Familia", "Tipo", "Fecha", "Documento Ingreso", "Cantidad", "Proveedor", "Detalles", "Responsable")

        tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)

        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)

        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        registros = self.controlador.obtener_historial_producto(producto_id)

        if registros:
            entradas = registros["entradas"]
            salidas = registros["salidas"]

            # ✅ Mostrar las ENTRADAS con `precioEntrada` y `docuIngreso`
            for entrada in entradas:
                idproducto, partname, codigoInterno, descripcion, precio_entrada, nomfamilia, fecha, docu_ingreso, cantidad, proveedor = entrada
                tree.insert("", tk.END, values=(idproducto, partname, codigoInterno, descripcion, precio_entrada, nomfamilia, 
                                                "Entrada", fecha, docu_ingreso, cantidad, proveedor, "-", "-"))

            # ✅ Mostrar las SALIDAS
            for salida in salidas:
                idproducto, partname, codigoInterno, descripcion, precio, nomfamilia, fecha, cantidad, tipo, modelo, marca, responsable = salida
                detalles = f"{tipo} {modelo} {marca}"
                tree.insert("", tk.END, values=(idproducto, partname, codigoInterno, descripcion, precio, nomfamilia, 
                                                "Salida", fecha, "-", cantidad, "-", detalles, responsable))
        else:
            tree.insert("", tk.END, values=("No hay datos", "", "", "", "", "", "", "", "", "", "", "", ""))

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

        headers = [col for col in self.tree["columns"]]
        sheet.append(headers)

        for producto in productos:
            sheet.append(producto)

        workbook.save(filepath)
        messagebox.showinfo("Éxito", f"Datos exportados exitosamente a {filepath}")

    def mostrar_todas_entradas_salidas(self):
        ventana_historial = tk.Toplevel(self.root)
        ventana_historial.title("Todas las Entradas y Salidas")
        ventana_historial.geometry("1200x500")
        ventana_historial.configure(bg="#f4f4f9")

        tk.Label(
            ventana_historial, text="Todas las Entradas y Salidas",
            font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", pady=10
        ).pack(fill=tk.X)

        frame_tabla = tk.Frame(ventana_historial, bg="white", bd=2, relief="ridge")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas = (
            "ID Producto", "Part Name", "Código Interno", "Descripción", "Precio",
            "Familia", "Tipo", "Fecha", "Documento Ingreso", "Cantidad", "Proveedor", "Detalles", "Responsable"
        )

        tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)

        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)

        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        registros = self.controlador.obtener_historial_general()

        if registros:
            entradas = registros["entradas"]
            salidas = registros["salidas"]

            # ✅ Ordenamos por la fecha en orden descendente
            datos_completos = []

            # 🔹 Procesamos las ENTRADAS
            for entrada in entradas:
                idproducto, partname, codigoInterno, descripcion, precio_entrada, nomfamilia, fecha, docu_ingreso, cantidad, proveedor = entrada
                datos_completos.append((
                    idproducto, partname, codigoInterno, descripcion, precio_entrada, 
                    nomfamilia, "Entrada", fecha, docu_ingreso, cantidad, proveedor, "-", "-"
                ))

            # 🔹 Procesamos las SALIDAS
            for salida in salidas:
                idproducto, partname, codigoInterno, descripcion, precio, nomfamilia, fecha, cantidad, tipo, modelo, marca, responsable = salida
                detalles = f"{tipo} {modelo} {marca}"
                datos_completos.append((
                    idproducto, partname, codigoInterno, descripcion, precio, 
                    nomfamilia, "Salida", fecha, "-", cantidad, "-", detalles, responsable
                ))

            # 🔹 Aplicamos ordenación manual por la fecha en orden DESCENDENTE
            datos_completos.sort(key=lambda x: x[7], reverse=True)  # El índice 7 es la columna "Fecha"

            # 🔹 Insertamos los datos ordenados en el Treeview
            for fila in datos_completos:
                tree.insert("", tk.END, values=fila)

        else:
            tree.insert("", tk.END, values=("No hay datos", "", "", "", "", "", "", "", "", "", "", "", ""))

        def exportar_todas_entradas_salidas_a_excel():
            datos = [tree.item(child)["values"] for child in tree.get_children()]
            if not datos:
                messagebox.showwarning("Advertencia", "No hay datos para exportar.")
                return

            # 🔹 Obtener la fecha de hoy en formato YYYY-MM-DD
            fecha_hoy = datetime.today().strftime('%Y-%m-%d')

            # 🔹 Nombre predeterminado del archivo
            default_filename = f"Entradas_Salidas_{fecha_hoy}.xlsx"

            filepath = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Archivos de Excel", "*.xlsx")],
                initialfile=default_filename  # ✅ Se usa la fecha como nombre de archivo por defecto
            )
            if not filepath:
                return

            # Crear archivo Excel
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Entradas y Salidas"

            # Agregar encabezados
            sheet.append(columnas)

            # Agregar datos
            for fila in datos:
                sheet.append(fila)

            # Guardar archivo
            workbook.save(filepath)
            messagebox.showinfo("Éxito", f"Datos exportados exitosamente a {filepath}")

        # 🔹 Asegurar que el botón use la función corregida
        tk.Button(
            ventana_historial, text="Exportar a Excel", font=("Arial", 12), bg="#007ACC", fg="white",
            command=exportar_todas_entradas_salidas_a_excel
        ).pack(pady=10, side=tk.LEFT, padx=10)