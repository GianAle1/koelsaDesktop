import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
from fpdf import FPDF


class VistaSalida:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Registrar Salida de Productos")
        self.root.geometry("1100x750")
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

        # Crear campos
        self.fecha_entry = self._crear_campo("Fecha:", 0)
        self.fecha_entry.insert(0, date.today().strftime('%Y-%m-%d'))

        # Responsable como combobox con datos de la tabla responsable
        self.responsable_combobox = self._crear_combobox("Responsable:", 1)

        self.maquinaria_combobox = self._crear_combobox("Maquinaria:", 2)
        self.producto_combobox = self._crear_combobox("Producto:", 3)
        self.cantidad_entry = self._crear_campo("Cantidad:", 4)
        self.observaciones_entry = self._crear_textarea("Observaciones:", 5)
        # Proyecto como combobox con datos de la tabla proyecto
        self.proyecto_combobox = self._crear_combobox("Proyecto:", 6)

        # Botón para agregar a la lista
        self._crear_boton("Agregar Producto", self.agregar_producto, "#4CAF50")

        # Tabla para productos agregados
        self._crear_tabla()

        # Botón para eliminar producto
        self._crear_boton("Eliminar Producto", self.eliminar_producto, "#f44336", pady=10)

        # Botón para guardar la salida
        self._crear_boton("Guardar Salida", lambda: self.guardar_salida(), "#4CAF50", pady=10)



        # Inicializar listas y cargar datos
        self.productos_temporales = []
        self.cargar_maquinarias()
        self.cargar_productos()
        self.cargar_responsables()  # Cargar responsables en el combobox
        self.cargar_proyectos()


    def _crear_campo(self, texto, row):
        tk.Label(self.frame_entrada, text=texto, font=("Arial", 12), bg="#f4f4f9").grid(row=row, column=0, sticky="w", padx=5)
        entry = tk.Entry(self.frame_entrada, font=("Arial", 12), width=40)
        entry.grid(row=row, column=1, padx=5)
        return entry

    def _crear_combobox(self, texto, row):
        tk.Label(self.frame_entrada, text=texto, font=("Arial", 12), bg="#f4f4f9").grid(row=row, column=0, sticky="w", padx=5)
        combobox = ttk.Combobox(self.frame_entrada, font=("Arial", 12), state="readonly", width=40)
        combobox.grid(row=row, column=1, padx=5)
        return combobox

    def _crear_textarea(self, texto, row):
        tk.Label(self.frame_entrada, text=texto, font=("Arial", 12), bg="#f4f4f9").grid(row=row, column=0, sticky="nw", padx=5)
        textarea = tk.Text(self.frame_entrada, font=("Arial", 12), width=40, height=4, wrap=tk.WORD)
        textarea.grid(row=row, column=1, padx=5, pady=5)
        return textarea

    def _crear_boton(self, texto, command, bg_color, pady=0):
        boton = tk.Button(
            self.root, text=texto, font=("Arial", 12), bg=bg_color, fg="white", command=command
        )
        boton.pack(pady=pady)
        return boton

    def _crear_tabla(self):
        """Crea la tabla para visualizar los productos agregados sin mostrar el ID de la maquinaria."""
        self.frame_tabla = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Se eliminó "ID Maquinaria"
        columnas = ("Producto", "Cantidad", "Precio", "Ubicación", "Maquinaria Destino")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=10)

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=180)  # Ajusta el ancho si es necesario

        self.tree.pack(fill=tk.BOTH, expand=True)


    def cargar_responsables(self):
        """Carga los responsables en el combobox desde la base de datos."""
        try:
            responsables = self.controlador.listar_responsables()
            if responsables:
                self.responsable_combobox["values"] = [
                    f"{resp[0]} - {resp[1]}" for resp in responsables
                ]
            else:
                self.responsable_combobox["values"] = []
        except Exception as e:
            print(f"Error al cargar responsables: {e}")

    def cargar_maquinarias(self):
        """Carga las maquinarias en el combobox desde la base de datos."""
        try:
            maquinarias = self.controlador.listar_maquinarias()
            if maquinarias:
                self.maquinaria_combobox["values"] = [
                    f"{maq[0]} - {maq[1]} - {maq[2]}" for maq in maquinarias
                ]
        except Exception as e:
            print(f"Error al cargar maquinarias: {e}")

    def cargar_productos(self):
        """Carga los productos en el combobox desde la base de datos, incluyendo PartName y Ubicación específica."""
        try:
            productos = self.controlador.listar_productos()
            if productos:
                self.producto_combobox["values"] = [
                    f"{prod[0]} - {prod[1]} ({prod[3]}) - Precio: {float(prod[7]):.2f} - Ubicación: {prod[-2]}"
                    for prod in productos
                ]
            else:
                self.producto_combobox["values"] = []
        except Exception as e:
            print(f"Error al cargar productos: {e}")

    def cargar_proyectos(self):
        """Carga los proyectos en el combobox desde la base de datos."""
        try:
            proyectos = self.controlador.listar_proyectos()  # Llama al controlador
            if proyectos:
                self.proyecto_combobox["values"] = [
                    f"{proy[0]} - {proy[1]} ({proy[2]})" for proy in proyectos  # Formato: "ID - Nombre (Ubicación)"
                ]
            else:
                self.proyecto_combobox["values"] = []
        except Exception as e:
            print(f"Error al cargar proyectos: {e}")


    def agregar_producto(self):
        """Agrega un producto seleccionado a la lista temporal sin mostrar el ID de la maquinaria."""
        producto_seleccionado = self.producto_combobox.get()
        cantidad = self.cantidad_entry.get().strip()
        maquinaria_seleccionada = self.maquinaria_combobox.get()

        if not producto_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un producto.")
            return

        if not maquinaria_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una maquinaria.")
            return

        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Debe ingresar una cantidad válida (número mayor a 0).")
            return

        try:
            # Extraer datos del producto seleccionado
            partes_producto = producto_seleccionado.split(" - ")
            id_producto = int(partes_producto[0].strip())
            nombre_producto = partes_producto[1].strip()

            # Extraer ubicación desde la cadena
            ubicacion_producto = ""
            for parte in partes_producto:
                if "Ubicación" in parte:
                    ubicacion_producto = parte.replace("Ubicación:", "").strip()

            # Extraer datos de la maquinaria
            partes_maquinaria = maquinaria_seleccionada.split(" - ")
            id_maquinaria = int(partes_maquinaria[0].strip())
            maquinaria_destino = partes_maquinaria[2].strip()  # ✅ Ahora toma la serie en lugar del modelo

            # Verificar si el producto ya fue agregado
            for prod in self.productos_temporales:
                if prod["id_producto"] == id_producto and prod["idmaquinaria"] == id_maquinaria:
                    messagebox.showwarning("Advertencia", "Este producto ya ha sido agregado para esta maquinaria.")
                    return

            # Agregar el producto a la lista temporal con el ID de maquinaria oculto
            self.productos_temporales.append({
                "id_producto": id_producto,
                "producto": nombre_producto,
                "cantidad": int(cantidad),
                "precio": 1,  # Si el precio está disponible, reemplazar con el correcto
                "ubicacion": ubicacion_producto,
                "idmaquinaria": id_maquinaria,  # Se almacena en la lista pero no se mostrará
                "maquinaria_destino": maquinaria_destino  # ✅ Ahora almacena la serie de la maquinaria
            })

            self.actualizar_tabla()
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")

        except (ValueError, IndexError) as e:
            messagebox.showerror("Error", f"Ocurrió un error al procesar el producto: {e}")




    def actualizar_tabla(self):
        """Actualiza la tabla de productos agregados sin mostrar el ID de maquinaria."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for producto in self.productos_temporales:
            self.tree.insert("", tk.END, values=(
                producto["producto"], 
                producto["cantidad"], 
                producto["precio"], 
                producto["ubicacion"],  # ✅ Mostramos la ubicación del producto
                producto["maquinaria_destino"]  # ✅ Mostramos la SERIE de la maquinaria en lugar del modelo
            ))



    def eliminar_producto(self):
        selected_item = self.tree.selection()
        if selected_item:
            for item in selected_item:
                self.tree.delete(item)
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto para eliminar.")

    def guardar_salida(self):
        """Guarda la salida de productos en la base de datos y genera automáticamente el reporte PDF."""
        fecha = self.fecha_entry.get()
        responsable = self.responsable_combobox.get()
        proyecto = self.proyecto_combobox.get()
        observaciones = self.observaciones_entry.get("1.0", tk.END).strip()

        # Validaciones
        if not responsable:
            messagebox.showerror("Error", "Debe seleccionar un responsable.")
            return
        if not proyecto:
            messagebox.showerror("Error", "Debe seleccionar un proyecto.")
            return
        if not self.productos_temporales:
            messagebox.showerror("Error", "Debe agregar al menos un producto a la salida.")
            return

        # Extraer ID del responsable y proyecto
        try:
            id_responsable = int(responsable.split(" - ")[0])
            id_proyecto = int(proyecto.split(" - ")[0])  # Extrae el ID del ComboBox
        except ValueError:
            messagebox.showerror("Error", "El formato del responsable o proyecto no es válido.")
            return

        # Extraer solo los valores correctos (idproducto, cantidad, idmaquinaria) para la BD
        productos_para_bd = [
            (prod["id_producto"], prod["cantidad"], prod["idmaquinaria"]) for prod in self.productos_temporales
        ]

        # Llamar al controlador para guardar en la base de datos
        try:
            salida_id = self.controlador.guardar_salida(fecha, id_responsable, id_proyecto, productos_para_bd, observaciones)

            if salida_id:
                # Generar automáticamente el reporte PDF con el nombre del ID de la salida
                self.generar_reporte_pdf(salida_id, fecha, responsable, proyecto, observaciones, self.productos_temporales)

                messagebox.showinfo("Éxito", f"Salida registrada con ID: {salida_id}. Reporte generado correctamente.")
                self.productos_temporales.clear()
                self.actualizar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo guardar la salida en la base de datos.")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar la salida: {e}")
            print(f"Error al guardar salida: {e}")


    def generar_reporte_pdf(self, salida_id, fecha, responsable, proyecto, observaciones, productos):
        """Genera un PDF con la información de la salida de productos y permite seleccionar la ruta de guardado."""
        pdf = FPDF()
        pdf.add_page()

        # Configuración general de la fuente
        pdf.set_font("Arial", size=12)

        # Agregar logo
        try:
            pdf.image("vista/imagen/marca.png", x=170, y=10, w=30)
        except FileNotFoundError:
            print("No se encontró la imagen del logo.")

        # Encabezado de la empresa
        pdf.set_xy(10, 20)
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(0, 10, "KOELSA PERU S.R.L.", ln=True, align="L")
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 10, "RUC: 20529427485", ln=True, align="L")
        pdf.cell(0, 10, "Dirección: Otr. Panamericana Sur Km. 26 Lote. 1", ln=True, align="L")
        pdf.cell(0, 10, "Distrito: Lurín, Lima, Perú", ln=True, align="L")
        pdf.ln(15)

        # Título del reporte
        pdf.set_font("Arial", style="B", size=14)
        pdf.set_text_color(50, 50, 255)
        pdf.cell(0, 10, "REPORTE DE SALIDA DE PRODUCTOS - Taller Lima", ln=True, align="C")
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)

        # Información General
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"ID Salida: {salida_id}", ln=True)
        pdf.cell(0, 10, f"Fecha: {fecha}", ln=True)
        pdf.cell(0, 10, f"Responsable: {responsable}", ln=True)
        pdf.cell(0, 10, f"Proyecto: {proyecto}", ln=True)
        pdf.multi_cell(0, 10, f"Observaciones: {observaciones}")
        pdf.ln(10)

        # Tabla de productos
        pdf.set_font("Arial", style="B", size=12)
        pdf.set_fill_color(220, 220, 220)

        columnas = ["N°", "Producto", "Cantidad", "Precio", "Ubicación", "Maquinaria Destino"]
        anchos = [10, 50, 20, 30, 40, 40]  # Ancho de cada columna

        for col, width in zip(columnas, anchos):
            pdf.cell(width, 10, col, border=1, align="C", fill=True)
        pdf.ln()

        # Agregar productos
        pdf.set_font("Arial", size=10)
        for idx, prod in enumerate(productos, start=1):
            pdf.cell(10, 10, str(idx), border=1, align="C")
            pdf.cell(50, 10, prod["producto"], border=1, align="C")
            pdf.cell(20, 10, str(prod["cantidad"]), border=1, align="C")
            pdf.cell(30, 10, f"{prod.get('precio', 0):.2f}", border=1, align="C")
            pdf.cell(40, 10, prod["ubicacion"], border=1, align="C")
            pdf.cell(40, 10, prod["maquinaria_destino"], border=1, align="C")
            pdf.ln()

        # Espacio y firma del responsable
        pdf.ln(20)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "_________________________", ln=True, align="C")
        pdf.cell(0, 10, "Firma del Responsable", ln=True, align="C")

        # ✅ Mostrar cuadro de diálogo para seleccionar la ruta de guardado
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"salida_{salida_id}.pdf",  # Pre-carga el nombre con el ID
            title="Guardar Reporte de Salida"
        )

        # Si el usuario selecciona una ruta, se guarda el archivo
        if filename:
            try:
                pdf.output(filename)
                messagebox.showinfo("Éxito", f"Reporte guardado correctamente en:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el reporte: {e}")