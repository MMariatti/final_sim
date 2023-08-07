import math
import random
import bisect
import numpy as np

from dominio.clases.caja import Caja
from dominio.clases.cliente import Cliente
from dominio.clases.grupo_cajas import GrupoCajas
from dominio.clases.evento import Evento
from dominio.clases.manejador_eventos import ManejadorEventos
from dominio.clases.cola import Cola

from supermercado.soporte.helper import truncar


class Simulador:

    # Atributos para conexion con el controlador
    controlador = None

    # Atributos para los parametros generales de la simulacion
    tiempo_simulacion = None
    tiempo_desde = None
    cantidad_iteraciones = None

    # Atributos con parametros especificos de la simulacion

    tiempo_llegada_cliente = None
    tiempo_atencion_caja = None
    tiempo_compra_articulos_cliente = None
    cantidad_cajas = None
    cantidad_clientes = None
    cantidad_maxima_clientes = None
    cantidad_de_clientes_que_compran = None
    cantidad_total_clientes = None
    porcentaje_clientes_que_compran = None

    # Atributos para la simulacion
    manejador_eventos = None
    grupo_cajas = None
    cola = None
    rnd_tiempo_proxima_llegada = None
    tiempo_proxima_llegada = None
    rnd_cantidad_articulos = None
    cantidad_articulos = None
    rnd_tiempo_compra = None
    tiempo_compra = None
    rnd_1_atencion_caja = None
    rnd_2_atencion_caja = None

    # Atributos para el manejo de los objetos de la simulacion y el vector de estado
    ultimo_n_iteracion = -1
    ultimo_id_cliente = 0
    ids_clientes_iteraciones = []
    clientes = []

    def __init__(self, controlador, tiempo_simulacion, tiempo_desde, cantidad_iteraciones, tiempo_llegada_cliente,
                 tiempo_atencion_caja,tiempo_compra_articulos_cliente, cantidad_cajas, cantidad_clientes,
                 cantidad_maxima_clientes, cantidad_de_clientes_que_compran,cantidad_total_clientes,
                 porcentaje_clientes_que_compran):
        self.controlador = controlador
        self.tiempo_simulacion = tiempo_simulacion
        self.tiempo_desde = tiempo_desde
        self.cantidad_iteraciones = cantidad_iteraciones
        self.tiempo_llegada_cliente = tiempo_llegada_cliente
        self.tiempo_atencion_caja = tiempo_atencion_caja
        self.tiempo_compra_articulos_cliente = tiempo_compra_articulos_cliente
        self.cantidad_cajas = cantidad_cajas
        self.cantidad_clientes = cantidad_clientes
        self.cantidad_maxima_clientes = cantidad_maxima_clientes
        self.cantidad_de_clientes_que_compran = cantidad_de_clientes_que_compran
        self.cantidad_total_clientes = cantidad_total_clientes
        self.porcentaje_clientes_que_compran = porcentaje_clientes_que_compran

    def generar_vector_estado(self,evento_actual, nuevos_eventos):
        self.ultimo_n_iteracion += 1
        n_iteracion = self.ultimo_n_iteracion
        evento = evento_actual.tipo
        if evento_actual.cliente is not None:
            evento += " " + str(evento_actual.cliente.id) + ")"
        if evento_actual.caja is not None:
            evento += " " + str(evento_actual.caja.id) + ")"

        reloj = evento_actual.tiempo_fin

        vector_estado = {
            "n_iteracion": n_iteracion,
            "evento": evento,
            "reloj": reloj,

            "rnd_tiempo_proxima_llegada": None,
            "tiempo_proxima_llegada": None,
            "proxima_llegada": None,

            "rnd_cantidad_articulos": None,
            "cantidad_articulos": None,
            "rnd_tiempo_compra": None,
            "tiempo_compra": None,
            "fines_compra": {},

            "rnd_1_atencion_caja": None,
            "rnd_2_atencion_caja": None,
            "tiempo_atencion_caja": None,
            "fines_atencion_caja": {},

            "estado_cajas": {},
            "cola": None,

            "cantidad_clientes_que_compran": None,
            "cantidad_total_clientes": None,
            "porcentaje_clientes_que_compran": None,

            "clientes": {}
        }

        for caja in self.grupo_cajas.cajas:
            vector_estado["fines_atencion_caja"][caja.id] = None
            vector_estado["estado_cajas"][caja.id] = caja.estado

        for evento_anterior in self.manejador_eventos.eventos:
            if evento_anterior == Evento.TIPO_INICIALIZACION:
                vector_estado["proxima_llegada"] = evento_anterior.tiempo_fin
            elif evento_anterior.tipo == Evento.TIPO_LLEGADA_CLIENTE:
                vector_estado["proxima_llegada"] = evento_anterior.tiempo_fin
            elif evento_anterior.tipo == Evento.TIPO_FIN_COMPRA:
                vector_estado["fines_compra"][evento_anterior.cliente.id] = evento_anterior.tiempo_fin
            elif evento_anterior.tipo == Evento.TIPO_FIN_ATENCION_CAJA:
                vector_estado["fines_atencion_caja"][evento_anterior.caja.id] = evento_anterior.tiempo_fin

        for nuevo_evento in nuevos_eventos:
            if nuevo_evento.tipo == Evento.TIPO_LLEGADA_CLIENTE:
                vector_estado["rnd_tiempo_proxima_llegada"] = nuevo_evento.rnd_tiempo
                vector_estado["tiempo_proxima_llegada"] = nuevo_evento.tiempo
                vector_estado["proxima_llegada"] = nuevo_evento.tiempo_fin
            elif nuevo_evento.tipo == Evento.TIPO_COMPRA_CLIENTE:
                vector_estado["rnd_cantidad_articulos"] = nuevo_evento.rnd_cantidad_articulos
                vector_estado["cantidad_articulos"] = nuevo_evento.cantidad_articulos
                vector_estado["rnd_tiempo_compra"] = nuevo_evento.rnd_tiempo_compra
                vector_estado["tiempo_compra"] = nuevo_evento.tiempo_compra
                vector_estado["fines_compra"][nuevo_evento.cliente.id] = nuevo_evento.tiempo_fin
            elif nuevo_evento.tipo == Evento.TIPO_ATENCION_CLIENTE:
                vector_estado["rnd_1_atencion_caja"] = nuevo_evento.rnd_1
                vector_estado["rnd_2_atencion_caja"] = nuevo_evento.rnd_2
                vector_estado["tiempo_atencion_caja"] = nuevo_evento.tiempo
                vector_estado["fines_atencion_caja"][nuevo_evento.caja.id] = nuevo_evento.tiempo_fin

            # Cola de las cajas, es una sola cola para las 3 cajas
            vector_estado["cola"] = self.grupo_cajas.cola

            vector_estado["cantidad_clientes_que_compran"] = self.cantidad_de_clientes_que_compran
            vector_estado["cantidad_total_clientes"] = self.cantidad_total_clientes
            vector_estado["porcentaje_clientes_que_compran"] = self.porcentaje_clientes_que_compran

            # Clientes que estan en el supermercado
            for cliente in self.clientes:
                vector_estado["clientes"][cliente.id] = cliente.cliente_dict()

        return vector_estado

    def obtener_cantidad_articulos(self, rnd_art):
        if 0 < rnd_art < 0.1:
            return 0
        elif 0.1 < rnd_art < 0.25:
            return 1
        elif 0.25 < rnd_art < 0.5:
            return 2
        elif 0.5 < rnd_art < 0.7:
            return 3
        elif 0.7 < rnd_art < 0.85:
            return 4
        else:
            return 5
    def simular_iteracion(self):

        self.rnd_tiempo_proxima_llegada = None
        self.tiempo_proxima_llegada = None

        self.rnd_cantidad_articulos = None
        self.cantidad_articulos = None
        self.rnd_tiempo_compra = None
        self.tiempo_compra = None

        self.rnd_1_atencion_caja = None
        self.rnd_2_atencion_caja = None
        self.tiempo_atencion_caja = None

        self.cantidad_de_clientes_que_compran = 0
        self.cantidad_total_clientes = 0
        self.porcentaje_clientes_que_compran = 0

        # Obtengo evento actual
        evento_actual = self.manejador_eventos.obtener_proximo_evento()

        # Inicializo lista de eventos generados durante la iteracion

        eventos_iteracion = []

        # Evento actual inicializacion

        if evento_actual.tipo == Evento.TIPO_INICIALIZACION:

            # Genero evento de llegada de cliente
            tipo_evento = Evento.TIPO_LLEGADA_CLIENTE
            rnd = truncar(random.random(), 2)
            tiempo = round(-12 * math.log(1 - rnd), 2)
            tiempo_fin = round(evento_actual.tiempo_fin + tiempo, 2)
            nuevo_evento = Evento(tipo_evento, rnd, tiempo, tiempo_fin)

            # Agrego evento a la lista de eventos de la iteracion
            self.manejador_eventos.agregar_evento(nuevo_evento)

            # Agrego evento a la lista de eventos de la iteracion
            eventos_iteracion.append(nuevo_evento)

        # Evento actual llegada de cliente

        elif evento_actual.tipo == Evento.TIPO_LLEGADA_CLIENTE:

            # Genero proxima llegada de cliente
            tipo_evento = Evento.TIPO_LLEGADA_CLIENTE
            rnd = truncar(random.random(), 2)
            tiempo = round(-12 * math.log(1 - rnd), 2)
            tiempo_fin = round(evento_actual.tiempo_fin + tiempo, 2)
            nuevo_evento = Evento(tipo_evento, rnd, tiempo, tiempo_fin)

            # Agrego evento a la lista de eventos de la iteracion
            self.manejador_eventos.agregar_evento(nuevo_evento)

            # Agrego evento a la lista de eventos de la iteracion
            eventos_iteracion.append(nuevo_evento)

            #compruebo que haya 10 o menos clientes que estan en estado COMPRANDO en este momento



            # Genero evento de compra de cliente
            tipo_evento = Evento.TIPO_COMPRA_CLIENTE
            rnd_art = truncar(random.random(), 2)
            cantidad_articulos = self.obtener_cantidad_articulos(rnd_art)
            rnd_tiempo_compra = truncar(random.random(), 2)
            # Genero tiempo de compra con distribucion uniforme con a = 8 y b = 10
            tiempo_compra = round((8 + (10 - 8) * rnd_tiempo_compra)*cantidad_articulos, 2)
            tiempo_fin = round(evento_actual.tiempo_fin + tiempo_compra, 2)
            nuevo_evento = Evento(tipo_evento, rnd_art, cantidad_articulos, rnd_tiempo_compra, tiempo_compra,
                                  tiempo_fin, evento_actual.cliente)

            # Agrego evento a la lista de eventos de la iteracion
            self.manejador_eventos.agregar_evento(nuevo_evento)

            # Agrego evento a la lista de eventos de la iteracion
            eventos_iteracion.append(nuevo_evento)
            # Actualizo estado del cliente
            evento_actual.cliente.estado = Cliente.ESTADO_COMPRANDO

            # Genero evento de atencion de cliente
            tipo_evento = Evento.TIPO_ATENCION_CLIENTE
            rnd_1 = truncar(random.random(), 2)
            rnd_2 = truncar(random.random(), 2)

            # genero tiempo de atencion con distribucion normal media 15 y desviacion estandar 3
            tiempo = round(math.sqrt(-2*math.log(rnd_1))*math.cos(2 * math.pi * rnd_2)*3 + 15, 2)
            tiempo_fin = round(evento_actual.tiempo_fin + tiempo, 2)

            # Busco si hay cajas libres para atender al cliente
            caja = self.grupo_cajas.buscar_caja_libre()
            if caja is not None:
                nuevo_evento = Evento(tipo_evento, rnd_1, rnd_2, tiempo, tiempo_fin, evento_actual.cliente, caja)
                # Agrego evento a la lista de eventos de la iteracion
                self.manejador_eventos.agregar_evento(nuevo_evento)

                # Agrego evento a la lista de eventos de la iteracion
                eventos_iteracion.append(nuevo_evento)
                # Actualizo estado del cliente
                evento_actual.cliente.estado = Cliente.ESTADO_ATENDIDO
                # Actualizo estado de la caja
                caja.estado = Caja.ESTADO_OCUPADO
                caja.cliente = evento_actual.cliente
            else:
                # Actualizo estado del cliente
                evento_actual.cliente.estado = Cliente.ESTADO_ESPERANDO
                # Agrego cliente a la cola de espera
                self.cola.agregar_cliente(evento_actual.cliente)












