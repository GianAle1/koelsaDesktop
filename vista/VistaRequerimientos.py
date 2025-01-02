import tkinter as tk
from tkinter import ttk, Menu, messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from vista.VistaEditarRequerimiento import VistaEditarRequerimiento

class VistaRequerimientos:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Lista de Requerimientos")
        self.root.geometry("1200x600")
        self.root.configure(bg="#e8f4f8")

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

        # Encabezados de la tabla
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=200)

        # Bindings
        self.tree.bind("<Double-1>", self.editar_requerimiento)
        self.tree.bind("<Button-3>", self.mostrar_menu_contextual)

        # Scrollbars
        scroll_y = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self.frame_tabla, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Cargar requerimientos
        self.listar_requerimientos()

        # Menú contextual
        self.menu_contextual = Menu(self.root, tearoff=0)
        self.menu_contextual.add_command(label="Generar Reporte", command=self.generar_reporte)

    def listar_requerimientos(self):
        requerimientos = self.controlador.listar_requerimientos()
        self.actualizar_tabla(requerimientos)

    def actualizar_tabla(self, requerimientos):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for requerimiento in requerimientos:
            valores = tuple(requerimiento)
            self.tree.insert("", tk.END, values=valores)

    def editar_requerimiento(self, event):
        # Obtener el elemento seleccionado
        item = self.tree.focus()
        if not item:
            tk.messagebox.showwarning("Selección requerida", "Por favor selecciona un requerimiento.")
            return

        # Recuperar los valores del elemento seleccionado
        valores = self.tree.item(item, "values")
        if not valores:
            tk.messagebox.showwarning("Error", "No se pudieron recuperar los datos del requerimiento seleccionado.")
            return

        # Crear una nueva ventana para editar
        ventana_edicion = tk.Toplevel(self.root)
        VistaEditarRequerimiento(ventana_edicion, self.controlador, valores)

    def mostrar_menu_contextual(self, event):
        # Mostrar menú contextual al hacer clic derecho
        try:
            item = self.tree.identify_row(event.y)
            if item:
                self.tree.selection_set(item)
                self.menu_contextual.post(event.x_root, event.y_root)
        finally:
            self.menu_contextual.grab_release()

    def generar_reporte(self):
        # Obtener el elemento seleccionado
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Selección requerida", "Por favor selecciona un requerimiento.")
            return

        # Recuperar el ID del requerimiento
        valores = self.tree.item(item, "values")
        id_requerimiento = valores[0] if valores else None

        if not id_requerimiento:
            messagebox.showerror("Error", "No se pudo recuperar el ID del requerimiento seleccionado.")
            return

        # Obtener detalles del requerimiento
        detalles = self.controlador.obtener_detalle_requerimiento(id_requerimiento)
        print(detalles)

        # Preguntar al usuario dónde guardar el PDF
        archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar reporte como"
        )

        if archivo:
            self.crear_reporte_pdf(archivo, id_requerimiento, detalles)

    def crear_reporte_pdf(self, archivo, id_requerimiento, detalles):
        try:
            c = canvas.Canvas(archivo, pagesize=letter)
            c.setFont("Helvetica", 10)

            # Título del reporte
            c.drawString(100, 750, f"REQUERIMIENTO FORMATO 2024")
            c.drawString(100, 735, f"REQUERIMIENTO DE REPUESTOS O DE SERVICIO")
            c.drawString(100, 720, f"Nº REQ: {id_requerimiento}")

            # Encabezados
            y = 700
            c.drawString(30, y, "ITEM")
            c.drawString(80, y, "PART NAME")
            c.drawString(200, y, "CANT.")
            c.drawString(250, y, "USO")
            c.drawString(300, y, "DESCRIPCION")
            c.drawString(450, y, "PROVEEDOR")
            c.drawString(550, y, "COSTO UNITARIO")
            c.drawString(650, y, "COSTO TOTAL")
            y -= 20

            # Detalles
            for detalle in detalles:
                c.drawString(30, y, str(detalle["item"]))
                c.drawString(80, y, detalle["part_name"])
                c.drawString(200, y, str(detalle["cantidad"]))
                c.drawString(250, y, detalle["uso"])
                c.drawString(300, y, detalle["descripcion"])
                c.drawString(450, y, detalle["proveedor"])
                c.drawString(550, y, f"${detalle['costo_unitario']:.2f}")
                c.drawString(650, y, f"${detalle['costo_total']:.2f}")
                y -= 20
                if y < 50:  # Salto de página si no hay más espacio
                    c.showPage()
                    y = 750

            c.save()
            messagebox.showinfo("Reporte generado", f"Reporte guardado como {archivo}.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el reporte: {e}")

    

    def mostrar_requerimientos(self):
        """Muestra la ventana de requerimientos."""
        self.root.mainloop()
