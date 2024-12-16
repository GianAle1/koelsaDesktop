import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

class VistaUnificadaMarcas:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Gestión de Marcas")
        self.root.geometry("1000x800")
        self.root.resizable(False, False)
        self.root.config(bg="#f0f0f0")  # Fondo claro para toda la ventana

        # Frame para organizar el contenido
        self.frame = tk.Frame(self.root, bg="#f0f0f0")
        self.frame.pack(pady=30)

        # Título
        self.titulo_label = tk.Label(self.frame, text="Gestión de Marcas", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#4CAF50")
        self.titulo_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Botones de las operaciones CRUD con nuevos estilos
        self.registrar_marca_button = tk.Button(self.frame, text="Registrar Marca", width=25, height=2, font=("Arial", 12), 
                                                bg="#4CAF50", fg="white", command=self.registrar_marca, relief="flat")
        self.registrar_marca_button.grid(row=1, column=0, pady=15, padx=10)

        self.eliminar_marca_button = tk.Button(self.frame, text="Eliminar Marca", width=25, height=2, font=("Arial", 12), 
                                               bg="#FF5722", fg="white", command=self.eliminar_marca, relief="flat")
        self.eliminar_marca_button.grid(row=2, column=0, pady=15, padx=10)

        self.listar_marca_button = tk.Button(self.frame, text="Listar Marcas", width=25, height=2, font=("Arial", 12), 
                                             bg="#2196F3", fg="white", command=self.listar_marcas, relief="flat")
        self.listar_marca_button.grid(row=3, column=0, pady=15, padx=10)

        self.salir_button = tk.Button(self.frame, text="Salir", width=25, height=2, font=("Arial", 12), 
                                      bg="#f44336", fg="white", command=self.salir, relief="flat")
        self.salir_button.grid(row=4, column=0, pady=20, padx=10)

        # Treeview para listar marcas con bordes, mejora visual y ancho ajustado
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nombre"), show="headings", height=10)
        self.tree.heading("ID", text="Código")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.column("ID", width=100, anchor=tk.CENTER)
        self.tree.column("Nombre", width=300, anchor=tk.W)
        self.tree.grid(row=5, column=0, columnspan=2, pady=20)

        # Estilo de la tabla
        self.tree.tag_configure("oddrow", background="#f9f9f9")
        self.tree.tag_configure("evenrow", background="#e9e9e9")

    def mostrar_marcas(self):
        """Muestra la ventana para gestionar las marcas"""
        self.root.mainloop()

    def registrar_marca(self):
        """Método para registrar una nueva marca"""
        # Pedir al usuario el nombre de la marca mediante un cuadro de entrada
        nombre_marca = simpledialog.askstring("Registrar Marca", "Ingrese el nombre de la marca:")

        # Validar si el usuario ha proporcionado un nombre
        if nombre_marca:
            marcas = self.controlador.registrar_marca(nombre_marca)
            if marcas is not None:
                messagebox.showinfo("Éxito", "Marca registrada con éxito!")
                self.actualizar_lista_marcas(marcas)  # Actualizar la lista después de registrar
            else:
                messagebox.showerror("Error", "Hubo un problema al registrar la marca.")
        else:
            messagebox.showwarning("Advertencia", "El nombre de la marca no puede estar vacío.")

    def eliminar_marca(self):
        """Método para eliminar una marca"""
        # Pedir al usuario el ID de la marca a eliminar
        id_marca = simpledialog.askinteger("Eliminar Marca", "Ingrese el ID de la marca a eliminar:")

        if id_marca:
            marcas = self.controlador.eliminar_marca(id_marca)
            if marcas is not None:
                messagebox.showinfo("Éxito", "Marca eliminada con éxito!")
                self.actualizar_lista_marcas(marcas)  # Actualizar la lista después de eliminar
            else:
                messagebox.showerror("Error", "Hubo un problema al eliminar la marca.")
        else:
            messagebox.showwarning("Advertencia", "Debe ingresar un ID válido.")

    def listar_marcas(self):
        """Método para listar todas las marcas"""
        marcas = self.controlador.listar_marcas()
        if marcas:
            self.actualizar_lista_marcas(marcas)

    def actualizar_lista_marcas(self, marcas):
        """Actualizar la lista de marcas en el Treeview"""
        # Limpiar las filas de la tabla antes de agregar nuevas
        for row in self.tree.get_children():
            self.tree.delete(row)

        if marcas:
            # Insertar cada marca como una fila en la tabla
            for index, marca in enumerate(marcas):
                tag = "oddrow" if index % 2 == 0 else "evenrow"
                self.tree.insert("", tk.END, values=(marca[0], marca[1]), tags=(tag,))
        else:
            # Si no hay marcas, mostrar un mensaje en la tabla
            self.tree.insert("", tk.END, values=("No se encontraron marcas", ""), tags=("oddrow",))

    def salir(self):
        """Método para salir de la aplicación"""
        self.root.quit()
