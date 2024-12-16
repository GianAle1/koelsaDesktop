import tkinter as tk
from vista.VistaUnificadaMarcas import VistaUnificadaMarcas
from vista.VistaUnificadaProveedores import VistaUnificadaProveedores
class VistaMenu:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Menú Principal Koelsa SRL")

        # Configuración de la ventana principal
        self.root.geometry("500x500")  # Aumento el tamaño de la ventana
        self.root.resizable(False, False)  # Evita que se pueda redimensionar

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

        # Botón de gestión de Productos
        self.productos_button = tk.Button(self.frame, text="Gestionar Productos", width=25, height=2, font=("Arial", 12), 
                                          bg="#FF5722", fg="white", command=self.abrir_ventana_productos, relief="flat")
        self.productos_button.grid(row=3, column=0, pady=15, padx=10)

        # Botón de Logout (salir)
        self.logout_button = tk.Button(self.frame, text="Cerrar Sesión", width=25, height=2, font=("Arial", 12),
                                       bg="#f44336", fg="white", command=self.cerrar_sesion, relief="flat")
        self.logout_button.grid(row=4, column=0, pady=20, padx=10)

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
        vista_proveedores = VistaUnificadaProveedores(ventana_proveedores, self.controlador)  # Crear vista de proveedores
        vista_proveedores.mostrar_proveedores()  # Llamamos al método para mostrar los proveedores

    def abrir_ventana_productos(self):
        """Abre la ventana de gestión de productos"""
        print("Ventana de Productos (pendiente de implementación)")  # Aquí agregarías la lógica de productos.

    def cerrar_sesion(self):
        """Cerrar sesión y volver al login"""
        self.root.withdraw()  # Ocultamos la ventana principal
        print("Sesión cerrada, volver al login.")