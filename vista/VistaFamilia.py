# vista/vista_familia.py
import tkinter as tk
from tkinter import ttk, messagebox

class VistaFamilia:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Registrar Familia")
        self.root.geometry("600x400")
        self.root.configure(bg="#f4f4f9")

        # Título
        self.titulo_label = tk.Label(
            self.root, text="Registro de Familias",
            font=("Arial", 18, "bold"), bg="#4CAF50", fg="white", pady=10
        )
        self.titulo_label.pack(fill=tk.X)

        # Frame de Entrada
        self.frame_entrada = tk.Frame(self.root, bg="#f4f4f9", padx=10, pady=10)
        self.frame_entrada.pack(fill=tk.X)

        # Nombre de Familia
        tk.Label(self.frame_entrada, text="Nombre de la Familia:", font=("Arial", 12), bg="#f4f4f9").grid(row=0, column=0, sticky="w", padx=5)
        self.familia_entry = tk.Entry(self.frame_entrada, font=("Arial", 12), width=30)
        self.familia_entry.grid(row=0, column=1, padx=5)

        # Botón para agregar familia
        self.agregar_button = tk.Button(
            self.frame_entrada, text="Agregar", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.agregar_familia
        )
        self.agregar_button.grid(row=0, column=2, padx=5)

        # Tabla para listar las familias
        self.frame_tabla = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        self.frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas = ("ID", "Nombre")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", height=10)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre de la Familia")

        self.tree.column("ID", anchor="center", width=50)
        self.tree.column("Nombre", anchor="center", width=300)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Botón para eliminar familia
        self.eliminar_button = tk.Button(
            self.root, text="Eliminar Familia", font=("Arial", 12), bg="#f44336", fg="white", command=self.eliminar_familia
        )
        self.eliminar_button.pack(pady=10)

        # Cargar familias en la tabla
        self.cargar_familias()

    def agregar_familia(self):
        """Agrega una nueva familia a la base de datos."""
        nombre_familia = self.familia_entry.get().strip()

        if not nombre_familia:
            messagebox.showerror("Error", "El nombre de la familia no puede estar vacío.")
            return

        exito = self.controlador.registrar_familia(nombre_familia)
        if exito:
            messagebox.showinfo("Éxito", "Familia registrada correctamente.")
            self.familia_entry.delete(0, tk.END)
            self.cargar_familias()
        else:
            messagebox.showerror("Error", "Ocurrió un error al registrar la familia.")

    def cargar_familias(self):
        """Carga las familias desde la base de datos y las muestra en la tabla."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        familias = self.controlador.listar_familias()
        for familia in familias:
            self.tree.insert("", tk.END, values=familia)

    def eliminar_familia(self):
        """Elimina la familia seleccionada."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Debe seleccionar una familia para eliminar.")
            return

        id_familia = self.tree.item(selected_item[0])["values"][0]

        confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar esta familia?")
        if confirmacion:
            exito = self.controlador.eliminar_familia(id_familia)
            if exito:
                messagebox.showinfo("Éxito", "Familia eliminada correctamente.")
                self.cargar_familias()
            else:
                messagebox.showerror("Error", "Ocurrió un error al eliminar la familia.")

    def mostrar_familia(self):
        self.root.mainloop()
