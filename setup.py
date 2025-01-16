from cx_Freeze import setup, Executable

setup(
    name="MiPrograma",
    version="1.0",
    description="Descripción del programa",
    executables=[Executable("main.py")]
)
