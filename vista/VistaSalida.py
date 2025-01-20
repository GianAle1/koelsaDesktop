import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from fpdf import FPDF
from tkinter import filedialog

class VistaSalida:
        def __init__(self, root, controlador):
            self.root = root
            self.controlador = controlador
            self.root.title("Registrar Salida de Productos")
            self.root.geometry("1100x750")  # Aumentar tamaño para más espacio
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
            self.responsable_entry = self._crear_campo("Responsable:", 1)
            self.maquinaria_combobox = self._crear_combobox("Maquinaria:", 2)
            self.producto_combobox = self._crear_combobox("Producto:", 3)
            self.cantidad_entry = self._crear_campo("Cantidad:", 4)
            self.observaciones_entry = self._crear_textarea("Observaciones:", 5)

            # Botón para agregar a la lista
            self._crear_boton("Agregar Producto", 6, self.agregar_producto, "#4CAF50")

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
            entry = tk.Entry(self.frame_entrada, font=("Arial", 12), width=40)
            entry.grid(row=row, column=1, padx=5)
            return entry

        def _crear_combobox(self, texto, row):
            """Crea un combobox con una etiqueta."""
            tk.Label(self.frame_entrada, text=texto, font=("Arial", 12), bg="#f4f4f9").grid(row=row, column=0, sticky="w", padx=5)
            combobox = ttk.Combobox(self.frame_entrada, font=("Arial", 12), state="readonly", width=40)
            combobox.grid(row=row, column=1, padx=5)
            return combobox

        def _crear_textarea(self, texto, row):
            """Crea un campo de texto grande para observaciones."""
            tk.Label(self.frame_entrada, text=texto, font=("Arial", 12), bg="#f4f4f9").grid(row=row, column=0, sticky="nw", padx=5)
            textarea = tk.Text(self.frame_entrada, font=("Arial", 12), width=40, height=4, wrap=tk.WORD)
            textarea.grid(row=row, column=1, padx=5, pady=5)
            return textarea

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

            columnas = ("Producto", "Cantidad", "ID Maquinaria", "Maquinaria Destino")
            self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=10)
            self.tree.heading("Producto", text="Producto")
            self.tree.heading("Cantidad", text="Cantidad")
            self.tree.heading("ID Maquinaria", text="ID Maquinaria")
            self.tree.heading("Maquinaria Destino", text="Maquinaria Destino")
            self.tree.column("Producto", anchor="center", width=200)
            self.tree.column("Cantidad", anchor="center", width=100)
            self.tree.column("ID Maquinaria", anchor="center", width=150)
            self.tree.column("Maquinaria Destino", anchor="center", width=200)
            self.tree.pack(fill=tk.BOTH, expand=True)
        

        def cargar_maquinarias(self):
            maquinarias = self.controlador.listar_maquinarias()
            self.maquinaria_combobox['values'] = [
                f"{maq[0]} - {maq[1]} {maq[2]} ({maq[3]})" for maq in maquinarias
            ] if maquinarias else []

        def cargar_productos(self):
            productos = self.controlador.listar_productos()
            self.producto_combobox['values'] = [f"{producto[2]} - {producto[3]}" for producto in productos]


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

            idmaquinaria, maquinaria_nombre = maquinaria_seleccionada.split(" - ", 1)
            # Guardar datos para la tabla y el reporte
            self.productos_temporales.append({
                "producto": producto_seleccionado,
                "cantidad": int(cantidad),
                "idmaquinaria": int(idmaquinaria),
                "maquinaria_destino": maquinaria_nombre  # Para reporte, no se guarda en BD
            })
            self.actualizar_tabla()


        def actualizar_tabla(self):
            for item in self.tree.get_children():
                self.tree.delete(item)
            for producto in self.productos_temporales:
                self.tree.insert(
                    "", tk.END, 
                    values=(producto["producto"], producto["cantidad"], producto["idmaquinaria"], producto["maquinaria_destino"])
                )

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

        def generar_reporte_pdf(self, salida_id, fecha, responsable, observaciones, productos):
            pdf = FPDF()
            pdf.add_page()

            # Configuración general del PDF
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)

            # Logo de la empresa
            try:
                pdf.image("vista/imagen/marca.png", x=170, y=0, w=40)
            except FileNotFoundError:
                print("No se encontró el logo. Asegúrate de tener 'marca.png' en el directorio.")
            pdf.set_xy(50, 10)
            pdf.set_font("Arial", style="B", size=16)
            pdf.cell(200, 10, "KOELSA PERU S.R.L.", ln=True, align="L")
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 10, "RUC: 20529427485", ln=True, align="L")
            pdf.cell(200, 10, "Dirección: Otr. Panamericana Sur Km. 26 Lote. 1", ln=True, align="L")
            pdf.cell(200, 10, "Distrito: Lurín, Lima, Perú", ln=True, align="L")
            pdf.ln(10)

            # Título del Reporte
            pdf.set_font("Arial", style="B", size=14)
            pdf.cell(200, 10, txt="REPORTE DE SALIDA DE PRODUCTOS", ln=True, align="C")
            pdf.ln(5)

            # Detalles de la salida
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"ID Salida: {salida_id}", ln=True)
            pdf.cell(200, 10, txt=f"Fecha: {fecha}", ln=True)
            pdf.cell(200, 10, txt=f"Responsable: {responsable}", ln=True)
            pdf.multi_cell(200, 10, txt=f"Observaciones: {observaciones}")
            pdf.ln(10)

            # Título de la tabla
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(200, 10, txt="Lista de Productos:", ln=True)
            pdf.ln(5)

            # Encabezados de la tabla
            pdf.set_fill_color(220, 220, 220)
            pdf.set_font("Arial", style="B", size=10)
            pdf.cell(100, 10, "Producto", border=1, align="C", fill=True)
            pdf.cell(20, 10, "Cantidad", border=1, align="C", fill=True)
            pdf.cell(70, 10, "Maquinaria Destino", border=1, align="C", fill=True)
            pdf.ln()

            # Iterar sobre los productos y añadirlos
            pdf.set_font("Arial", size=10)
            for prod in productos:
                pdf.cell(100, 10, prod["producto"], border=1, align="C")
                pdf.cell(20, 10, str(prod["cantidad"]), border=1, align="C")
                pdf.cell(70, 10, prod["maquinaria_destino"], border=1, align="C")
                pdf.ln()

            # Espacio para la firma
            pdf.ln(20)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="_________________________", ln=True, align="C")
            pdf.cell(200, 10, txt="Firma del Responsable", ln=True, align="C")

            # Guardar el archivo
            filename = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                    filetypes=[("PDF files", "*.pdf")])
            if filename:
                pdf.output(filename)
                messagebox.showinfo("Éxito", f"Reporte guardado como {filename}")




        def guardar_salida(self):
            fecha = self.fecha_entry.get()
            responsable = self.responsable_entry.get()
            observaciones = self.observaciones_entry.get("1.0", tk.END).strip()

            if not responsable:
                messagebox.showerror("Error", "Debe ingresar un responsable.")
                return

            if not self.productos_temporales:
                messagebox.showerror("Error", "Debe agregar al menos un producto a la salida.")
                return

            # Preparar los datos para la base de datos (sin maquinaria_destino)
            productos_para_bd = [(prod["producto"], prod["cantidad"], prod["idmaquinaria"]) for prod in self.productos_temporales]

            # Copiar productos para el reporte (incluye maquinaria_destino)
            productos_para_reporte = self.productos_temporales.copy()

            salida_id = self.controlador.guardar_salida(fecha, responsable, productos_para_bd, observaciones)
            if salida_id:
                messagebox.showinfo("Éxito", f"Salida registrada con ID: {salida_id}")
                self.productos_temporales = []  # Vaciar lista después de copiar
                self.actualizar_tabla()
                self.generar_reporte_pdf(salida_id, fecha, responsable, observaciones, productos_para_reporte)
            else:
                messagebox.showerror("Error", "Ocurrió un error al guardar la salida.")
