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

        # Aquí cambiamos el campo Responsable de Entry a Combobox
        self.responsable_combobox = self._crear_combobox("Responsable:", 1)

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

    def _crear_boton(self, texto, row, command, bg_color, pady=0):
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
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("ID Maquinaria", text="ID Maquinaria")
        self.tree.heading("Maquinaria Destino", text="Maquinaria Destino")
        self.tree.column("Producto", anchor="center", width=200)
        self.tree.column("Cantidad", anchor="center", width=100)
        self.tree.column("Precio", anchor="center", width=100)
        self.tree.column("ID Maquinaria", anchor="center", width=150)
        self.tree.column("Maquinaria Destino", anchor="center", width=200)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def cargar_responsables(self):
        """Carga los responsables en el combobox desde la base de datos."""
        try:
            responsables = self.controlador.listar_responsables()
            if responsables:
                self.responsable_combobox["values"] = [
                    f"{resp[0]} - {resp[1]}" for resp in responsables
                ]
                print("Responsables cargados:", self.responsable_combobox["values"])
            else:
                self.responsable_combobox["values"] = []
                print("No se encontraron responsables en la base de datos.")
        except Exception as e:
            print(f"Error al cargar responsables: {e}")

    def guardar_salida(self):
        """Guarda la salida de productos en la base de datos."""
        fecha = self.fecha_entry.get()
        responsable = self.responsable_combobox.get()
        observaciones = self.observaciones_entry.get("1.0", tk.END).strip()

        if not responsable:
            messagebox.showerror("Error", "Debe seleccionar un responsable.")
            return

        if not self.productos_temporales:
            messagebox.showerror("Error", "Debe agregar al menos un producto a la salida.")
            return

        # Extraer ID del responsable
        try:
            id_responsable = int(responsable.split(" - ")[0])  # Extrae el ID del formato "ID - Nombre"
        except ValueError:
            messagebox.showerror("Error", "El formato del responsable no es válido.")
            return

        productos_para_bd = [
            (prod["id_producto"], prod["cantidad"], prod["idmaquinaria"]) for prod in self.productos_temporales
        ]

        try:
            salida_id = self.controlador.guardar_salida(fecha, id_responsable, productos_para_bd, observaciones)
            if salida_id:
                messagebox.showinfo("Éxito", f"Salida registrada con ID: {salida_id}")
                self.productos_temporales = []
                self.actualizar_tabla()
            else:
                messagebox.showerror("Error", "Ocurrió un error al guardar la salida.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar la salida: {e}")


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

        pdf.set_font("Arial", style="B", size=11)
        pdf.set_fill_color(220, 220, 220)
        pdf.cell(10, 10, "N°", border=1, align="C", fill=True)
        pdf.cell(80, 10, "Producto", border=1, align="C", fill=True)
        pdf.cell(10, 10, "Cant", border=1, align="C", fill=True)
        pdf.cell(15, 10, "Precio", border=1, align="C", fill=True)
        pdf.cell(75, 10, "Maquinaria Destino", border=1, align="C", fill=True)
        pdf.ln()

        pdf.set_font("Arial", size=10)
        for idx, prod in enumerate(productos, start=1):
            pdf.cell(10, 10, str(idx), border=1, align="C")
            pdf.cell(80, 10, prod["producto"], border=1, align="C")
            pdf.cell(10, 10, str(prod["cantidad"]), border=1, align="C")
            pdf.cell(15, 10, f"{prod['precio']:.2f}", border=1, align="C")
            pdf.cell(75, 10, prod["maquinaria_destino"], border=1, align="C")
            pdf.ln()

        pdf.ln(20)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "_________________________", ln=True, align="C")
        pdf.cell(0, 10, "Firma del Responsable", ln=True, align="C")

        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if filename:
            pdf.output(filename)
            messagebox.showinfo("Éxito", f"Reporte guardado como {filename}")
