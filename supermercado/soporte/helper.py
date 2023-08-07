import json
import math
from decimal import Decimal


# Constantes para manejo de decimales
TWOPLACES = Decimal(10) ** -2
FOURPLACES = Decimal(10) ** -4
SIXPLACES = Decimal(10) ** -6


# Funciones
def truncar(numero, cantidad_decimales):
    cantidad_decimales = 10 ** cantidad_decimales
    return math.floor(numero * cantidad_decimales) / cantidad_decimales


def mostrar_diccionario_formateado(dict):
    return print(json.dumps(dict, default=lambda obj: obj.__str__(), indent=4))
