import tkinter as tk
from tkinter import messagebox
from vista.VistaUnificadaMarcas import VistaUnificadaMarcas
from vista.VistaUnificadaProveedores import VistaUnificadaProveedores
from vista.VistaProducto import VistaProducto
from vista.VistaUnificadaAlamacenes import VistaUnificadaAlamacenes
from vista.VistaProductos import VistaProductos
from vista.VistaEntrada import VistaEntrada


class VistaMenu:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Menú Principal - Koelsa SRL")
        self.root.geometry("900x750")
        self.root.resizable(False, False)
        self.root.config(bg="#f4f4f9")

        # Título
        self.titulo_label = tk.Label(
            self.root, text="Menú Principal",
            font=("Arial", 24, "bold"), bg="#4CAF50", fg="white", pady=15
        )
        self.titulo_label.pack(fill=tk.X)

        # Frame para los botones
        self.frame_botones = tk.Frame(self.root, bg="#f4f4f9")
        self.frame_botones.pack(pady=30)

        # Botones principales
        botones = [
            ("Gestionar Marcas", self.abrir_ventana_marcas, "#4CAF50"),
            ("Gestionar Proveedores", self.abrir_ventana_proveedores, "#2196F3"),
            ("Gestionar Almacenes", self.abrir_ventana_almacenes, "#673AB7"),
            ("Gestionar Inventario", self.abrir_ventana_inventario, "#FF9800"),
            ("Gestionar Productos", self.abrir_ventana_productos, "#009688"),
            ("Entrada de Productos", self.abrir_ventana_entrada_productos, "#FFC107"),
            ("Cerrar Sesión", self.cerrar_sesion, "#f44336"),
        ]

        for texto, comando, color in botones:
            boton = tk.Button(
                self.frame_botones, text=texto, font=("Arial", 14, "bold"),
                bg=color, fg="white", command=comando, width=30, height=2, relief="raised"
            )
            boton.pack(pady=10)

    def abrir_ventana_marcas(self):
        ventana_marcas = tk.Toplevel(self.root)
        vista_marcas = VistaUnificadaMarcas(ventana_marcas, self.controlador)
        vista_marcas.mostrar_marcas()

    def abrir_ventana_proveedores(self):
        ventana_proveedores = tk.Toplevel(self.root)
        vista_proveedores = VistaUnificadaProveedores(ventana_proveedores, self.controlador)
        vista_proveedores.mostrar_proveedores()

    def abrir_ventana_productos(self):
        ventana_productos = tk.Toplevel(self.root)
        vista_productos = VistaProducto(ventana_productos, self.controlador)
        vista_productos.mostrar_producto()

    def abrir_ventana_inventario(self):
        ventana_inventario = tk.Toplevel(self.root)
        vista_inventario = VistaProductos(ventana_inventario, self.controlador)
        vista_inventario.mostrar_inventario()

    def abrir_ventana_almacenes(self):
        ventana_almacenes = tk.Toplevel(self.root)
        vista_almacenes = VistaUnificadaAlamacenes(ventana_almacenes, self.controlador)
        vista_almacenes.mostrar_almacenes()

    def abrir_ventana_entrada_productos(self):
        ventana_entrada = tk.Toplevel(self.root)
        vista_entrada = VistaEntrada(ventana_entrada, self.controlador)

    def cerrar_sesion(self):
        self.root.withdraw()
        print("Sesión cerrada, volver al login.")
