import tkinter as tk
from tkinter import ttk, Menu, messagebox, filedialog
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from datetime import date
from vista.VistaEditarRequerimiento import VistaEditarRequerimiento

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
        if not valores:
            messagebox.showwarning("Error", "No se pudo recuperar el requerimiento seleccionado.")
            return

        id_requerimiento = valores[0]
        # Abrir ventana de edición
        ventana_edicion = tk.Toplevel(self.root)
        VistaEditarRequerimiento(ventana_edicion, self.controlador, valores)

    def generar_reporte(self):
        # Implementar lógica para generar reporte si es necesario
        pass

    def mostrar_requerimientos(self):
        """Inicia el bucle principal de la ventana de requerimientos."""
        self.root.mainloop()

