import tkinter as tk
from tkinter import ttk

class VistaProductos:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Inventario de Productos")
        self.root.geometry("1400x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f4f9")

        # Título estilizado
        self.titulo_label = tk.Label(
            self.root, text="Inventario de Productos", 
            font=("Arial", 18, "bold"), bg="#4CAF50", fg="white", pady=10
        )
        self.titulo_label.pack(fill=tk.X)

        # Frame contenedor para la tabla
        self.frame_tabla = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configuración de la tabla
        columnas = ("ID", "Part Name", "Descripción", "Marca", "Proveedor", "Familia",
                    "Unidad de Medida", "Cantidad", "Precio", "Almacén")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=24)

        # Encabezados de la tabla
        self.tree.heading("ID", text="ID")
        self.tree.heading("Part Name", text="Part Name")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Marca", text="Marca")
        self.tree.heading("Proveedor", text="Proveedor")
        self.tree.heading("Familia", text="Familia")
        self.tree.heading("Unidad de Medida", text="Unidad de Medida")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Almacén", text="Almacén")

        # Configurar las columnas (solo Descripción más grande)
        self.tree.column("ID", anchor="center", width=60)
        self.tree.column("Part Name", anchor="center", width=150)
        self.tree.column("Descripción", anchor="w", width=200)  
        self.tree.column("Marca", anchor="center", width=120)
        self.tree.column("Proveedor", anchor="center", width=150)
        self.tree.column("Familia", anchor="center", width=120)
        self.tree.column("Unidad de Medida", anchor="center", width=120)
        self.tree.column("Cantidad", anchor="center", width=100)
        self.tree.column("Precio", anchor="center", width=100)
        self.tree.column("Almacén", anchor="center", width=150)

        # Scrollbars
        scroll_y = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self.frame_tabla, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.listar_productos()    
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
                self.tree.insert("", tk.END, values=(producto[0], producto[1], producto[2], producto[3], producto[4], producto[5], producto[6], producto[7], producto[8],producto[9]), tags=(tag,))
        else:
            self.tree.insert("", tk.END, values=("No se encontraron productos", ""), tags=("oddrow",))