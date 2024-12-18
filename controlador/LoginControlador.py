from vista.login import VistaLogin
from modelo.usuario import Usuario
from vista.VistaMenu import VistaMenu
from controlador.MenuControlador import MenuControlador
import tkinter as tk
class LoginControlador:
    def __init__(self, root):
   
        self.vista_login = VistaLogin(root, self)
        self.usuario = Usuario()  
        self.menu_ventana = None  

    def iniciar_sesion(self, username, password):
        """Método que se llama cuando el usuario intenta iniciar sesión."""
        if self.usuario.verificar_credenciales(username, password):  # Si las credenciales son correctas
            self.mostrar_menu()  # Llamamos al controlador del menú
            return True
        else:
            return False

    def mostrar_menu(self):
        """Método para mostrar el menú después de un login exitoso."""
        if not self.menu_ventana:  # Solo creamos la ventana de menú si no existe una
            ventana_menu = tk.Tk()  # Crear una nueva ventana para el menú
            menu_controlador = MenuControlador()  # Controlador para gestionar el menú
            vista_menu = VistaMenu(ventana_menu, menu_controlador)  # Vista del menú
            vista_menu.mostrar_menu()  # Mostrar el menú
            self.menu_ventana = ventana_menu  # Guardamos la ventana para evitar crearla nuevamente
