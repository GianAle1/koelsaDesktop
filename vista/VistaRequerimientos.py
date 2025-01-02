import tkinter as tk
from tkinter import ttk, Menu, messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import date

class VistaRequerimientos:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Lista de Requerimientos")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f4f4f9")

        # Título
        self.titulo_label = tk.Label(
            self.root, text="Lista de Requerimientos",
            font=("Arial", 18, "bold"), bg="#007ACC", fg="white", pady=10
        )
        self.titulo_label.pack(fill=tk.X)

        # Frame para la tabla
        self.frame_tabla = tk.Frame(self.root, bg="white", bd=2, relief="ridge")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configuración de la tabla
        columnas = ("ID", "Fecha", "Criterio", "Productos", "Total")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=20)

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=200)

        # Scrollbars
        scroll_y = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self.frame_tabla, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Evento clic derecho
        self.tree.bind("<Button-3>", self.mostrar_menu_contextual)

        # Menú contextual
        self.menu_contextual = Menu(self.root, tearoff=0)
        self.menu_contextual.add_command(label="Generar Reporte", command=self.generar_reporte)

        # Cargar requerimientos
        self.listar_requerimientos()

    def listar_requerimientos(self):
        requerimientos = self.controlador.listar_requerimientos()
        self.actualizar_tabla(requerimientos)

    def actualizar_tabla(self, requerimientos):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for requerimiento in requerimientos:
            valores = tuple(requerimiento)
            self.tree.insert("", tk.END, values=valores)

    def mostrar_menu_contextual(self, event):
        # Mostrar menú contextual al hacer clic derecho
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.menu_contextual.post(event.x_root, event.y_root)

    def generar_reporte(self):
        # Obtener el elemento seleccionado
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Selección requerida", "Por favor selecciona un requerimiento.")
            return

        valores = self.tree.item(item, "values")
        id_requerimiento = valores[0]
        fecha_solicitud = valores[1]
        total = float(valores[4])

        detalles = self.controlador.obtener_detalle_requerimiento(id_requerimiento)

        archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar reporte como"
        )

        if archivo:
            self.crear_reporte_pdf(archivo, detalles, id_requerimiento, fecha_solicitud, total)

    def crear_reporte_pdf(self, archivo, detalles, id_requerimiento, fecha_solicitud, total):
        try:
            c = canvas.Canvas(archivo, pagesize=letter)
            ancho, alto = letter

            # Título del reporte
            c.setFont("Helvetica-Bold", 14)
            c.drawString(200, alto - 50, "REQUERIMIENTO FORMATO 2024")
            c.drawString(200, alto - 70, "REQUERIMIENTO DE REPUESTOS O DE SERVICIO")
            c.setFont("Helvetica", 10)
            c.drawString(400, alto - 70, f"REQ.-N° {id_requerimiento}")

            # Información adicional
            c.setFont("Helvetica", 10)
            c.drawString(50, alto - 100, f"* FECHA DE SOLICITUD: {fecha_solicitud}")
            c.drawString(400, alto - 100, "SERVICIOS")
            c.drawString(50, alto - 120, "* AREA DE TRABAJO O PROYECTO:")
            c.drawString(400, alto - 120, "* FECHA DE ENTREGA:")
            c.drawString(500, alto - 120, f"TOTAL: ${total:.2f}")

            # Encabezados de la tabla
            y = alto - 160
            encabezados = ["ITEM", "PART NAME", "CANT.", "USO", "DESCRIPCION DE REPUESTO", "PROVEEDOR", "UN. MED.", "NOMBRE DEL EQUIPO", "SERIE EQUIPO", "NOMBRE DE PROY./ALM.", "COSTO UNITARIO", "COSTO TOTAL"]
            posiciones_x = [30, 80, 130, 180, 250, 400, 470, 500, 550, 600, 650, 700]

            c.setFont("Helvetica-Bold", 8)
            for i, encabezado in enumerate(encabezados):
                c.drawString(posiciones_x[i], y, encabezado)

            y -= 20
            c.setFont("Helvetica", 8)

            # Detalles del requerimiento
            for idx, detalle in enumerate(detalles, start=1):
                if y < 50:  # Salto de página
                    c.showPage()
                    y = alto - 50
                c.drawString(posiciones_x[0], y, str(idx))
                c.drawString(posiciones_x[1], y, detalle[2])  # PART NAME
                c.drawString(posiciones_x[2], y, str(detalle[3]))  # CANT.
                c.drawString(posiciones_x[3], y, detalle[6])  # USO
                c.drawString(posiciones_x[4], y, detalle[2])  # DESCRIPCION
                c.drawString(posiciones_x[5], y, detalle[7])  # PROVEEDOR
                c.drawString(posiciones_x[6], y, "UND")  # UNIDAD MEDIDA
                c.drawString(posiciones_x[7], y, detalle[8])  # NOMBRE EQUIPO
                c.drawString(posiciones_x[8], y, "-")  # SERIE EQUIPO
                c.drawString(posiciones_x[9], y, detalle[9])  # NOMBRE PROY./ALM.
                c.drawString(posiciones_x[10], y, f"${detalle[4]:.2f}")  # COSTO UNITARIO
                c.drawString(posiciones_x[11], y, f"${detalle[5]:.2f}")  # COSTO TOTAL
                y -= 20

            c.save()
            messagebox.showinfo("Reporte generado", f"Reporte guardado como {archivo}.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el reporte: {e}")

    def mostrar_requerimientos(self):
        """Muestra la ventana de requerimientos."""
        self.root.mainloop()
