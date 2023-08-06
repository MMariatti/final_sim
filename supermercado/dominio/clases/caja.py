
class Caja:

    id = None
    estado = None
    cliente = None

    ESTADO_LIBRE = "Libre"
    ESTADO_OCUPADO = "Ocupado"

    def __init__(self, id_caja=None, estado=None, cliente=None):
        self.id = id_caja
        self.estado = estado
        self.cliente = cliente

    def cambiar_a_estado_libre(self):
        self.estado = Caja.ESTADO_LIBRE

    def cambiar_a_estado_ocupado(self):
        self.estado = Caja.ESTADO_OCUPADO

    def asignar_cliente(self, cliente):
        self.cliente = cliente

    def desasignar_cliente(self):
        cliente = self.cliente
        self.cliente = None
        return cliente

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

    def __str__(self):
        return "Caja(id={id}, estado={estado}, cliente={cliente})".format(
            id=str(self.id),
            estado=self.estado,
            cliente=self.cliente.id if self.cliente is not None else "None"
        )

    def __repr__(self):
        return "Caja(id={id}, estado={estado}, cliente={cliente})".format(
            id=str(self.id),
            estado=self.estado,
            cliente=self.cliente.id if self.cliente is not None else "None"
        )