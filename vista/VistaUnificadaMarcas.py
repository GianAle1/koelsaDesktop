import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from tkinter.font import Font

class VistaUnificadaMarcas:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Gestión de Marcas")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.config(bg="#ffffff")  # Fondo blanco

        # Fuentes personalizadas
        self.titulo_fuente = Font(family="Arial", size=20, weight="bold")
        self.boton_fuente = Font(family="Arial", size=12, weight="bold")

        # Frame principal
        self.frame_principal = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Título
        self.titulo_label = tk.Label(
            self.frame_principal, text="Gestión de Marcas", font=self.titulo_fuente,
            bg="#ffffff", fg="#4CAF50", pady=10
        )
        self.titulo_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

        # Botones CRUD
        self.botones_frame = tk.Frame(self.frame_principal, bg="#ffffff")
        self.botones_frame.grid(row=1, column=0, sticky="nsew", pady=10, padx=10)

        # Lista de botones con íconos
        botones = [
            ("🆕 Registrar Marca", self.registrar_marca, "#4CAF50"),
            ("❌ Eliminar Marca", self.eliminar_marca, "#FF5722"),
            ("📋 Listar Marcas", self.listar_marcas, "#2196F3"),
            ("🚪 Salir", self.salir, "#f44336"),
        ]

        for idx, (texto, comando, color) in enumerate(botones):
            boton = tk.Button(
                self.botones_frame, text=texto, font=self.boton_fuente,
                bg=color, fg="white", width=25, height=2, command=comando, relief="flat", bd=3
            )
            boton.grid(row=idx, column=0, pady=5, padx=5, sticky="nsew")
            # Hover Effect
            boton.bind("<Enter>", lambda e, btn=boton: btn.config(bg=self._hover_color(color)))
            boton.bind("<Leave>", lambda e, btn=boton: btn.config(bg=color))

        # Tabla de Marcas
        self.tabla_frame = tk.Frame(self.frame_principal, bg="#ffffff")
        self.tabla_frame.grid(row=1, column=1, sticky="nsew", pady=10, padx=10)

        self.tree = ttk.Treeview(self.tabla_frame, columns=("ID", "Nombre"), show="headings", height=15)
        self.tree.heading("ID", text="Código")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.column("ID", width=100, anchor=tk.CENTER)
        self.tree.column("Nombre", width=300, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Estilo de la tabla
        self.tree.tag_configure("oddrow", background="#f9f9f9")
        self.tree.tag_configure("evenrow", background="#e9e9e9")

        # Expandir frames al redimensionar ventana
        self.frame_principal.grid_rowconfigure(1, weight=1)
        self.frame_principal.grid_columnconfigure(1, weight=1)

    def _hover_color(self, color):
        """Calcula un color más oscuro para el hover."""
        import colorsys
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        l = max(0, l - 0.1)  # Reduce la luminosidad
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

    def mostrar_marcas(self):
        """Muestra la ventana para gestionar las marcas."""
        self.root.mainloop()

    def registrar_marca(self):
        """Método para registrar una nueva marca."""
        nombre_marca = simpledialog.askstring("Registrar Marca", "Ingrese el nombre de la marca:")
        if nombre_marca:
            marcas = self.controlador.registrar_marca(nombre_marca)
            if marcas:
                messagebox.showinfo("Éxito", "Marca registrada con éxito!")
                self.actualizar_lista_marcas(marcas)
            else:
                messagebox.showerror("Error", "Hubo un problema al registrar la marca.")
        else:
            messagebox.showwarning("Advertencia", "El nombre de la marca no puede estar vacío.")

    def eliminar_marca(self):
        """Método para eliminar una marca."""
        id_marca = simpledialog.askinteger("Eliminar Marca", "Ingrese el ID de la marca a eliminar:")
        if id_marca:
            marcas = self.controlador.eliminar_marca(id_marca)
            if marcas:
                messagebox.showinfo("Éxito", "Marca eliminada con éxito!")
                self.actualizar_lista_marcas(marcas)
            else:
                messagebox.showerror("Error", "Hubo un problema al eliminar la marca.")
        else:
            messagebox.showwarning("Advertencia", "Debe ingresar un ID válido.")

    def listar_marcas(self):
        """Método para listar todas las marcas."""
        marcas = self.controlador.listar_marcas()
        self.actualizar_lista_marcas(marcas)

    def actualizar_lista_marcas(self, marcas):
        """Actualizar la lista de marcas en el Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        if marcas:
            for index, marca in enumerate(marcas):
                tag = "oddrow" if index % 2 == 0 else "evenrow"
                self.tree.insert("", tk.END, values=(marca[0], marca[1]), tags=(tag,))

    def salir(self):
        """Método para salir de la aplicación."""
        self.root.quit()
