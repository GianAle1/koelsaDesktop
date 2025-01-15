import tkinter as tk
from tkinter import messagebox

class VistaLogin:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador

        # Configuración de la ventana principal
        self.root.title("Login")
        self.root.geometry("400x400")  # Tamaño ajustado de la ventana
        self.root.config(bg="#f0f0f0")  # Fondo claro

        # Título de la pantalla
        self.title_label = tk.Label(self.root, text="Bienvenido", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#4CAF50")
        self.title_label.pack(pady=30)  # Espaciado en la parte superior

        # Frame para los campos de entrada y botones
        self.frame = tk.Frame(self.root, bg="#f0f0f0")
        self.frame.pack(pady=20)

        # Etiquetas y campos de entrada para usuario y contraseña
        self.username_label = tk.Label(self.frame, text="Username:", font=("Arial", 12), bg="#f0f0f0")
        self.username_label.grid(row=0, column=0, pady=10, padx=10, sticky="e")

        self.username_entry = tk.Entry(self.frame, font=("Arial", 12), bd=2, relief="solid", width=25)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)

        self.password_label = tk.Label(self.frame, text="Password:", font=("Arial", 12), bg="#f0f0f0")
        self.password_label.grid(row=1, column=0, pady=10, padx=10, sticky="e")

        self.password_entry = tk.Entry(self.frame, show="*", font=("Arial", 12), bd=2, relief="solid", width=25)
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)

        # Botón de login
        self.login_button = tk.Button(self.root, text="Login", command=self.iniciar_sesion, font=("Arial", 12), bg="#4CAF50", fg="white", width=20, height=2, relief="flat")
        self.login_button.pack(pady=30)

    def iniciar_sesion(self):
        """Al hacer clic en el botón de login, validamos las credenciales"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.controlador.iniciar_sesion(username, password):  # Llamamos al controlador para validar
            # El controlador manejará la transición al menú
            self.root.withdraw()  # Ocultamos la ventana de login
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
