import tkinter as tk
from controlador.LoginControlador import LoginControlador

def main():
    root = tk.Tk()
    LoginControlador(root)
    root.mainloop()

if __name__ == "__main__":
    main()