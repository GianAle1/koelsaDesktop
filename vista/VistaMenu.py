import tkinter as tk
from vista.VistaUnificadaMarcas import VistaUnificadaMarcas
from vista.VistaUnificadaProveedores import VistaUnificadaProveedores
from vista.VistaProducto import VistaProducto
from vista.VistaUnificadaAlamacenes import VistaUnificadaAlamacenes
from vista.VistaProductos import VistaProductos

class VistaMenu:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Menú Principal Koelsa SRL")

        # Configuración de la ventana principal
        self.root.geometry("800x700")  # Tamaño de la ventana
        self.root.resizable(False, False)  # No permite redimensionar la ventana

        self.root.config(bg="#f0f0f0")  # Fondo claro para toda la ventana

        # Frame para organizar el contenido
        self.frame = tk.Frame(self.root, bg="#f0f0f0")
        self.frame.pack(pady=50)

        # Título
        self.titulo_label = tk.Label(self.frame, text="Menú Principal", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#4CAF50")
        self.titulo_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Botón de gestión de Marcas
        self.marcas_button = tk.Button(self.frame, text="Gestionar Marcas", width=25, height=2, font=("Arial", 12), 
                                       bg="#4CAF50", fg="white", command=self.abrir_ventana_marcas, relief="flat")
        self.marcas_button.grid(row=1, column=0, pady=15, padx=10)

        # Botón de gestión de Proveedores
        self.proveedores_button = tk.Button(self.frame, text="Gestionar Proveedores", width=25, height=2, font=("Arial", 12), 
                                            bg="#2196F3", fg="white", command=self.abrir_ventana_proveedores, relief="flat")
        self.proveedores_button.grid(row=2, column=0, pady=15, padx=10)

        # Botón de gestión de Almacenes
        self.almacenes_button = tk.Button(self.frame, text="Gestionar Almacenes", width=25, height=2, font=("Arial", 12), 
                                          bg="#2196F3", fg="white", command=self.abrir_ventana_almacenes, relief="flat")
        self.almacenes_button.grid(row=3, column=0, pady=15, padx=10)
        
        # Botón de gestión de Inventario
        self.inventario_button = tk.Button(self.frame, text="Gestionar Inventario", width=25, height=2, font=("Arial", 12), 
                                           bg="#FF9800", fg="white", command=self.abrir_ventana_inventario, relief="flat")
        self.inventario_button.grid(row=4, column=0, pady=15, padx=10)

        # Botón de gestión de Productos
        self.productos_button = tk.Button(self.frame, text="Gestionar Productos", width=25, height=2, font=("Arial", 12), 
                                          bg="#4CAF50", fg="white", command=self.abrir_ventana_productos, relief="flat")
        self.productos_button.grid(row=5, column=0, pady=15, padx=10)

        # Botón de Logout (salir)
        self.logout_button = tk.Button(self.frame, text="Cerrar Sesión", width=25, height=2, font=("Arial", 12),
                                       bg="#f44336", fg="white", command=self.cerrar_sesion, relief="flat")
        self.logout_button.grid(row=6, column=0, pady=20, padx=10)

    def mostrar_menu(self):
        """Muestra el menú principal, si el login fue exitoso"""
        self.root.deiconify()  # Si el root fue ocultado, la vuelve a mostrar

    def abrir_ventana_marcas(self):
        """Abre la ventana de gestión de marcas"""
        ventana_marcas = tk.Toplevel(self.root)
        vista_marcas = VistaUnificadaMarcas(ventana_marcas, self.controlador)
        vista_marcas.mostrar_marcas()

    def abrir_ventana_proveedores(self):
        """Abre la ventana de gestión de proveedores"""
        ventana_proveedores = tk.Toplevel(self.root)
        vista_proveedores = VistaUnificadaProveedores(ventana_proveedores, self.controlador)
        vista_proveedores.mostrar_proveedores()

    def abrir_ventana_productos(self):
        """Abre la ventana de gestión de productos"""
        ventana_productos = tk.Toplevel(self.root)
        vista_productos = VistaProducto(ventana_productos, self.controlador)
        vista_productos.mostrar_producto()

    def abrir_ventana_inventario(self):
        """Abre la ventana de gestión de inventario"""
        ventana_inventario = tk.Toplevel(self.root)
        vista_inventario = VistaProductos(ventana_inventario, self.controlador)
        vista_inventario.mostrar_inventario()

    def abrir_ventana_almacenes(self):
        """Abre la ventana de gestión de almacenes"""
        ventana_almacenes = tk.Toplevel(self.root)
        vista_almacenes = VistaUnificadaAlamacenes(ventana_almacenes, self.controlador)
        vista_almacenes.mostrar_almacenes()

    def cerrar_sesion(self):
        """Cerrar sesión y volver al login"""
        self.root.withdraw()  # Ocultamos la ventana principal
        print("Sesión cerrada, volver al login.")
