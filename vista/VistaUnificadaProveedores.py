import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

class VistaUnificadaProveedores:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Gestión de Proveedores")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.config(bg="#e8f4f8")  # Fondo azul claro

        # Frame principal
        self.frame = tk.Frame(self.root, bg="#e8f4f8", pady=20)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Título estilizado
        self.titulo_label = tk.Label(
            self.frame, 
            text="Gestión de Proveedores", 
            font=("Arial", 18, "bold"), 
            bg="#007ACC", 
            fg="white", 
            pady=10
        )
        self.titulo_label.pack(fill=tk.X, pady=(0, 20))

        # Frame para botones
        self.frame_botones = tk.Frame(self.frame, bg="#e8f4f8")
        self.frame_botones.pack(pady=10)

        # Botones estilizados
        boton_estilo = {
            "width": 20,
            "height": 2,
            "font": ("Arial", 12),
            "bg": "#007ACC",
            "fg": "white",
            "relief": "groove",
            "bd": 2
        }

        self.registrar_proveedor_button = tk.Button(
            self.frame_botones, 
            text="Registrar Proveedor", 
            command=self.registrar_proveedor,
            **boton_estilo
        )
        self.registrar_proveedor_button.grid(row=0, column=0, padx=10, pady=10)

        self.eliminar_proveedor_button = tk.Button(
            self.frame_botones, 
            text="Eliminar Proveedor", 
            command=self.eliminar_proveedor,
            **boton_estilo
        )
        self.eliminar_proveedor_button.grid(row=0, column=1, padx=10, pady=10)

        self.listar_proveedor_button = tk.Button(
            self.frame_botones, 
            text="Listar Proveedores", 
            command=self.listar_proveedores,
            **boton_estilo
        )
        self.listar_proveedor_button.grid(row=0, column=2, padx=10, pady=10)

        self.salir_button = tk.Button(
            self.frame_botones, 
            text="Salir", 
            command=self.salir,
            **boton_estilo
        )
        self.salir_button.grid(row=0, column=3, padx=10, pady=10)

        # Frame para la tabla
        self.frame_tabla = tk.Frame(self.frame, bg="white", bd=2, relief="ridge")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, pady=20)

        # Tabla de proveedores
        self.tree = ttk.Treeview(
            self.frame_tabla, 
            columns=("ID", "Nombre", "Dirección", "Teléfono", "Correo"), 
            show="headings", 
            height=10
        )

        # Encabezados
        self.tree.heading("ID", text="Código")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Dirección", text="Dirección")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Correo", text="Correo")

        # Configurar columnas
        self.tree.column("ID", width=80, anchor=tk.CENTER)
        self.tree.column("Nombre", width=200, anchor=tk.W)
        self.tree.column("Dirección", width=250, anchor=tk.W)
        self.tree.column("Teléfono", width=150, anchor=tk.CENTER)
        self.tree.column("Correo", width=200, anchor=tk.W)

        # Scrollbars para la tabla
        scroll_y = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self.frame_tabla, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def mostrar_proveedores(self):
        """Muestra la ventana para gestionar proveedores"""
        self.root.mainloop()

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
                self.listar_proveedores() 
            else:
                messagebox.showerror("Error", "Hubo un problema al eliminar el proveedor.")
        else:
            messagebox.showwarning("Advertencia", "Debe ingresar un ID válido.")

    def listar_proveedores(self):
        proveedores = self.controlador.listar_proveedores()
        if proveedores:
            self.actualizar_lista_proveedores(proveedores)
    
    def actualizar_lista_proveedores(self, proveedores):
        """Actualizar la lista de marcas en el Treeview"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        if proveedores:
            for index, proveedor in enumerate(proveedores):
                tag = "oddrow" if index % 2 == 0 else "evenrow"
                self.tree.insert("", tk.END, values=(proveedor[0], proveedor[1], proveedor[2], proveedor[3], proveedor[4]), tags=(tag,))
        else:
            self.tree.insert("", tk.END, values=("No se encontraron marcas", ""), tags=("oddrow",))

    def salir(self):
        """Método para cerrar la ventana de proveedores"""
        self.root.destroy()
