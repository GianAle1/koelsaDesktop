import tkinter as tk
from controlador.LoginControlador import LoginControlador

def iniciar_aplicacion():
    root = tk.Tk()
    LoginControlador(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_aplicacion()