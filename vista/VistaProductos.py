import tkinter as tk
from tkinter import ttk

class VistaProductos:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Inventario de Productos")

        # Configuración de la ventana
        self.root.geometry("800x600")  # Tamaño de la ventana
        self.root.resizable(True, True)

        # Frame para la tabla
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Part Name", "Descripción", "Marca", "Unidad de Medida", "Cantidad", "Proveedor", "Almacén", "Uso", "Equipo", "Precio"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Part Name", text="Part Name")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Marca", text="Marca")
        self.tree.heading("Unidad de Medida", text="Unidad de Medida")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Proveedor", text="Proveedor")
        self.tree.heading("Almacén", text="Almacén")
        self.tree.heading("Uso", text="Uso")
        self.tree.heading("Equipo", text="Equipo")
        self.tree.heading("Precio", text="Precio")

        self.scroll_y = tk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=self.scroll_y.set)

    def mostrar_inventario(self):
        self.root.mainloop()

    def listar_productos(self):
        productos = self.controlador.listar_productos()
        if productos:
            self.actualizar_lista_productos(productos)

    def actualizar_lista_productos(self, productos):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if productos:
            for index, producto in enumerate(productos):
                tag = "oddrow" if index % 2 == 0 else "evenrow"
                self.tree.insert("", tk.END, values=(producto[0], producto[1]), tags=(tag,))
        else:
            self.tree.insert("", tk.END, values=("No se encontraron productos", ""), tags=("oddrow",))