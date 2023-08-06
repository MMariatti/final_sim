import bisect


class ManejadorEventos:

    eventos = []

    def __init__(self, eventos=[]):
        self.eventos = eventos

    def agregar_evento(self, evento):
        bisect.insort(self.eventos, evento)

    def obtener_proximo_evento(self):
        return self.eventos.pop(0)

    def __str__(self):
        eventos = ""
        for i in range(0, len(self.eventos)):
            eventos += str(self.eventos[i].tiempo_fin)
            if i != len(self.eventos) - 1:
                eventos += ", "
        return "ManejadorEventos(eventos=[{eventos}])".format(
            eventos=eventos
        )

    def __repr__(self):
        eventos = ""
        for i in range(0, len(self.eventos)):
            eventos += str(self.eventos[i].tiempo_fin)
            if i != len(self.eventos) - 1:
                eventos += ", "
        return "ManejadorEventos(eventos=[{eventos}])".format(
            eventos=eventos
        )
