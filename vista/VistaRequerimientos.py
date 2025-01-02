import tkinter as tk
from tkinter import ttk, Menu, messagebox, filedialog
from reportlab.lib.pagesizes import landscape, letter
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

        # Eventos
        self.tree.bind("<Double-1>", self.editar_requerimiento)  # Doble clic para editar
        self.tree.bind("<Button-3>", self.mostrar_menu_contextual)  # Clic derecho para menú contextual

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

    def editar_requerimiento(self, event):
        # Obtener el elemento seleccionado
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Selección requerida", "Por favor selecciona un requerimiento.")
            return

        # Recuperar los valores del elemento seleccionado
        valores = self.tree.item(item, "values")
        id_requerimiento = valores[0]

        # Crear ventana de edición
        ventana_edicion = tk.Toplevel(self.root)
        ventana_edicion.title("Editar Requerimiento")
        ventana_edicion.geometry("800x600")
        ventana_edicion.configure(bg="#f4f4f9")

        # Datos generales del requerimiento
        tk.Label(ventana_edicion, text="Editar Requerimiento", font=("Arial", 16, "bold"), bg="#007ACC", fg="white").pack(fill=tk.X)
        frame_general = tk.Frame(ventana_edicion, bg="#f4f4f9", pady=10)
        frame_general.pack(fill=tk.X, padx=10)

        tk.Label(frame_general, text="ID:", bg="#f4f4f9", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
        tk.Label(frame_general, text=id_requerimiento, bg="#f4f4f9", font=("Arial", 12)).grid(row=0, column=1, sticky="w")

        tk.Label(frame_general, text="Fecha:", bg="#f4f4f9", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
        fecha_entry = tk.Entry(frame_general, font=("Arial", 12))
        fecha_entry.grid(row=1, column=1, sticky="w")
        fecha_entry.insert(0, valores[1])

        tk.Label(frame_general, text="Criterio:", bg="#f4f4f9", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
        criterio_combobox = ttk.Combobox(frame_general, values=["Programada", "Normal", "Urgente"], state="readonly", font=("Arial", 12))
        criterio_combobox.grid(row=2, column=1, sticky="w")
        criterio_combobox.set(valores[2])

        # Detalles del requerimiento
        tk.Label(ventana_edicion, text="Detalles del Requerimiento", font=("Arial", 14, "bold"), bg="#007ACC", fg="white").pack(fill=tk.X, pady=5)
        frame_detalles = tk.Frame(ventana_edicion, bg="white", bd=2, relief="ridge")
        frame_detalles.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas = ("ID", "Producto", "Cantidad", "Proveedor", "Uso", "Almacén", "Precio Unitario", "Precio Total")
        detalles_tree = ttk.Treeview(frame_detalles, columns=columnas, show="headings")
        for col in columnas:
            detalles_tree.heading(col, text=col)
            detalles_tree.column(col, anchor="center", width=100)
        detalles_tree.pack(fill=tk.BOTH, expand=True)

        # Obtener detalles del requerimiento
        detalles = self.controlador.obtener_detalle_requerimiento(id_requerimiento)
        for detalle in detalles:
            detalles_tree.insert("", tk.END, values=detalle)

        # Botones
        frame_botones = tk.Frame(ventana_edicion, bg="#f4f4f9", pady=10)
        frame_botones.pack(fill=tk.X, padx=10)

        tk.Button(frame_botones, text="Guardar Cambios", font=("Arial", 12), bg="#4CAF50", fg="white", command=lambda: self.guardar_cambios_requerimiento(id_requerimiento, fecha_entry.get(), criterio_combobox.get(), detalles_tree)).pack(side=tk.RIGHT, padx=5)
        tk.Button(frame_botones, text="Cerrar", font=("Arial", 12), bg="#f44336", fg="white", command=ventana_edicion.destroy).pack(side=tk.RIGHT, padx=5)

    def guardar_cambios_requerimiento(self, id_requerimiento, fecha, criterio, detalles_tree):
        # Validar datos
        if not fecha or not criterio:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Preparar datos para guardar
        detalles_actualizados = []
        for item in detalles_tree.get_children():
            valores = detalles_tree.item(item, "values")
            detalles_actualizados.append(valores)

        exito = self.controlador.actualizar_requerimiento(id_requerimiento, fecha, criterio, detalles_actualizados)
        if exito:
            messagebox.showinfo("Éxito", "Requerimiento actualizado correctamente.")
            self.listar_requerimientos()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el requerimiento.")

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
            c = canvas.Canvas(archivo, pagesize=landscape(letter))
            ancho, alto = landscape(letter)

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
            posiciones_x = [30, 100, 150, 200, 280, 430, 500, 550, 600, 670, 720, 770]

            c.setFont("Helvetica-Bold", 8)
            for i, encabezado in enumerate(encabezados):
                c.drawString(posiciones_x[i], y, encabezado)

            y -= 20
            c.setFont("Helvetica", 8)

            # Detalles del requerimiento
            for idx, detalle in enumerate(detalles, start=1):
                if y < 50:
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
        self.root.mainloop()
