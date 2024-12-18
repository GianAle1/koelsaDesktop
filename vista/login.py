import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Usaremos Pillow para redimensionar la imagen

def resource_path(relative_path):
    """Obtenemos la ruta correcta al recurso dentro del ejecutable"""
    try:
        base_path = sys._MEIPASS  # Si el script es empaquetado
    except Exception:
        base_path = os.path.abspath(".")  # Si estamos ejecutando desde el código fuente
    return os.path.join(base_path, relative_path)

class VistaLogin:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador

        self.root.title("Login")
        self.root.geometry("400x500")  # Aumento el tamaño de la ventana
        self.root.config(bg="#f0f0f0")  # Fondo claro

        # Cargar y redimensionar la imagen (logo)
        image_path = resource_path("vista/imagen/login.png")  # Usamos resource_path para obtener la ruta correcta
        self.logo = Image.open(image_path)  # Cargar la imagen usando PIL
        self.logo = self.logo.resize((150, 150))  # Redimensionamos la imagen
        self.logo = ImageTk.PhotoImage(self.logo)  # Convertimos la imagen para usar en Tkinter

        # Agregar el logo en la ventana
        self.logo_label = tk.Label(self.root, image=self.logo, bg="#f0f0f0")
        self.logo_label.pack(pady=20)  # Espaciado en la parte superior

        # Título de la pantalla
        self.title_label = tk.Label(self.root, text="Bienvenido", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#4CAF50")
        self.title_label.pack(pady=10)

        # Frame para los campos de entrada y botones
        self.frame = tk.Frame(self.root, bg="#f0f0f0")
        self.frame.pack(pady=20)

        # Etiquetas y campos de entrada para usuario y contraseña
        self.username_label = tk.Label(self.frame, text="Username:", font=("Arial", 12), bg="#f0f0f0")
        self.username_label.grid(row=0, column=0, pady=5)

        self.username_entry = tk.Entry(self.frame, font=("Arial", 12), bd=2, relief="solid", width=25)
        self.username_entry.grid(row=0, column=1, pady=5)

        self.password_label = tk.Label(self.frame, text="Password:", font=("Arial", 12), bg="#f0f0f0")
        self.password_label.grid(row=1, column=0, pady=5)

        self.password_entry = tk.Entry(self.frame, show="*", font=("Arial", 12), bd=2, relief="solid", width=25)
        self.password_entry.grid(row=1, column=1, pady=5)

        # Botón de login
        self.login_button = tk.Button(self.root, text="Login", command=self.iniciar_sesion, font=("Arial", 12), bg="#4CAF50", fg="white", width=20, height=2, relief="flat")
        self.login_button.pack(pady=20)

    def iniciar_sesion(self):
        """Al hacer click en el botón de login, validamos las credenciales"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.controlador.iniciar_sesion(username, password):  # Llamamos al controlador para validar
            # El controlador manejará la transición al menú
            self.root.withdraw()  # Ocultamos la ventana de login
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
