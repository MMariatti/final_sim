import sys
from PyQt5.QtWidgets import QApplication
from interfaz.recursos import sim
from interfaz.ventana_supermercado import VentanaSupermercado

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = VentanaSupermercado(app)
    window.show()
    app.exec_()
