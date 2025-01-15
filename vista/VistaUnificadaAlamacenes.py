import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

class VistaUnificadaAlamacenes:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Gestión de Almacenes")
        self.root.geometry("1000x800")
        self.root.resizable(False, False)
        self.root.config(bg="#f0f0f0")  # Fondo claro para toda la ventana

        # Frame para organizar el contenido
        self.frame = tk.Frame(self.root, bg="#f0f0f0")
        self.frame.pack(pady=30)

        # Título
        self.titulo_label = tk.Label(self.frame, text="Gestión de Almacenes", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#4CAF50")
        self.titulo_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Botones de las operaciones CRUD con nuevos estilos
        self.registrar_button = tk.Button(self.frame, text="Registrar Almacén", width=25, height=2, font=("Arial", 12), 
                                          bg="#4CAF50", fg="white", command=self.registrar_alamcen, relief="flat")
        self.registrar_button.grid(row=1, column=0, pady=15, padx=10)

        self.eliminar_button = tk.Button(self.frame, text="Eliminar Almacén", width=25, height=2, font=("Arial", 12), 
                                         bg="#FF5722", fg="white", command=self.eliminar_alamacen, relief="flat")
        self.eliminar_button.grid(row=2, column=0, pady=15, padx=10)

        self.listar_button = tk.Button(self.frame, text="Listar Almacenes", width=25, height=2, font=("Arial", 12), 
                                       bg="#2196F3", fg="white", command=self.listar_almacenes, relief="flat")
        self.listar_button.grid(row=3, column=0, pady=15, padx=10)

        self.salir_button = tk.Button(self.frame, text="Salir", width=25, height=2, font=("Arial", 12), 
                                      bg="#f44336", fg="white", command=self.salir, relief="flat")
        self.salir_button.grid(row=4, column=0, pady=20, padx=10)

        # Treeview para listar almacenes con bordes, mejora visual y ancho ajustado
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Nombre", "Direccion", "Capacidad"), show="headings", height=10)
        self.tree.heading("ID", text="Código")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Direccion", text="Dirección")
        self.tree.heading("Capacidad", text="Capacidad")
        self.tree.column("ID", width=100, anchor=tk.CENTER)
        self.tree.column("Nombre", width=300, anchor=tk.W)
        self.tree.column("Direccion", width=300, anchor=tk.W)
        self.tree.column("Capacidad", width=200, anchor=tk.W)
        self.tree.grid(row=5, column=0, columnspan=2, pady=20)

        # Estilo de la tabla
        self.tree.tag_configure("oddrow", background="#f9f9f9")
        self.tree.tag_configure("evenrow", background="#e9e9e9")

    def mostrar_almacenes(self):
        """Muestra la ventana para gestionar los almacenes."""
        self.root.mainloop()

    def registrar_alamcen(self):
        """Método para registrar un nuevo almacén."""
        nombre = simpledialog.askstring("Registrar Almacén", "Ingrese el nombre del almacén:")
        direccion = simpledialog.askstring("Registrar Almacén", "Ingrese la dirección del almacén:")
        capacidad = simpledialog.askinteger("Registrar Almacén", "Ingrese la capacidad del almacén:")

        if nombre and direccion and capacidad is not None:
            almacenes = self.controlador.registrar_almacen(nombre, direccion, capacidad)
            if almacenes is not None:
                messagebox.showinfo("Éxito", "Almacén registrado con éxito!")
                self.actualizar_lista_almacenes(almacenes)
            else:
                messagebox.showerror("Error", "Hubo un problema al registrar el almacén.")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def eliminar_alamacen(self):
        """Método para eliminar un almacén."""
        id_almacen = simpledialog.askinteger("Eliminar Almacén", "Ingrese el ID del almacén a eliminar:")

        if id_almacen:
            almacenes = self.controlador.eliminar_almacen(id_almacen)
            if almacenes is not None:
                messagebox.showinfo("Éxito", "Almacén eliminado con éxito!")
                self.actualizar_lista_almacenes(almacenes)
            else:
                messagebox.showerror("Error", "Hubo un problema al eliminar el almacén.")
        else:
            messagebox.showwarning("Advertencia", "Debe ingresar un ID válido.")

    def listar_almacenes(self):
        """Método para listar todos los almacenes."""
        almacenes = self.controlador.listar_almacenes()
        self.actualizar_lista_almacenes(almacenes)

    def actualizar_lista_almacenes(self, almacenes):
        """Actualizar la lista de almacenes en el Treeview."""
        # Limpiar las filas de la tabla antes de agregar nuevas
        for row in self.tree.get_children():
            self.tree.delete(row)

        if almacenes:
            # Insertar cada almacén como una fila en la tabla
            for index, almacen in enumerate(almacenes):
                tag = "oddrow" if index % 2 == 0 else "evenrow"
                self.tree.insert("", tk.END, values=(almacen[0], almacen[1], almacen[2], almacen[3]), tags=(tag,))
        else:
            # Si no hay almacenes, mostrar un mensaje en la tabla
            self.tree.insert("", tk.END, values=("No se encontraron almacenes", "", "", ""), tags=("oddrow",))

    def salir(self):
        """Método para salir de la aplicación."""
        self.root.quit()
