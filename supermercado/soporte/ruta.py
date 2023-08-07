import sys
import os


class Ruta:

    @staticmethod
    def generar_ruta(relative_path):
        try:
            ruta_base = sys._MEIPASS
        except Exception:
            ruta_base = os.path.abspath(".")

        return os.path.join(ruta_base, relative_path)
