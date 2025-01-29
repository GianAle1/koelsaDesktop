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

        # Botón para agregar a la lista
        self._crear_boton("Agregar Producto", self.agregar_producto, "#4CAF50")

        # Tabla para productos agregados
        self._crear_tabla()

        # Botón para eliminar producto
        self._crear_boton("Eliminar Producto", self.eliminar_producto, "#f44336", pady=10)

        # Botón para guardar la salida
        self._crear_boton("Guardar Salida", self.guardar_salida, "#4CAF50", pady=10)

        # Inicializar listas y cargar datos
        self.productos_temporales = []
        self.cargar_maquinarias()
        self.cargar_productos()
        self.cargar_responsables()  # Cargar responsables en el combobox

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
        self.frame_tabla = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas = ("Producto", "Cantidad", "Precio", "ID Maquinaria", "Maquinaria Destino")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=200)

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
        """Carga los productos en el combobox desde la base de datos."""
        try:
            productos = self.controlador.listar_productos()
            if productos:
                self.producto_combobox["values"] = [
                    f"{prod[0]} - {prod[2]} ({prod[3]}) - Precio: {prod[7]:.2f}" for prod in productos
                ]
        except Exception as e:
            print(f"Error al cargar productos: {e}")

    def agregar_producto(self):
        """Agrega un producto seleccionado a la lista temporal."""
        producto_seleccionado = self.producto_combobox.get()
        cantidad = self.cantidad_entry.get()
        maquinaria_seleccionada = self.maquinaria_combobox.get()

        if not producto_seleccionado or not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Debe seleccionar un producto y una cantidad válida.")
            return

        if not maquinaria_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una maquinaria.")
            return

        id_producto = int(producto_seleccionado.split(" - ")[0])
        id_maquinaria = int(maquinaria_seleccionada.split(" - ")[0])
        nombre_producto = producto_seleccionado.split(" - ")[1]
        maquinaria_destino = maquinaria_seleccionada.split(" - ")[1]

        self.productos_temporales.append({
            "id_producto": id_producto,
            "producto": nombre_producto,
            "cantidad": int(cantidad),
            "idmaquinaria": id_maquinaria,
            "maquinaria_destino": maquinaria_destino
        })

        self.actualizar_tabla()
        messagebox.showinfo("Éxito", "Producto agregado correctamente.")

    def actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for producto in self.productos_temporales:
            self.tree.insert("", tk.END, values=(
                producto["producto"], producto["cantidad"], producto["idmaquinaria"], producto["maquinaria_destino"]
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
        fecha = self.fecha_entry.get()
        responsable = self.responsable_combobox.get()

        if not responsable:
            messagebox.showerror("Error", "Debe seleccionar un responsable.")
            return

        id_responsable = int(responsable.split(" - ")[0])
        self.controlador.guardar_salida(fecha, id_responsable, self.productos_temporales)
        messagebox.showinfo("Éxito", "Salida registrada correctamente.")

    def cargar_responsables(self):
        """Carga los responsables en el combobox desde la base de datos."""
        try:
            responsables = self.controlador.listar_responsables()  # Llamamos al controlador
            if responsables:
                self.responsable_combobox["values"] = [
                    f"{resp[0]} - {resp[1]}" for resp in responsables
                ]
            else:
                self.responsable_combobox["values"] = []
        except Exception as e:
            print(f"Error al cargar responsables: {e}")


    def generar_reporte_pdf(self, salida_id, fecha, responsable, observaciones, productos):
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", size=12)

        try:
            pdf.image("vista/imagen/marca.png", x=170, y=10, w=30)
        except FileNotFoundError:
            pass

        pdf.set_xy(10, 20)
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(0, 10, "KOELSA PERU S.R.L.", ln=True, align="L")
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 10, "RUC: 20529427485", ln=True, align="L")
        pdf.cell(0, 10, "Dirección: Otr. Panamericana Sur Km. 26 Lote. 1", ln=True, align="L")
        pdf.cell(0, 10, "Distrito: Lurín, Lima, Perú", ln=True, align="L")
        pdf.ln(15)

        pdf.set_font("Arial", style="B", size=14)
        pdf.set_text_color(50, 50, 255)
        pdf.cell(0, 10, "REPORTE DE SALIDA DE PRODUCTOS", ln=True, align="C")
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)

        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"ID Salida: {salida_id}", ln=True)
        pdf.cell(0, 10, f"Fecha: {fecha}", ln=True)
        pdf.cell(0, 10, f"Responsable: {responsable}", ln=True)
        pdf.multi_cell(0, 10, f"Observaciones: {observaciones}")
        pdf.ln(10)

        pdf.set_font("Arial", style="B", size=12)
        pdf.set_fill_color(220, 220, 220)
        pdf.cell(10, 10, "N°", border=1, align="C", fill=True)
        pdf.cell(60, 10, "Producto", border=1, align="C", fill=True)
        pdf.cell(30, 10, "Cantidad", border=1, align="C", fill=True)
        pdf.cell(30, 10, "Precio", border=1, align="C", fill=True)
        pdf.cell(60, 10, "Maquinaria Destino", border=1, align="C", fill=True)
        pdf.ln()

        pdf.set_font("Arial", size=10)
        for idx, prod in enumerate(productos, start=1):
            pdf.cell(10, 10, str(idx), border=1, align="C")
            pdf.cell(60, 10, prod["producto"], border=1, align="C")
            pdf.cell(30, 10, str(prod["cantidad"]), border=1, align="C")
            pdf.cell(30, 10, f"{prod['precio']:.2f}", border=1, align="C")
            pdf.cell(60, 10, prod["maquinaria_destino"], border=1, align="C")
            pdf.ln()

        pdf.ln(20)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "_________________________", ln=True, align="C")
        pdf.cell(0, 10, "Firma del Responsable", ln=True, align="C")

        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if filename:
            pdf.output(filename)
            messagebox.showinfo("Éxito", f"Reporte guardado como {filename}")
