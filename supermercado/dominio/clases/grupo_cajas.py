import bisect

from dominio.clases.empleado import Caja


class GrupoCajas:

    cajas = []
    cola = None

    def __init__(self, cajas=[], cola=None):
        self.cajas = cajas
        self.cola = cola

    def agregar_caja(self, caja):
        bisect.insort(self.cajas, caja)

    def existe_caja_libre(self):
        for i in range(len(self.cajas) - 1, -1, -1):
            if self.cajas[i].estado == Caja.ESTADO_LIBRE:
                return True
        return False

    def obtener_caja_libre(self):
        for i in range(0, len(self.cajas)):
            if self.cajas[i].estado == Caja.ESTADO_LIBRE:
                return self.cajas[i]
        return None

    def __str__(self):
        cajas = ""
        for i in range(0, len(self.cajas)):
            cajas += self.cajas[i].id
            if i != len(self.cajas) - 1:
                cajas += ", "
        return "GrupoCajas(cajas=[{cajas}], cola={cola})".format(
            cajas=cajas,
            cola=self.cola
        )

    def __repr__(self):
        cajas = ""
        for i in range(0, len(self.cajas)):
            cajas += self.cajas[i].id
            if i != len(self.cajas) - 1:
                cajas += ", "
        return "GrupoCajas(cajas=[{cajas}], cola={cola})".format(
            cajas=cajas,
            cola=self.cola
        )