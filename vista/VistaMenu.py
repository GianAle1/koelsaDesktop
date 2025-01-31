import tkinter as tk
from tkinter import messagebox
from vista.VistaUnificadaMarcas import VistaUnificadaMarcas
from vista.VistaUnificadaProveedores import VistaUnificadaProveedores
from vista.VistaProducto import VistaProducto
from vista.VistaUnificadaAlamacenes import VistaUnificadaAlamacenes
from vista.VistaProductos import VistaProductos
from vista.VistaEntrada import VistaEntrada
from vista.VistaSalida import VistaSalida
from vista.VistaRequerimiento import VistaRequerimiento
from vista.VistaRequerimientos import VistaRequerimientos
from vista.VistaBacklog import VistaBacklog
from vista.VistaFamilia import VistaFamilia
from tkinter.font import Font

class VistaMenu:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Menú Principal - Koelsa SRL")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        self.root.config(bg="#E3F2FD")  # Fondo azul claro suave

        # Fuentes personalizadas
        self.titulo_fuente = Font(family="Arial", size=20, weight="bold")
        self.boton_fuente = Font(family="Arial", size=12, weight="bold")

        # Título
        self.titulo_label = tk.Label(
            self.root, text="📌 Menú Principal",
            font=self.titulo_fuente, bg="#1565C0", fg="white", pady=15
        )
        self.titulo_label.pack(fill=tk.X)

        # Frame para organizar los botones
        self.frame_botones = tk.Frame(self.root, bg="#E3F2FD")
        self.frame_botones.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Botones principales organizados en una cuadrícula
        botones = [
            ("📦 Marcas", self.abrir_ventana_marcas, "#4CAF50"),
            ("🤝 Proveedores", self.abrir_ventana_proveedores, "#2196F3"),
            ("🏢 Almacenes", self.abrir_ventana_almacenes, "#673AB7"),
            ("🏷️ Familias", self.abrir_ventana_familias, "#8D6E63"),
            ("📊 Inventario", self.abrir_ventana_inventario, "#FF9800"),
            ("🛒 Productos", self.abrir_ventana_productos, "#009688"),
            ("📥 Entrada", self.abrir_ventana_entrada_productos, "#FFC107"),
            ("📤 Salida", self.abrir_ventana_salida_productos, "#FF5722"),
            ("📋 Requerimientos", self.abrir_ventana_requerimiento, "#3F51B5"),
            ("📃 Listar Requerimientos", self.abrir_ventana_requerimientos, "#007ACC"),
            ("🗂 Backlogs", self.abrir_ventana_backlogs, "#795548"),
            ("🚪 Cerrar Sesión", self.cerrar_sesion, "#f44336"),
        ]

        # Crear botones en una cuadrícula dinámica
        for row in range(3):  # Tres filas
            for col in range(4):  # Cuatro columnas
                index = row * 4 + col
                if index < len(botones):
                    texto, comando, color = botones[index]
                    boton = tk.Button(
                        self.frame_botones, text=texto, font=self.boton_fuente,
                        bg=color, fg="white", command=comando, width=20, height=2,
                        relief="raised", bd=3, cursor="hand2"
                    )
                    boton.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                    boton.bind("<Enter>", lambda e, btn=boton: btn.config(bg="#37474F"))
                    boton.bind("<Leave>", lambda e, btn=boton: btn.config(bg=color))

        # Expandir las celdas de la cuadrícula para que ocupen el espacio disponible
        for row in range(3):
            self.frame_botones.rowconfigure(row, weight=1)
        for col in range(4):
            self.frame_botones.columnconfigure(col, weight=1)

    def mostrar_menu(self):
        """Este método asegura que el menú sea visible."""
        self.root.deiconify()

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

    def abrir_ventana_salida_productos(self):
        ventana_salida = tk.Toplevel(self.root)
        vista_salida = VistaSalida(ventana_salida, self.controlador)

    def abrir_ventana_requerimiento(self):
        ventana_requerimiento = tk.Toplevel(self.root)
        vista_requerimiento = VistaRequerimiento(ventana_requerimiento, self.controlador)
        vista_requerimiento.mostrar_requerimiento()

    def abrir_ventana_requerimientos(self):
        ventana_requerimientos = tk.Toplevel(self.root)
        vista_requerimientos = VistaRequerimientos(ventana_requerimientos, self.controlador)
        vista_requerimientos.mostrar_requerimientos()

    def abrir_ventana_backlogs(self):
        ventana_backlogs = tk.Toplevel(self.root)
        vista_backlog = VistaBacklog(ventana_backlogs, self.controlador)
        vista_backlog.mostrar_backlogs()

    def abrir_ventana_familias(self):
        ventana_familias = tk.Toplevel(self.root)
        vista_familias = VistaFamilia(ventana_familias, self.controlador)
        vista_familias.mostrar_familia()

    def cerrar_sesion(self):
        """Confirma el cierre de sesión antes de cerrar la aplicación."""
        confirmacion = messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?")
        if confirmacion:
            self.root.withdraw()
            print("Sesión cerrada, volver al login.")
