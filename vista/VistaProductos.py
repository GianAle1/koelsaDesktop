import tkinter as tk
from tkinter import ttk

class VistaProductos:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Inventario de Productos")
        self.root.geometry("1400x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#e8f4f8")  # Fondo más claro

        # Título estilizado
        self.titulo_label = tk.Label(
            self.root, text="Inventario de Productos",
            font=("Arial", 18, "bold"), bg="#007ACC", fg="white", pady=10
        )
        self.titulo_label.pack(fill=tk.X)

        # Frame para Filtros
        self.frame_filtros = tk.Frame(self.root, bg="#e8f4f8")
        self.frame_filtros.pack(fill=tk.X, padx=10, pady=10)

        # Filtro por familia
        tk.Label(
            self.frame_filtros, text="Filtrar por Familia:",
            font=("Arial", 12, "bold"), bg="#e8f4f8", fg="#333333"
        ).pack(side=tk.LEFT, padx=5)

        self.familia_combobox = ttk.Combobox(
            self.frame_filtros, state="readonly",
            font=("Arial", 12), width=30
        )
        self.familia_combobox.pack(side=tk.LEFT, padx=10)

        # Botón de Filtrar
        self.boton_filtrar = tk.Button(
            self.frame_filtros, text="Filtrar", font=("Arial", 12, "bold"),
            bg="#4CAF50", fg="white", command=self.listar_productos,
            relief="groove", bd=2
        )
        self.boton_filtrar.pack(side=tk.LEFT, padx=10)

        # Botón de Restablecer
        self.boton_resetear = tk.Button(
            self.frame_filtros, text="Restablecer", font=("Arial", 12, "bold"),
            bg="#f44336", fg="white", command=self.listar_productos,
            relief="groove", bd=2
        )
        self.boton_resetear.pack(side=tk.LEFT, padx=10)

        # Frame contenedor para la tabla
        self.frame_tabla = tk.Frame(self.root, bg="white", bd=2, relief="ridge")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configuración de la tabla
        columnas = (
            "ID", "Part Name", "Descripción", "Marca", "Proveedor", "Familia",
            "Unidad de Medida", "Cantidad", "Precio", "Almacén"
        )
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=20)

        # Estilo de encabezados de la tabla
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="#007ACC")
        style.configure("Treeview", font=("Arial", 11), rowheight=25)

        # Encabezados de la tabla
        for col in columnas:
            self.tree.heading(col, text=col)

        # Configurar las columnas
        self.tree.column("ID", anchor="center", width=60)
        self.tree.column("Part Name", anchor="center", width=150)
        self.tree.column("Descripción", anchor="w", width=300)
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
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Cargar productos
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
                # Asegurarse de que los valores sean cadenas y no causen errores
                valores = tuple(str(valor) if valor is not None else "" for valor in producto)
                tag = "oddrow" if index % 2 == 0 else "evenrow"
                try:
                    self.tree.insert("", tk.END, values=valores, tags=(tag,))
                except Exception as e:
                    print(f"Error insertando el producto en la tabla: {e}")
        else:
            self.tree.insert("", tk.END, values=("No se encontraron productos",), tags=("oddrow",))
