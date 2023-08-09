class Cola:
    id_cola = None
    clientes = []

    def __init__(self, id_cola,clientes=[]):
        id_cola = id_cola
        self.clientes = clientes

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def agregar_cliente_al_principio(self, cliente):
        self.clientes.insert(0, cliente)

    def existe_proximo_cliente(self):
        return len(self.clientes) != 0

    def obtener_proximo_cliente(self):
        return self.clientes.pop(0)

    def obtener_longitud(self):
        return len(self.clientes)

    def __str__(self):
        clientes = ""
        for i in range(0, len(self.clientes)):
            clientes += str(self.clientes[i].id)
            if i != len(self.clientes) - 1:
                clientes += ", "
        return "Cola(clientes=[{clientes}])".format(
            clientes=clientes
        )

    def __repr__(self):
        clientes = ""
        for i in range(0, len(self.clientes)):
            clientes += str(self.clientes[i].id)
            if i != len(self.clientes) - 1:
                clientes += ", "
        return "Cola(clientes=[{clientes}])".format(
            clientes=clientes
        )

