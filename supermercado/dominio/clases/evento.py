class Evento:
    tipo = None
    rnd_llegada_cliente = None
    rnd_cant_articulos = None
    rnd_tiempo_compra = None
    rnd1_atencion_caja = None
    rnd2_atencion_caja = None
    tiempo = None
    tiempo_fin = None
    caja = None
    cliente = None
    articulos = None

    TIPO_INICIALIZACION = "inicializacion"
    TIPO_LLEGADA_CLIENTE = "llegada_cliente"
    TIPO_FIN_ATENCION_CLIENTE = "fin_atencion_cliente"
    TIPO_FIN_COMPRA_CLIENTE = "fin_compra_cliente"
    TIPO_FIN_SIMULACION = "fin_simulacion"

    def __init__(self, tipo_evento=None, rnd_llegada_cliente=None, rnd_cant_articulos=None,
                 rnd_tiempo_compra=None, rnd1_atencion_caja=None, rnd2_atencion_caja=None, tiempo=None,
                 tiempo_fin=None, cliente=None, caja=None, articulos=None):
        self.tipo = tipo_evento
        self.rnd_llegada_cliente = rnd_llegada_cliente
        self.rnd_cant_articulos = rnd_cant_articulos
        self.rnd_tiempo_compra = rnd_tiempo_compra
        self.rnd1_atencion_caja = rnd1_atencion_caja
        self.rnd2_atencion_caja = rnd2_atencion_caja
        self.tiempo = tiempo
        self.tiempo_fin = tiempo_fin
        self.cliente = cliente
        self.caja = caja
        self.articulos = articulos

    def __eq__(self, other):
        return True if self.tiempo_fin == other.tiempo_fin else False

    def __ne__(self, other):
        return True if self.tiempo_fin != other.tiempo_fin else False

    def __gt__(self, other):
        return True if self.tiempo_fin > other.tiempo_fin else False

    def __lt__(self, other):
        return True if self.tiempo_fin < other.tiempo_fin else False

    def __ge__(self, other):
        return True if self.tiempo_fin >= other.tiempo_fin else False

    def __le__(self, other):
        return True if self.tiempo_fin <= other.tiempo_fin else False

    def __str__(self):
        return (
            "Evento(tipo={tipo}, rnd_llegada_cliente={rnd_llegada_cliente}, rnd_cant_articulos={rnd_cant_articulos},"
            " rnd_tiempo_compra={rnd_tiempo_compra}, rnd1_atencion_caja={rnd1_atencion_caja}, "
            "rnd2_atencion_caja={rnd2_atencion_caja}, tiempo={tiempo}, tiempo_fin={tiempo_fin},"
            " cliente={cliente}, caja={caja}, articulos={articulos})".format(
                tipo=self.tipo,
                rnd_llegada_cliente=str(self.rnd_llegada_cliente),
                rnd_cant_articulos=str(self.rnd_cant_articulos),
                rnd_tiempo_compra=str(self.rnd_tiempo_compra),
                rnd1_atencion_caja=str(self.rnd1_atencion_caja),
                rnd2_atencion_caja=str(self.rnd2_atencion_caja),
                tiempo=str(self.tiempo),
                tiempo_fin=str(self.tiempo_fin),
                cliente=self.cliente.id if self.cliente is not None else "None",
                caja=self.caja.id if self.caja is not None else "None",
                articulos=self.articulos)
        )

    def __repr__(self):
        return (
            "Evento(tipo={tipo}, rnd_llegada_cliente={rnd_llegada_cliente}, rnd_cant_articulos={rnd_cant_articulos},"
            " rnd_tiempo_compra={rnd_tiempo_compra}, rnd1_atencion_caja={rnd1_atencion_caja}, "
            "rnd2_atencion_caja={rnd2_atencion_caja}, tiempo={tiempo}, tiempo_fin={tiempo_fin},"
            " cliente={cliente}, caja={caja}, articulos={articulos})".format(
                tipo=self.tipo,
                rnd_llegada_cliente=str(self.rnd_llegada_cliente),
                rnd_cant_articulos=str(self.rnd_cant_articulos),
                rnd_tiempo_compra=str(self.rnd_tiempo_compra),
                rnd1_atencion_caja=str(self.rnd1_atencion_caja),
                rnd2_atencion_caja=str(self.rnd2_atencion_caja),
                tiempo=str(self.tiempo),
                tiempo_fin=str(self.tiempo_fin),
                cliente=self.cliente.id if self.cliente is not None else "None",
                caja=self.caja.id if self.caja is not None else "None",
                articulos=str(self.articulos))
        )
