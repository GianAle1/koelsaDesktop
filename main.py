import os
import sys
import tkinter as tk
import traceback
from controlador.LoginControlador import LoginControlador

def obtener_ruta(ruta_relativa):
    """Devuelve la ruta absoluta al recurso."""
    # Cuando el programa está empaquetado con PyInstaller
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        # Modo desarrollo
        base_path = os.path.abspath(".")
    return os.path.join(base_path, ruta_relativa)


def iniciar_aplicacion():
    try:
        root = tk.Tk()
        LoginControlador(root)
        root.mainloop()

    except Exception as e:
        
        print("Error detectado:")
        print(traceback.format_exc())
        input("Presiona Enter para cerrar...")

if __name__ == "__main__":
    iniciar_aplicacion()