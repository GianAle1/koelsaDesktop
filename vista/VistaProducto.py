import tkinter as tk
from tkinter import  messagebox, ttk
from ttkwidgets.autocomplete import AutocompleteCombobox


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

        # Campo Marca con AutocompleteCombobox
        self.marca_label = tk.Label(self.frame, text="Marca:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.marca_label.grid(row=2, column=0, sticky="w", padx=15, pady=5)
        self.marca_combobox = AutocompleteCombobox(self.frame, width=40, font=("Arial", 12))  # Usamos AutocompleteCombobox
        self.marca_combobox.grid(row=2, column=1, pady=5)
        # Combobox solo lectura
        self.marca_combobox.grid(row=2, column=1, pady=5)

        self.familia_label = tk.Label(self.frame, text="Familia:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.familia_label.grid(row=3, column=0, sticky="w", padx=15, pady=5)
        self.familia_combobox = ttk.Combobox(self.frame, width=40, font=("Arial", 12), state="readonly")  # Combobox solo lectura
        self.familia_combobox.grid(row=3, column=1, pady=5)

        self.descripcion_label = tk.Label(self.frame, text="Descripción:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.descripcion_label.grid(row=4, column=0, sticky="w", padx=15, pady=5)
        self.descripcion_entry = tk.Entry(self.frame, width=40, font=("Arial", 12), relief="solid", bd=2)
        self.descripcion_entry.grid(row=4, column=1, pady=5)

        self.undMedida_label = tk.Label(self.frame, text="Unidad de Medida:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.undMedida_label.grid(row=5, column=0, sticky="w", padx=15, pady=5)
        self.unidadMedida_combobox = ttk.Combobox(self.frame, width=40, font=("Arial", 12), state="readonly")  # Combobox solo lectura
        self.unidadMedida_combobox.grid(row=5, column=1, pady=5)

        self.cantidad_label = tk.Label(self.frame, text="Cantidad:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.cantidad_label.grid(row=6, column=0, sticky="w", padx=15, pady=5)
        self.cantidad_entry = tk.Entry(self.frame, width=40, font=("Arial", 12), relief="solid", bd=2)
        self.cantidad_entry.grid(row=6, column=1, pady=5)

        self.precio_label = tk.Label(self.frame, text="Precio:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.precio_label.grid(row=7, column=0, sticky="w", padx=15, pady=5)
        self.precio_entry = tk.Entry(self.frame, width=40, font=("Arial", 12), relief="solid", bd=2)
        self.precio_entry.grid(row=7, column=1, pady=5)

        

        # Almacén
        self.almacen_label = tk.Label(self.frame, text="Almacén:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.almacen_label.grid(row=9, column=0, sticky="w", padx=15, pady=5)
        self.almacen_combobox = ttk.Combobox(self.frame, width=40, font=("Arial", 12), state="readonly")  # Combobox solo lectura
        self.almacen_combobox.grid(row=9, column=1, pady=5)
        self.almacen_combobox.bind("<<ComboboxSelected>>", self.cargar_subalmacenes)  # Vincular evento

        # Sub Almacén
        self.subalmacen_label = tk.Label(self.frame, text="Sub Almacén:", font=("Arial", 12), bg="#f4f4f9", anchor="w")
        self.subalmacen_label.grid(row=10, column=0, sticky="w", padx=15, pady=5)
        self.subalmacen_combobox = ttk.Combobox(self.frame, width=40, font=("Arial", 12), state="readonly")  # Combobox solo lectura
        self.subalmacen_combobox.grid(row=10, column=1, pady=5)
        
      
        self.listar_marcas()
        self.listar_almacenes()
        self.listar_unidadMedidas()
        self.listar_familias()

        self.registrar_button = tk.Button(self.frame, text="Registrar Producto", font=("Arial", 14), command=self.registrar_producto, bg="#4CAF50", fg="white", relief="raised", bd=4)
        self.registrar_button.grid(row=12, column=0, columnspan=2, pady=20)

    def mostrar_producto(self):
        self.root.mainloop()

    

    def listar_marcas(self):
        """Obtiene las marcas desde el controlador y las configura en el AutocompleteCombobox."""
        marcas = self.controlador.listar_marcas()  # Obtener marcas del controlador
        marca_nombres = [marca[1] for marca in marcas]  # Extraer nombres de las marcas
        self.marca_combobox.set_completion_list(marca_nombres)  # Actualizar valores
        self.marca_combobox.set("")  # Limpiar selección inicial

    def listar_unidadMedidas(self):
        unidadMedidas = self.controlador.listar_unidadMedidas()
        UnidadMedida_nombres = [UnidadMedida[1] for UnidadMedida in unidadMedidas]
        self.unidadMedida_combobox['values'] = UnidadMedida_nombres
        self.unidadMedida_combobox.current(0)

    def listar_almacenes(self):
        almacenes = self.controlador.listar_almacenes()
        almacen_nombres = [almacen[1] for almacen in almacenes]
        self.almacen_combobox['values'] = almacen_nombres
        self.almacen_combobox.current(0)

    def listar_familias(self):
        familias = self.controlador.listar_familias()
        familia_nombres = [familia[1] for familia in familias]
        self.familia_combobox['values'] = familia_nombres
        self.familia_combobox.current(0)

    def registrar_producto(self):
        nombre = self.partname_entry.get()
        descripcion = self.descripcion_entry.get()
        cantidad = self.cantidad_entry.get()
        precio = self.precio_entry.get()
        
        marca_seleccionada = self.marca_combobox.get()
        und_medida = self.unidadMedida_combobox.get()  # Unidad de medida
        familia_seleccionado = self.familia_combobox.get()
        subalmacen_seleccionado = self.subalmacen_combobox.get()  # Subalmacén seleccionado

        # Validación de campos
        if not nombre or not descripcion or not cantidad or not precio  or not marca_seleccionada or not und_medida or not subalmacen_seleccionado or not familia_seleccionado:
            messagebox.showwarning("Advertencia", "Todos los campos deben ser completados.")
            return

        # Validación de cantidad y precio numéricos
        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showwarning("Advertencia", "La cantidad debe ser un número entero y el precio debe ser un número válido.")
            return

        # Obtener IDs de las opciones seleccionadas
        

        marcas = self.controlador.listar_marcas()
        marca_id = next((marca[0] for marca in marcas if marca[1] == marca_seleccionada), None)

        unidades = self.controlador.listar_unidadMedidas()
        unidad_id = next((unidad[0] for unidad in unidades if unidad[1] == und_medida), None)

        familias = self.controlador.listar_familias()
        familia_id = next((familia_item[0] for familia_item in familias if familia_item[1] == familia_seleccionado), None)

        # Obtener subalmacen_id para el subalmacen seleccionado
        almacen_seleccionado = self.almacen_combobox.get()
        almacenes = self.controlador.listar_almacenes()
        almacen_id = next((almacen[0] for almacen in almacenes if almacen[1] == almacen_seleccionado), None)

        subalmacenes = self.controlador.listar_subalmacenes(almacen_id)
        subalmacen_id = next((subalmacen[0] for subalmacen in subalmacenes if subalmacen[1] == subalmacen_seleccionado), None)

        # Validar que todos los IDs sean encontrados
        if not all([ marca_id, unidad_id, familia_id, subalmacen_id]):
            messagebox.showerror("Error", "Uno o más de los valores seleccionados no son válidos.")
            return

        # Llamar al controlador para registrar el producto
        exito = self.controlador.registrar_producto(
        nombre, descripcion, cantidad, precio, marca_id, subalmacen_id, unidad_id, familia_id
        )

        if exito:
            messagebox.showinfo("Éxito", "Producto registrado con éxito.")
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "Hubo un problema al registrar el producto.")


        # Función para cargar subalmacenes
    def cargar_subalmacenes(self, event=None):
        """Carga los subalmacenes asociados al almacén seleccionado."""
        almacen_seleccionado = self.almacen_combobox.get()
        if not almacen_seleccionado:
            self.subalmacen_combobox["values"] = []
            return

        # Obtener el ID del almacén seleccionado
        almacenes = self.controlador.listar_almacenes()
        almacen_id = next((almacen[0] for almacen in almacenes if almacen[1] == almacen_seleccionado), None)

        if almacen_id:
            # Obtener subalmacenes para el almacén seleccionado
            subalmacenes = self.controlador.listar_subalmacenes(almacen_id)
            if subalmacenes:
                self.subalmacen_combobox["values"] = [subalmacen[1] for subalmacen in subalmacenes]
                self.subalmacen_combobox.current(0)
            else:
                self.subalmacen_combobox["values"] = ["No hay subalmacenes"]
                self.subalmacen_combobox.current(0)
        else:
            self.subalmacen_combobox["values"] = ["Seleccione un almacén válido"]
            self.subalmacen_combobox.current(0)

    def limpiar_campos(self):
        """Limpia todos los campos de entrada después de registrar un producto."""
        self.partname_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.proveedor_combobox.set("")  # Restablecer el ComboBox
        self.marca_combobox.set("")
        self.unidadMedida_combobox.set("")
        self.familia_combobox.set("")
        self.almacen_combobox.set("")
        self.subalmacen_combobox.set("")