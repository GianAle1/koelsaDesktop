import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import messagebox
from datetime import date
from tkinter import ttk
from fpdf import FPDF  # Para la generación del PDF
from tkinter import filedialog, messagebox  # Para mostrar diálogos de guardado y mensajes

class CustomAutocompleteCombobox(AutocompleteCombobox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.completion_list = []
        self._completion_matches = []
        self.bind("<Return>", self._filter_matches)  # ✅ Ahora filtra al presionar Enter

    def set_completion_list(self, completion_list):
        """Actualiza la lista de valores disponibles para autocompletar."""
        self.completion_list = completion_list

    def _filter_matches(self, event=None):
        """Filtra valores que coincidan con cualquier parte de la cadena cuando se presiona Enter."""
        text = self.get().lower()
        if text == "":
            self._completion_matches = self.completion_list
        else:
            # Buscar coincidencias en cualquier parte de la cadena
            self._completion_matches = [item for item in self.completion_list if text in item.lower()]

        self._update_listbox()

    def _update_listbox(self):
        """Actualiza los elementos desplegables."""
        self["values"] = self._completion_matches
        if self._completion_matches:
            self.event_generate("<Down>")  # Abre el desplegable si hay coincidencias



class VistaEntrada:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Registrar Entrada de Producto")
        self.root.geometry("900x700")
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

        # Documento de Ingreso
        tk.Label(self.frame_entrada, text="Documento de Ingreso:", font=("Arial", 12), bg="#f4f4f9").grid(row=1, column=0, sticky="w", padx=5)
        self.docu_ingreso_entry = tk.Entry(self.frame_entrada, font=("Arial", 12), width=40)
        self.docu_ingreso_entry.grid(row=1, column=1, padx=5)

        # Producto
        tk.Label(self.frame_entrada, text="Producto:", font=("Arial", 12), bg="#f4f4f9").grid(row=2, column=0, sticky="w", padx=5)
        self.producto_combobox = CustomAutocompleteCombobox(self.frame_entrada, font=("Arial", 12), width=40, completevalues=[])
        self.producto_combobox.grid(row=2, column=1, padx=5)

        # Proveedor
        tk.Label(self.frame_entrada, text="Proveedor:", font=("Arial", 12), bg="#f4f4f9").grid(row=3, column=0, sticky="w", padx=5)
        self.proveedor_combobox = CustomAutocompleteCombobox(self.frame_entrada, font=("Arial", 12), width=40, completevalues=[])
        self.proveedor_combobox.grid(row=3, column=1, padx=5)

        # Cantidad
        tk.Label(self.frame_entrada, text="Cantidad:", font=("Arial", 12), bg="#f4f4f9").grid(row=4, column=0, sticky="w", padx=5)
        self.cantidad_entry = tk.Entry(self.frame_entrada, font=("Arial", 12), width=20)
        self.cantidad_entry.grid(row=4, column=1, padx=5)

        # Precio
        tk.Label(self.frame_entrada, text="Precio:", font=("Arial", 12), bg="#f4f4f9").grid(row=5, column=0, sticky="w", padx=5)
        self.precio_entry = tk.Entry(self.frame_entrada, font=("Arial", 12), width=20)
        self.precio_entry.grid(row=5, column=1, padx=5)

        # Botón para agregar a la lista temporal
        self.agregar_button = tk.Button(
            self.frame_entrada, text="Agregar", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.agregar_producto
        )
        self.agregar_button.grid(row=6, column=1, sticky="e", pady=10)

        # Tabla para los productos agregados
        self.frame_tabla = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas = ("Producto", "Cantidad", "Precio Unitario", "Proveedor", "Total")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=10)

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Botón para guardar la entrada
        self.guardar_button = tk.Button(
            self.root, text="Guardar Entrada", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.guardar_entrada
        )
        self.guardar_button.pack(pady=10)

        # Cargar productos y proveedores al combobox
        self.cargar_productos()
        self.cargar_proveedores()

        # Lista temporal para los productos
        self.productos_temporales = []

    def cargar_productos(self):
        productos = self.controlador.listar_productos()
        if productos:
            values = [
                f"{producto[0]} - {producto[1]} - {producto[2]} - {producto[3]}" for producto in productos
            ]
            self.producto_combobox.set_completion_list(values)
            self.productos_info = {producto[0]: producto for producto in productos}

    def cargar_proveedores(self):
        proveedores = self.controlador.listar_proveedores()
        if proveedores:
            values = [f"{proveedor[0]} - {proveedor[1]} - {proveedor[2]}" for proveedor in proveedores]
            self.proveedor_combobox.set_completion_list(values)
            self.proveedores_info = {proveedor[0]: proveedor for proveedor in proveedores}

    def agregar_producto(self):
        producto_seleccionado = self.producto_combobox.get()
        proveedor_seleccionado = self.proveedor_combobox.get()
        cantidad = self.cantidad_entry.get()
        precio = self.precio_entry.get()

        if not producto_seleccionado or not proveedor_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un producto y un proveedor.")
            return

        try:
            id_producto = int(producto_seleccionado.split(" - ")[0])
            id_proveedor = int(proveedor_seleccionado.split(" - ")[0])
            cantidad = int(cantidad)
            precio = float(precio)
            total = cantidad * precio

            self.productos_temporales.append((id_producto, producto_seleccionado, cantidad, precio, id_proveedor, proveedor_seleccionado, total))
            self.actualizar_tabla()
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar valores numéricos válidos.")

    def actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for _, nombre_producto, cantidad, precio, _, nombre_proveedor, total in self.productos_temporales:
            self.tree.insert("", tk.END, values=(nombre_producto, cantidad, f"{precio:.2f}", nombre_proveedor, f"{total:.2f}"))

    def guardar_entrada(self):
        """Guarda la entrada en la base de datos y genera el reporte."""
        fecha = self.fecha_entry.get()
        docu_ingreso = self.docu_ingreso_entry.get()

        if not self.productos_temporales:
            messagebox.showerror("Error", "Debe agregar al menos un producto a la entrada.")
            return

        try:
            # 🔹 Guardar la entrada en la BD y obtener el ID generado
            identrada = self.controlador.guardar_entrada(fecha, docu_ingreso, self.productos_temporales)

            if identrada:
                # 🔹 Generar el reporte PDF automáticamente
                self.generar_reporte_pdf(identrada, fecha, docu_ingreso, self.productos_temporales)

                messagebox.showinfo("Éxito", "Entrada registrada correctamente.")
                self.productos_temporales.clear()
                self.actualizar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo guardar la entrada en la base de datos.")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar la entrada: {e}")

    def generar_reporte_pdf(self, identrada, fecha, docu_ingreso, productos):
        """Genera un reporte PDF de la entrada registrada."""
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Configuración de fuente
        pdf.set_font("Arial", style="B", size=16)

        # Título del reporte
        pdf.cell(0, 10, "REPORTE DE ENTRADA DE PRODUCTOS - TALLER LIMA", ln=True, align="C")
        pdf.ln(5)

        # Información General
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"ID de Entrada: {identrada}", ln=True)
        pdf.cell(0, 10, f"Fecha: {fecha}", ln=True)
        pdf.cell(0, 10, f"Documento de Ingreso: {docu_ingreso}", ln=True)
        pdf.ln(5)

        # Encabezado de tabla
        pdf.set_font("Arial", style="B", size=12)
        pdf.set_fill_color(220, 220, 220)
        
        columnas = ["Producto", "Cantidad", "Precio Unitario", "Total"]
        anchos = [80, 30, 40, 40]  # Ajustar tamaños de columna

        for col, width in zip(columnas, anchos):
            pdf.cell(width, 10, col, border=1, align="C", fill=True)
        pdf.ln()

        # Agregar productos a la tabla
        pdf.set_font("Arial", size=10)
        total_general = 0  # Suma total de la entrada

        for _, nombre_producto, cantidad, precio, _, nombre_proveedor, total in productos:
            pdf.cell(80, 10, nombre_producto, border=1, align="C")
            pdf.cell(30, 10, str(cantidad), border=1, align="C")
            pdf.cell(40, 10, f"S/. {precio:.2f}", border=1, align="C")
            pdf.cell(40, 10, f"S/. {total:.2f}", border=1, align="C")
            pdf.ln()
            total_general += total

        # Línea final con el total general
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(150, 10, "Total General", border=1, align="R")
        pdf.cell(40, 10, f"S/. {total_general:.2f}", border=1, align="C")
        pdf.ln(15)

        # Firma del Responsable
        pdf.cell(0, 10, "_________________________", ln=True, align="C")
        pdf.cell(0, 10, "Firma del Responsable", ln=True, align="C")

        # Guardar archivo con cuadro de diálogo
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"entrada_{identrada}.pdf",
            title="Guardar Reporte de Entrada"
        )

        if filename:
            try:
                pdf.output(filename)
                messagebox.showinfo("Éxito", f"Reporte guardado correctamente en:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el reporte: {e}")


    def eliminar_producto(self):
        """Elimina un producto de la lista temporal."""
        selected_item = self.tree.selection()
        if selected_item:
            for item in selected_item:
                self.tree.delete(item)
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto para eliminar.")
