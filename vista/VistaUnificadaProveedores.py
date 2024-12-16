# vista/VistaUnificadaProveedores.py
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

class VistaUnificadaProveedores:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Gestión de Proveedores")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Frame para organizar el contenido
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=30)

        # Título
        self.titulo_label = tk.Label(self.frame, text="Gestión de Proveedores", font=("Arial", 16, "bold"))
        self.titulo_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Botones de las operaciones CRUD
        self.registrar_proveedor_button = tk.Button(self.frame, text="Registrar Proveedor", width=20, height=2, font=("Arial", 12), command=self.registrar_proveedor)
        self.registrar_proveedor_button.grid(row=1, column=0, pady=10)

        self.eliminar_proveedor_button = tk.Button(self.frame, text="Eliminar Proveedor", width=20, height=2, font=("Arial", 12), command=self.eliminar_proveedor)
        self.eliminar_proveedor_button.grid(row=2, column=0, pady=10)

        self.listar_proveedor_button = tk.Button(self.frame, text="Listar Proveedores", width=20, height=2, font=("Arial", 12), command=self.listar_proveedores)
        self.listar_proveedor_button.grid(row=3, column=0, pady=10)

        self.salir_button = tk.Button(self.frame, text="Salir", width=20, height=2, font=("Arial", 12), command=self.salir)
        self.salir_button.grid(row=4, column=0, pady=20)

        # Treeview para listar proveedores dentro de la misma ventana
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nombre", "Dirección", "Teléfono", "Correo"), show="headings", height=6)
        self.tree.heading("ID", text="Código")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Dirección", text="Dirección")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Correo", text="Correo")
        self.tree.column("ID", width=100, anchor=tk.CENTER)
        self.tree.column("Nombre", width=200, anchor=tk.W)
        self.tree.column("Dirección", width=200, anchor=tk.W)
        self.tree.column("Teléfono", width=100, anchor=tk.CENTER)
        self.tree.column("Correo", width=150, anchor=tk.W)
        self.tree.grid(row=5, column=0, columnspan=2, pady=10)

    def registrar_proveedor(self):
        """Método para registrar un nuevo proveedor"""
        nombre = simpledialog.askstring("Registrar Proveedor", "Ingrese el nombre del proveedor:")
        direccion = simpledialog.askstring("Registrar Proveedor", "Ingrese la dirección del proveedor:")
        telefono = simpledialog.askstring("Registrar Proveedor", "Ingrese el teléfono del proveedor:")
        correo = simpledialog.askstring("Registrar Proveedor", "Ingrese el correo del proveedor:")

        if nombre and direccion and telefono and correo:
            proveedor_registrado = self.controlador.registrar_proveedor(nombre, direccion, telefono, correo)
            if proveedor_registrado:
                messagebox.showinfo("Éxito", "Proveedor registrado con éxito!")
                self.listar_proveedores()  # Refrescar lista de proveedores
            else:
                messagebox.showerror("Error", "Hubo un problema al registrar el proveedor.")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos deben ser llenados.")

    def eliminar_proveedor(self):
        """Método para eliminar un proveedor"""
        id_proveedor = simpledialog.askinteger("Eliminar Proveedor", "Ingrese el ID del proveedor a eliminar:")

        if id_proveedor:
            proveedor_eliminado = self.controlador.eliminar_proveedor(id_proveedor)
            if proveedor_eliminado:
                messagebox.showinfo("Éxito", "Proveedor eliminado con éxito!")
                self.listar_proveedores()  # Refrescar lista de proveedores
            else:
                messagebox.showerror("Error", "Hubo un problema al eliminar el proveedor.")
        else:
            messagebox.showwarning("Advertencia", "Debe ingresar un ID válido.")

    def listar_proveedores(self):
        """Método para listar los proveedores en la tabla"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        proveedores = self.controlador.obtener_proveedores()
        for proveedor in proveedores:
            self.tree.insert("", "end", values=proveedor)

    def salir(self):
        """Método para cerrar la ventana de proveedores"""
        self.root.destroy()