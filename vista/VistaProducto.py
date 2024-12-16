# vista/VistaProducto.py
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

class VistaProducto:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Registrar Producto")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Frame para organizar el contenido
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=30)

        # Título
        self.titulo_label = tk.Label(self.frame, text="Registrar Producto", font=("Arial", 16, "bold"))
        self.titulo_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Campos para registrar producto
        self.partname_label = tk.Label(self.frame, text="Nombre del Producto:")
        self.partname_label.grid(row=1, column=0, sticky="w", padx=10)
        self.partname_entry = tk.Entry(self.frame, width=40)
        self.partname_entry.grid(row=1, column=1)

        self.descripcion_label = tk.Label(self.frame, text="Descripción:")
        self.descripcion_label.grid(row=2, column=0, sticky="w", padx=10)
        self.descripcion_entry = tk.Entry(self.frame, width=40)
        self.descripcion_entry.grid(row=2, column=1)

        self.undMedida_label = tk.Label(self.frame, text="Unidad de Medida:")
        self.undMedida_label.grid(row=3, column=0, sticky="w", padx=10)
        self.undMedida_entry = tk.Entry(self.frame, width=40)
        self.undMedida_entry.grid(row=3, column=1)

        self.cantidad_label = tk.Label(self.frame, text="Cantidad:")
        self.cantidad_label.grid(row=4, column=0, sticky="w", padx=10)
        self.cantidad_entry = tk.Entry(self.frame, width=40)
        self.cantidad_entry.grid(row=4, column=1)

        self.precio_label = tk.Label(self.frame, text="Precio:")
        self.precio_label.grid(row=5, column=0, sticky="w", padx=10)
        self.precio_entry = tk.Entry(self.frame, width=40)
        self.precio_entry.grid(row=5, column=1)

        self.proveedor_label = tk.Label(self.frame, text="Proveedor:")
        self.proveedor_label.grid(row=6, column=0, sticky="w", padx=10)
        self.proveedor_combobox = ttk.Combobox(self.frame, width=37)
        self.proveedor_combobox.grid(row=6, column=1)

        self.listar_proveedores()  # Llamar para listar los proveedores en el combobox

        self.registrar_button = tk.Button(self.frame, text="Registrar Producto", command=self.registrar_producto)
        self.registrar_button.grid(row=7, column=0, columnspan=2, pady=20)
    
    def mostrar_producto(self):
        """Muestra la ventana para gestionar producto"""
        self.root.mainloop()

    def listar_proveedores(self):
        """Carga la lista de proveedores en el ComboBox"""
        proveedores = self.controlador.listar_proveedores()
        self.proveedor_combobox['values'] = [proveedor[1] for proveedor in proveedores]  # Solo mostramos el nombre
        self.proveedor_combobox.current(0)  # Selecciona el primer proveedor por defecto
