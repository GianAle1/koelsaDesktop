import tkinter as tk
from tkinter import  ttk
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

        # Scrollbars
        scroll_y = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self.frame_tabla, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

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

    def mostrar_requerimientos(self):
        """Muestra la ventana de requerimientos."""
        self.root.mainloop()

