import tkinter as tk
from tkinter import ttk, messagebox

class VistaEditarRequerimiento:
    def __init__(self, root, controlador, requerimiento):
        self.root = root
        self.controlador = controlador
        self.requerimiento = requerimiento

        self.root.title("Editar Requerimiento")
        self.root.geometry("1000x700")
        self.root.configure(bg="#e8f4f8")

        # Frame de Información del Requerimiento
        frame_info = tk.LabelFrame(self.root, text="Información del Requerimiento", font=("Arial", 14), bg="#e8f4f8", padx=10, pady=10)
        frame_info.pack(fill=tk.X, padx=10, pady=10)

        labels = ["ID", "Fecha", "Criterio", "Total"]
        self.entradas = []
        for i, label_text in enumerate(labels):
            label = tk.Label(frame_info, text=label_text, font=("Arial", 12), bg="#e8f4f8")
            label.grid(row=0, column=i * 2, padx=10, pady=10, sticky="w")

            entrada = tk.Entry(frame_info, font=("Arial", 12), width=20)
            entrada.grid(row=0, column=i * 2 + 1, padx=10, pady=10)
            entrada.insert(0, str(self.requerimiento[i]))
            if label_text == "ID":
                entrada.configure(state="readonly")
            self.entradas.append(entrada)

        # Sección de Productos Detallados
        frame_productos = tk.LabelFrame(self.root, text="Productos en Detalle", font=("Arial", 14), bg="#e8f4f8", padx=10, pady=10)
        frame_productos.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas = ("Producto", "Cantidad", "P. Unitario", "P.Total", "Uso", "Proveedor", "Maquinaria", "Almacen")
        self.tree_productos = ttk.Treeview(frame_productos, columns=columnas, show="headings", height=10)

        for col in columnas:
            self.tree_productos.heading(col, text=col)
            self.tree_productos.column(col, anchor="center", width=120)

        self.tree_productos.pack(fill=tk.BOTH, expand=True)

        # Cargar productos en el Treeview
        self.cargar_detalle_productos(self.requerimiento[0])

        # Evento de doble clic
        self.tree_productos.bind("<Double-1>", self.editar_producto)

        # Botones de acción
        frame_botones = tk.Frame(self.root, bg="#e8f4f8")
        frame_botones.pack(fill=tk.X, padx=10, pady=10)

        btn_guardar = tk.Button(frame_botones, text="Guardar", font=("Arial", 12, "bold"), bg="#007ACC", fg="white", command=self.guardar_cambios)
        btn_guardar.pack(side=tk.LEFT, padx=5)

        btn_cancelar = tk.Button(frame_botones, text="Cancelar", font=("Arial", 12, "bold"), bg="#D9534F", fg="white", command=self.root.destroy)
        btn_cancelar.pack(side=tk.LEFT, padx=5)

    def cargar_detalle_productos(self, id_requerimiento):
        """Carga los productos del detalle del requerimiento en el Treeview."""
        detalle_productos = self.controlador.obtener_detalle_requerimiento(id_requerimiento)

        for producto in detalle_productos:
            valores = [str(value) for value in producto]
            self.tree_productos.insert("", tk.END, values=valores)

    def editar_producto(self, event):
        """Abre una ventana para editar un producto seleccionado."""
        item = self.tree_productos.focus()
        if not item:
            messagebox.showwarning("Advertencia", "Selecciona un producto para editar.")
            return

        valores = self.tree_productos.item(item, "values")

        # Crear ventana de edición
        ventana_edicion = tk.Toplevel(self.root)
        ventana_edicion.title("Editar Producto")
        ventana_edicion.geometry("500x400")

        campos = ["Cantidad", "P. Unitario", "Proveedor"]
        entradas = []

        for i, campo in enumerate(campos):
            label = tk.Label(ventana_edicion, text=campo, font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")

            entrada = tk.Entry(ventana_edicion, font=("Arial", 12))
            entrada.grid(row=i, column=1, padx=10, pady=10)
            entrada.insert(0, valores[i + 1])  # Ajustar índice según la columna
            entradas.append(entrada)

        def guardar_producto():
            try:
                nueva_cantidad = entradas[0].get()
                nuevo_precio_unitario = entradas[1].get()
                nuevo_proveedor = entradas[2].get()

                # Actualizar los valores en el Treeview
                self.tree_productos.item(item, values=(
                    valores[0],  # Producto
                    nueva_cantidad,
                    nuevo_precio_unitario,
                    f"{float(nueva_cantidad) * float(nuevo_precio_unitario):.2f}",  # Nuevo precio total
                    valores[4],  # Uso
                    nuevo_proveedor,
                    valores[6],  # Maquinaria
                    valores[7]   # Almacén
                ))

                ventana_edicion.destroy()
                messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos para cantidad y precio unitario.")

        # Botones en la ventana de edición
        btn_guardar = tk.Button(ventana_edicion, text="Guardar", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=guardar_producto)
        btn_guardar.grid(row=len(campos), column=0, pady=20, padx=10)

        btn_cancelar = tk.Button(ventana_edicion, text="Cancelar", font=("Arial", 12, "bold"), bg="#f44336", fg="white", command=ventana_edicion.destroy)
        btn_cancelar.grid(row=len(campos), column=1, pady=20, padx=10)

    def guardar_cambios(self):
        """Guarda los cambios realizados en el requerimiento y sus detalles."""
        try:
            id_requerimiento = self.entradas[0].get()
            fecha = self.entradas[1].get()
            criterio = self.entradas[2].get()

            if not fecha or not criterio:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            # Recopilar datos de los productos desde el Treeview
            detalles_actualizados = []
            for item in self.tree_productos.get_children():
                valores = self.tree_productos.item(item, "values")
                detalles_actualizados.append(valores)

            # Llamar al controlador para actualizar el requerimiento
            exito = self.controlador.actualizar_requerimiento(id_requerimiento, fecha, criterio, detalles_actualizados)
            if exito:
                messagebox.showinfo("Éxito", "Requerimiento actualizado correctamente.")
                self.root.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el requerimiento.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar los cambios: {e}")
