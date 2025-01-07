import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

class VistaUnificadaProveedores:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Gestión de Proveedores")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
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

        # Botones con íconos
        botones = [
            ("🆕 Registrar Proveedor", self.registrar_proveedor, "#007ACC"),
            ("❌ Eliminar Proveedor", self.eliminar_proveedor, "#FF5722"),
            ("📋 Listar Proveedores", self.listar_proveedores, "#4CAF50"),
            ("🚪 Salir", self.salir, "#f44336")
        ]

        for idx, (texto, comando, color) in enumerate(botones):
            boton = tk.Button(
                self.frame_botones,
                text=texto,
                font=("Arial", 12, "bold"),
                bg=color,
                fg="white",
                width=20,
                height=2,
                command=comando,
                relief="groove",
                bd=2
            )
            boton.grid(row=0, column=idx, padx=10, pady=10, sticky="nsew")
            # Hover Effect
            boton.bind("<Enter>", lambda e, btn=boton: btn.config(bg=self._hover_color(color)))
            boton.bind("<Leave>", lambda e, btn=boton: btn.config(bg=color))

        # Frame para la tabla
        self.frame_tabla = tk.Frame(self.frame, bg="white", bd=2, relief="ridge")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, pady=20)

        # Tabla de proveedores
        self.tree = ttk.Treeview(
            self.frame_tabla,
            columns=("ID", "Nombre", "Ruc", "Dirección", "Teléfono", "Correo"),
            show="headings",
            height=10
        )

        # Encabezados
        self.tree.heading("ID", text="Código")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Ruc", text="Ruc")
        self.tree.heading("Dirección", text="Dirección")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Correo", text="Correo")

        # Configurar columnas
        self.tree.column("ID", width=80, anchor=tk.CENTER)
        self.tree.column("Nombre", width=200, anchor=tk.W)
        self.tree.column("Ruc", width=200, anchor=tk.W)
        self.tree.column("Dirección", width=250, anchor=tk.W)
        self.tree.column("Teléfono", width=150, anchor=tk.CENTER)
        self.tree.column("Correo", width=200, anchor=tk.W)
        # Estilo de la tabla
        self.tree.tag_configure("oddrow", background="#f9f9f9")
        self.tree.tag_configure("evenrow", background="#e9e9e9")

        # Scrollbars para la tabla
        scroll_y = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self.frame_tabla, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _hover_color(self, color):
        """Calcula un color más oscuro para el hover."""
        import colorsys
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        l = max(0, l - 0.1)  # Reduce la luminosidad
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

    def mostrar_proveedores(self):
        """Muestra la ventana para gestionar proveedores."""
        self.root.mainloop()

    def registrar_proveedor(self):
        """Método para registrar un nuevo proveedor."""
        ruc = simpledialog.askstring("Registrar Proveedor", "Ingrese el RUC del proveedor:")
        nombre = simpledialog.askstring("Registrar Proveedor", "Ingrese el nombre del proveedor:")
        direccion = simpledialog.askstring("Registrar Proveedor", "Ingrese la dirección del proveedor:")
        telefono = simpledialog.askstring("Registrar Proveedor", "Ingrese el teléfono del proveedor:")
        correo = simpledialog.askstring("Registrar Proveedor", "Ingrese el correo del proveedor:")

        if nombre and direccion and telefono and correo:
            proveedor_registrado = self.controlador.registrar_proveedor(nombre, direccion, telefono, correo,ruc)
            if proveedor_registrado:
                messagebox.showinfo("Éxito", "Proveedor registrado con éxito!")
                self.listar_proveedores()  # Refrescar lista de proveedores
            else:
                messagebox.showerror("Error", "Hubo un problema al registrar el proveedor.")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos deben ser llenados.")

    def eliminar_proveedor(self):
        """Método para eliminar un proveedor."""
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
        """Actualizar la lista de marcas en el Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        if proveedores:
            for index, proveedor in enumerate(proveedores):
                tag = "oddrow" if index % 2 == 0 else "evenrow"
                self.tree.insert("", tk.END, values=(proveedor[0], proveedor[1], proveedor[2], proveedor[3], proveedor[4], proveedor[5]), tags=(tag,))
        else:
            self.tree.insert("", tk.END, values=("No se encontraron proveedores", "", "", "", ""), tags=("oddrow",))

    def salir(self):
        """Método para cerrar la ventana de proveedores."""
        self.root.destroy()
