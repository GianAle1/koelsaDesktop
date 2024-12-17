import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

class VistaProducto:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Registrar Producto")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Fondo personalizado
        self.frame = tk.Frame(self.root, bg="#f4f4f9")
        self.frame.pack(pady=30)

        # Título
        self.titulo_label = tk.Label(self.frame, text="Registrar Producto", font=("Arial", 18, "bold"), bg="#f4f4f9", fg="#333333")
        self.titulo_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Campos para registrar producto
        self.partname_label = tk.Label(self.frame, text="Part name:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.partname_label.grid(row=1, column=0, sticky="w", padx=15, pady=5)
        self.partname_entry = tk.Entry(self.frame, width=40, font=("Arial", 12), relief="solid", bd=2)
        self.partname_entry.grid(row=1, column=1, pady=5)

        self.descripcion_label = tk.Label(self.frame, text="Descripción:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.descripcion_label.grid(row=2, column=0, sticky="w", padx=15, pady=5)
        self.descripcion_entry = tk.Entry(self.frame, width=40, font=("Arial", 12), relief="solid", bd=2)
        self.descripcion_entry.grid(row=2, column=1, pady=5)

        self.undMedida_label = tk.Label(self.frame, text="Unidad de Medida:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.undMedida_label.grid(row=3, column=0, sticky="w", padx=15, pady=5)
        self.unidadMedida_combobox = ttk.Combobox(self.frame, width=40, font=("Arial", 12), state="readonly")  # Combobox solo lectura
        self.unidadMedida_combobox.grid(row=3, column=1, pady=5)

        self.cantidad_label = tk.Label(self.frame, text="Cantidad:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.cantidad_label.grid(row=4, column=0, sticky="w", padx=15, pady=5)
        self.cantidad_entry = tk.Entry(self.frame, width=40, font=("Arial", 12), relief="solid", bd=2)
        self.cantidad_entry.grid(row=4, column=1, pady=5)

        self.precio_label = tk.Label(self.frame, text="Precio:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.precio_label.grid(row=5, column=0, sticky="w", padx=15, pady=5)
        self.precio_entry = tk.Entry(self.frame, width=40, font=("Arial", 12), relief="solid", bd=2)
        self.precio_entry.grid(row=5, column=1, pady=5)

        self.proveedor_label = tk.Label(self.frame, text="Proveedor:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.proveedor_label.grid(row=6, column=0, sticky="w", padx=15, pady=5)
        self.proveedor_combobox = ttk.Combobox(self.frame, width=40, font=("Arial", 12), state="readonly")  # Combobox solo lectura
        self.proveedor_combobox.grid(row=6, column=1, pady=5)

        self.marca_label = tk.Label(self.frame, text="Marca:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.marca_label.grid(row=7, column=0, sticky="w", padx=15, pady=5)
        self.marca_combobox = ttk.Combobox(self.frame, width=40, font=("Arial", 12), state="readonly")  # Combobox solo lectura
        self.marca_combobox.grid(row=7, column=1, pady=5)

        self.uso_label = tk.Label(self.frame, text="Uso:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.uso_label.grid(row=8, column=0, sticky="w", padx=15, pady=5)
        self.uso_combobox = ttk.Combobox(self.frame, width=40, font=("Arial", 12), state="readonly")  # Combobox solo lectura
        self.uso_combobox.grid(row=8, column=1, pady=5)

        self.equipo_label = tk.Label(self.frame, text="Equipo:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.equipo_label.grid(row=9, column=0, sticky="w", padx=15, pady=5)
        self.equipo_combobox = ttk.Combobox(self.frame, width=40, font=("Arial", 12), state="readonly")  # Combobox solo lectura
        self.equipo_combobox.grid(row=9, column=1, pady=5)

        self.almacen_label = tk.Label(self.frame, text="Almacén:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.almacen_label.grid(row=10, column=0, sticky="w", padx=15, pady=5)
        self.almacen_combobox = ttk.Combobox(self.frame, width=40, font=("Arial", 12), state="readonly")  # Combobox solo lectura
        self.almacen_combobox.grid(row=10, column=1, pady=5)

        # Llamar para listar proveedores y marcas
        self.listar_proveedores()
        self.listar_marcas()
        self.listar_almacenes()
        self.listar_usos()
        self.listar_unidadMedidas()
        self.listar_equipos()
        
        # Botón para registrar el producto
        self.registrar_button = tk.Button(self.frame, text="Registrar Producto", font=("Arial", 14), command=self.registrar_producto, bg="#4CAF50", fg="white", relief="raised", bd=4)
        self.registrar_button.grid(row=11, column=0, columnspan=2, pady=20)

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

    def listar_usos(self):
        """Carga la lista de marcas en el ComboBox"""
        usos = self.controlador.listar_usos()
        uso_nombres = [uso[1] for uso in usos]
        self.uso_combobox['values'] = uso_nombres
        self.uso_combobox.current(0)

    def listar_equipos(self):
        equipos = self.controlador.listar_equipos()
        equipo_nombres = [equipo[1] for equipo in equipos]
        self.equipo_combobox['values'] = equipo_nombres
        self.equipo_combobox.current(0)

    def listar_unidadMedidas(self):
        unidadMedidas = self.controlador.listar_unidadMedidas()
        UnidadMedida_nombres = [UnidadMedida[1] for UnidadMedida in unidadMedidas]
        self.unidadMedida_combobox['values'] = UnidadMedida_nombres
        self.unidadMedida_combobox.current(0)

    def listar_almacenes(self):
        """Carga la lista de almacenes en el ComboBox"""
        almacenes = self.controlador.listar_almacenes()
        almacen_nombres = [almacen[1] for almacen in almacenes]
        self.almacen_combobox['values'] = almacen_nombres
        self.almacen_combobox.current(0)

    def registrar_producto(self):
        nombre = self.partname_entry.get()
        descripcion = self.descripcion_entry.get()
        cantidad = self.cantidad_entry.get()
        precio = self.precio_entry.get()
        proveedor_seleccionado = self.proveedor_combobox.get()
        marca_seleccionada = self.marca_combobox.get()
        und_medida = self.unidadMedida_combobox.get()  # Unidad de medida
        uso = self.uso_combobox.get()  # Uso
        equipo = self.equipo_combobox.get()  # Equipo
        almacen_seleccionado = self.almacen_combobox.get()  # Almacén seleccionado

        # Validación de campos
        if not nombre or not descripcion or not cantidad or not precio or not proveedor_seleccionado or not marca_seleccionada or not und_medida or not uso or not equipo or not almacen_seleccionado:
            messagebox.showwarning("Advertencia", "Todos los campos deben ser completados.")
            return

        # Validación de cantidad y precio numéricos
        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showwarning("Advertencia", "La cantidad debe ser un número entero y el precio debe ser un número válido.")
            return

        # Obtener los IDs correspondientes a proveedor, marca, almacén, unidad de medida, uso y equipo
        proveedores = self.controlador.listar_proveedores()
        proveedor_id = next((proveedor[0] for proveedor in proveedores if proveedor[1] == proveedor_seleccionado), None)
        
        marcas = self.controlador.listar_marcas()
        marca_id = next((marca[0] for marca in marcas if marca[1] == marca_seleccionada), None)

        almacenes = self.controlador.listar_almacenes()
        almacen_id = next((almacen[0] for almacen in almacenes if almacen[1] == almacen_seleccionado), None)

        # Obtener los ID de la unidad de medida
        unidades = self.controlador.listar_unidadMedidas()
        unidad_id = next((unidad[0] for unidad in unidades if unidad[1] == und_medida), None)

        # Obtener el ID del uso
        usos = self.controlador.listar_usos()
        uso_id = next((uso_item[0] for uso_item in usos if uso_item[1] == uso), None)

        # Obtener el ID del equipo
        equipos = self.controlador.listar_equipos()
        equipo_id = next((equipo_item[0] for equipo_item in equipos if equipo_item[1] == equipo), None)

        # Validar que todos los IDs sean encontrados
        if not all([proveedor_id, marca_id, almacen_id, unidad_id, uso_id, equipo_id]):
            messagebox.showerror("Error", "Uno o más de los valores seleccionados no son válidos.")
            return

        # Si los IDs son válidos, llamar al controlador para registrar el producto
        exito = self.controlador.registrar_producto(
            nombre, descripcion, cantidad, precio, proveedor_id, marca_id, almacen_id, unidad_id, uso_id, equipo_id
        )
        if exito:
            messagebox.showinfo("Éxito", "Producto registrado con éxito.")
        else:
            messagebox.showerror("Error", "Hubo un problema al registrar el producto.")
