import tkinter as tk
from tkinter import ttk

class VistaEditarRequerimiento:
    def __init__(self, root, controlador, requerimiento):
        self.root = root
        self.controlador = controlador
        self.requerimiento = requerimiento  # Datos del requerimiento a editar

        self.root.title("Editar Requerimiento")
        self.root.geometry("800x600")
        self.root.configure(bg="#e8f4f8")

        # Sección de datos principales del requerimiento
        labels = ["ID", "Fecha", "Criterio", "Total"]
        self.entradas = []
        for i, label_text in enumerate(labels):
            label = tk.Label(self.root, text=label_text, font=("Arial", 12), bg="#e8f4f8")
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")
            
            entrada = tk.Entry(self.root, font=("Arial", 12))
            entrada.grid(row=i, column=1, padx=10, pady=10)
            entrada.insert(0, str(self.requerimiento[i]))  # Colocar el valor actual en la entrada
            if label_text == "ID":  # Hacer que el campo de ID sea de solo lectura
                entrada.configure(state="readonly")
            self.entradas.append(entrada)

        # Sección de productos en requerimientoDetalle
        label_productos = tk.Label(self.root, text="Productos en Detalle", font=("Arial", 14, "bold"), bg="#e8f4f8")
        label_productos.grid(row=len(labels), column=0, columnspan=2, pady=10)

        self.frame_productos = tk.Frame(self.root, bg="white", bd=2, relief="ridge")
        self.frame_productos.grid(row=len(labels) + 1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        columnas = ("ID Producto", "Descripción", "Cantidad", "Precio Unitario", "Precio Total")
        self.tree_productos = ttk.Treeview(self.frame_productos, columns=columnas, show="headings", height=10)
        
        for col in columnas:
            self.tree_productos.heading(col, text=col)
            self.tree_productos.column(col, anchor="center", width=150)

        self.tree_productos.pack(fill=tk.BOTH, expand=True)

        # Cargar productos del detalle
        self.cargar_detalle_productos()

        # Botones
        btn_guardar = tk.Button(
            self.root, text="Guardar", font=("Arial", 12, "bold"), bg="#007ACC", fg="white", command=self.guardar_cambios
        )
        btn_guardar.grid(row=len(labels) + 2, column=0, pady=20, padx=10)

        btn_cancelar = tk.Button(
            self.root, text="Cancelar", font=("Arial", 12, "bold"), bg="#D9534F", fg="white", command=self.root.destroy
        )
        btn_cancelar.grid(row=len(labels) + 2, column=1, pady=20, padx=10)

    def cargar_detalle_productos(self):
        """Carga los productos del detalle del requerimiento en el Treeview."""
        id_requerimiento = self.requerimiento[0]  # ID del requerimiento seleccionado
        detalle_productos = self.controlador.obtener_detalle_requerimiento(id_requerimiento)

        for producto in detalle_productos:
            # Sanitiza los valores reemplazando comas con otro carácter, como punto y coma (;)
            valores = tuple(str(value).replace(",", ";") if value is not None else "" for value in producto)
            self.tree_productos.insert("", tk.END, values=valores)

    def guardar_cambios(self):
        """Guarda los cambios en los datos principales y el detalle."""
        id_requerimiento = self.entradas[0].get()
        fecha = self.entradas[1].get()
        criterio = self.entradas[2].get()

        # Aquí se actualizarían los datos principales en la base de datos
        print(f"Guardando requerimiento: ID={id_requerimiento}, Fecha={fecha}, Criterio={criterio}")

        # Actualizar detalles (Ejemplo)
        for item in self.tree_productos.get_children():
            valores = self.tree_productos.item(item, "values")
            print(f"Actualizando producto: {valores}")

        self.root.destroy()
