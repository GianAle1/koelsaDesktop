import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

class VistaProducto:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Registrar Producto")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Frame para organizar el contenido
        self.frame = tk.Frame(self.root, bg="#f4f4f9")
        self.frame.pack(pady=30)

        # Título
        self.titulo_label = tk.Label(self.frame, text="Registrar Producto", font=("Arial", 16, "bold"), bg="#f4f4f9")
        self.titulo_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Campos para registrar producto
        self.partname_label = tk.Label(self.frame, text="Nombre del Producto:", font=("Arial", 12), bg="#f4f4f9")
        self.partname_label.grid(row=1, column=0, sticky="w", padx=10)
        self.partname_entry = tk.Entry(self.frame, width=40, font=("Arial", 12))
        self.partname_entry.grid(row=1, column=1)

        self.descripcion_label = tk.Label(self.frame, text="Descripción:", font=("Arial", 12), bg="#f4f4f9")
        self.descripcion_label.grid(row=2, column=0, sticky="w", padx=10)
        self.descripcion_entry = tk.Entry(self.frame, width=40, font=("Arial", 12))
        self.descripcion_entry.grid(row=2, column=1)

        self.undMedida_label = tk.Label(self.frame, text="Unidad de Medida:", font=("Arial", 12), bg="#f4f4f9")
        self.undMedida_label.grid(row=3, column=0, sticky="w", padx=10)
        self.undMedida_entry = tk.Entry(self.frame, width=40, font=("Arial", 12))
        self.undMedida_entry.grid(row=3, column=1)

        self.cantidad_label = tk.Label(self.frame, text="Cantidad:", font=("Arial", 12), bg="#f4f4f9")
        self.cantidad_label.grid(row=4, column=0, sticky="w", padx=10)
        self.cantidad_entry = tk.Entry(self.frame, width=40, font=("Arial", 12))
        self.cantidad_entry.grid(row=4, column=1)

        self.precio_label = tk.Label(self.frame, text="Precio:", font=("Arial", 12), bg="#f4f4f9")
        self.precio_label.grid(row=5, column=0, sticky="w", padx=10)
        self.precio_entry = tk.Entry(self.frame, width=40, font=("Arial", 12))
        self.precio_entry.grid(row=5, column=1)

        self.proveedor_label = tk.Label(self.frame, text="Proveedor:", font=("Arial", 12), bg="#f4f4f9")
        self.proveedor_label.grid(row=6, column=0, sticky="w", padx=10)
        self.proveedor_combobox = ttk.Combobox(self.frame, width=37, font=("Arial", 12))
        self.proveedor_combobox.grid(row=6, column=1)

        self.marca_label = tk.Label(self.frame, text="Marca:", font=("Arial", 12), bg="#f4f4f9")
        self.marca_label.grid(row=7, column=0, sticky="w", padx=10)
        self.marca_combobox = ttk.Combobox(self.frame, width=37, font=("Arial", 12))
        self.marca_combobox.grid(row=7, column=1)

        # Campo "Uso"
        self.uso_label = tk.Label(self.frame, text="Uso:", font=("Arial", 12), bg="#f4f4f9")
        self.uso_label.grid(row=8, column=0, sticky="w", padx=10)
        self.uso_entry = tk.Entry(self.frame, width=40, font=("Arial", 12))
        self.uso_entry.grid(row=8, column=1)

        # Campo "Equipo"
        self.equipo_label = tk.Label(self.frame, text="Equipo:", font=("Arial", 12), bg="#f4f4f9")
        self.equipo_label.grid(row=9, column=0, sticky="w", padx=10)
        self.equipo_entry = tk.Entry(self.frame, width=40, font=("Arial", 12))
        self.equipo_entry.grid(row=9, column=1)

        # Campo "Almacén"
        self.almacen_label = tk.Label(self.frame, text="Almacén:", font=("Arial", 12), bg="#f4f4f9")
        self.almacen_label.grid(row=10, column=0, sticky="w", padx=10)
        self.almacen_combobox = ttk.Combobox(self.frame, width=37, font=("Arial", 12))
        self.almacen_combobox.grid(row=10, column=1)

       
        # Llamar para listar proveedores y marcas
        self.listar_proveedores()  
        self.listar_marcas()  
        self.listar_almacenes()  
        # Botón para registrar el producto
        self.registrar_button = tk.Button(self.frame, text="Registrar Producto", font=("Arial", 12), command=self.registrar_producto, bg="#4CAF50", fg="white", relief="raised")
        self.registrar_button.grid(row=8, column=0, columnspan=2, pady=20)

    def mostrar_producto(self):
        """Muestra la ventana para gestionar producto"""
        self.root.mainloop()

    def listar_proveedores(self):
        """Carga la lista de proveedores en el ComboBox"""
        proveedores = self.controlador.listar_proveedores()
        proveedor_nombres = [proveedor[1] for proveedor in proveedores]
        self.proveedor_combobox['values'] = proveedor_nombres
        self.proveedor_combobox.current(0)

    def listar_marcas(self):
        """Carga la lista de marcas en el ComboBox"""
        marcas = self.controlador.listar_marcas()
        marca_nombres = [marca[1] for marca in marcas]
        self.marca_combobox['values'] = marca_nombres
        self.marca_combobox.current(0)
    def listar_almacenes(self):
        """Carga la lista de marcas en el ComboBox"""
        almacenes = self.controlador.listar_almacenes()
        almacen_nombres = [marca[1] for marca in almacenes]
        self.almacen_combobox['values'] = almacen_nombres
        self.almacen_combobox.current(0)

    def registrar_producto(self):
        nombre = self.partname_entry.get()
        descripcion = self.descripcion_entry.get()
        cantidad = self.cantidad_entry.get()
        precio = self.precio_entry.get()
        proveedor_seleccionado = self.proveedor_combobox.get()
        marca_seleccionada = self.marca_combobox.get()
        und_medida = self.undMedida_entry.get()  # Unidad de medida
        uso = self.uso_entry.get()  # Uso
        equipo = self.equipo_entry.get()  # Equipo
        almacen_seleccionado = self.almacen_combobox.get()  # Almacén seleccionado

        # Validación de campos
        if not nombre or not descripcion or not cantidad or not precio or not proveedor_seleccionado or not marca_seleccionada or not und_medida or not almacen_seleccionado:
            messagebox.showwarning("Advertencia", "Todos los campos deben ser completados.")
            return

        # Validación de cantidad y precio numéricos
        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showwarning("Advertencia", "La cantidad debe ser un número entero y el precio debe ser un número válido.")
            return

        # Obtener los IDs correspondientes a proveedor, marca y almacén
        proveedores = self.controlador.listar_proveedores()
        proveedor_id = next((proveedor[0] for proveedor in proveedores if proveedor[1] == proveedor_seleccionado), None)
        
        marcas = self.controlador.listar_marcas()
        marca_id = next((marca[0] for marca in marcas if marca[1] == marca_seleccionada), None)
        
        almacenes = self.controlador.listar_almacenes()
        almacen_id = next((almacen[0] for almacen in almacenes if almacen[1] == almacen_seleccionado), None)

        # Si los IDs son válidos, llamar al controlador
        if proveedor_id and marca_id and almacen_id:
            exito = self.controlador.registrar_producto(
                nombre, descripcion, cantidad, precio, proveedor_id, marca_id, almacen_id, und_medida, uso, equipo
            )
            if exito:
                messagebox.showinfo("Éxito", "Producto registrado con éxito.")
            else:
                messagebox.showerror("Error", "Hubo un problema al registrar el producto.")
        else:
            messagebox.showerror("Error", "Proveedor, Marca o Almacén no encontrados.")