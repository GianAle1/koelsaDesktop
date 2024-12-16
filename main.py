# main.py
import tkinter as tk
from controlador.LoginControlador import LoginControlador

def main():
    root = tk.Tk()
    controlador = LoginControlador(root)  # Aquí instanciamos el controlador
    root.mainloop()

if __name__ == "__main__":
    main()
