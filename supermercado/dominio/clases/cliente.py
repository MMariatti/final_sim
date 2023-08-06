
class Cliente:

    id = None
    estado = None
    caja = None

    ESTADO_COMPRANDO = "Comprando"
    ESTADO_ESPERANDO_ATENCION = "Esperando atencion"
    ESTADO_SIENDO_ATENDIDO = "Siendo atendido"

    def __init__(self, id_cliente=None, estado=None,    caja=None):
        self.id = id_cliente
        self.estado = estado
        self.caja = caja

    def cambiar_a_estado_comprando(self):
        self.estado = Cliente.ESTADO_COMPRANDO

    def cambiar_a_estado_esperando_atencion(self):
        self.estado = Cliente.ESTADO_ESPERANDO_ATENCION

    def cambiar_a_estado_siendo_atendido(self):
        self.estado = Cliente.ESTADO_SIENDO_ATENDIDO

    def __eq__(self, other):
        return True if self.id == other.id else False

    def __ne__(self, other):
        return True if self.id != other.id else False

    def __gt__(self, other):
        return True if self.id > other.id else False

    def __lt__(self, other):
        return True if self.id < other.id else False

    def __ge__(self, other):
        return True if self.id >= other.id else False

    def __le__(self, other):
        return True if self.id <= other.id else False

    def cliente_dict(self):
        return {
            'id': self.id,
            'estado': self.estado,
            'caja': self.caja if self.caja is not None else None
        }

    def __str__(self):
        return str(self.cliente_dict())
