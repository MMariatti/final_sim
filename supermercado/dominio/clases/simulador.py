import math
import random
import bisect
import numpy as np

from supermercado.dominio.clases.caja import Caja
from supermercado.dominio.clases.cliente import Cliente
from supermercado.dominio.clases.grupo_cajas import GrupoCajas
from supermercado.dominio.clases.evento import Evento
from supermercado.dominio.clases.manejador_eventos import ManejadorEventos
from supermercado.dominio.clases.cola import Cola

from supermercado.soporte.helper import truncar


def obtener_cantidad_articulos(rnd_art):
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
    cantidad_cajas = 3
    cantidad_clientes = None
    cantidad_de_clientes_comprando_simultaneamente = None  # No puede ser mayor a 10
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
                 tiempo_atencion_caja, tiempo_compra_articulos_cliente, cantidad_cajas, cantidad_clientes,
                 cantidad_maxima_clientes, cantidad_de_clientes_que_compran, cantidad_total_clientes,
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

    def generar_vector_estado(self, evento_actual, nuevos_eventos):
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

            if evento_anterior.tipo == Evento.TIPO_LLEGADA_CLIENTE:
                vector_estado["proxima_llegada"] = evento_anterior.tiempo_fin
            elif evento_anterior.tipo == Evento.TIPO_FIN_COMPRA_CLIENTE:
                vector_estado["fines_compra"][evento_anterior.cliente.id] = evento_anterior.tiempo_fin
            elif evento_anterior.tipo == Evento.TIPO_FIN_ATENCION_CLIENTE:
                vector_estado["fines_atencion_caja"][evento_anterior.caja.id] = evento_anterior.tiempo_fin

        for nuevo_evento in nuevos_eventos:
            if nuevo_evento.tipo == Evento.TIPO_LLEGADA_CLIENTE:
                vector_estado["rnd_tiempo_proxima_llegada"] = nuevo_evento.rnd_llegada_cliente
                vector_estado["tiempo_proxima_llegada"] = nuevo_evento.tiempo
                vector_estado["proxima_llegada"] = nuevo_evento.tiempo_fin
                vector_estado["rnd_cantidad_articulos"] = nuevo_evento.rnd_cant_articulos
                vector_estado["cantidad_articulos"] = nuevo_evento.articulos
                vector_estado["rnd_tiempo_compra"] = nuevo_evento.rnd_tiempo_compra
                vector_estado["tiempo_compra"] = nuevo_evento.rnd_tiempo_compra
                print("nuevo evento", nuevo_evento)
                vector_estado["fines_compra"][nuevo_evento.cliente.id] = nuevo_evento.tiempo_fin
            elif nuevo_evento.tipo == Evento.TIPO_FIN_COMPRA_CLIENTE:
                vector_estado["rnd_1_atencion_caja"] = nuevo_evento.rnd1_atencion_caja
                vector_estado["rnd_2_atencion_caja"] = nuevo_evento.rnd2_atencion_caja
                vector_estado["tiempo_atencion_caja"] = nuevo_evento.tiempo
                if nuevo_evento.caja is not None:
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
        print(eventos_iteracion)

        # Evento actual inicializacion

        if evento_actual.tipo == Evento.TIPO_INICIALIZACION:
            # Genero evento de llegada de cliente
            tipo_evento = Evento.TIPO_LLEGADA_CLIENTE
            rnd = truncar(random.random(), 2)
            tiempo = round(-12 * math.log(1 - rnd), 2)
            tiempo_fin = round(evento_actual.tiempo_fin + tiempo, 2)

            # Genero Cliente asociado a la llegada
            self.ultimo_id_cliente += 1
            id_cliente = self.ultimo_id_cliente
            estado_cliente = Cliente.ESTADO_COMPRANDO
            cliente = Cliente(id_cliente, estado_cliente)

            nuevo_evento = Evento(tipo_evento, rnd_llegada_cliente=rnd, tiempo=tiempo, tiempo_fin=tiempo_fin,
                                  cliente=cliente)
            print("Evento llegada cliente: " + str(nuevo_evento))
            # Agrego evento a la lista de eventos de la iteracion
            self.manejador_eventos.agregar_evento(nuevo_evento)

            # Agrego evento a la lista de eventos de la iteracion
            eventos_iteracion.append(nuevo_evento)

        # Evento actual llegada de cliente

        elif evento_actual.tipo == Evento.TIPO_LLEGADA_CLIENTE:

            # Chequeo que no haya mas de 10 clientes comprando en simultaneo
            if self.cantidad_de_clientes_comprando_simultaneamente <= 10:
                self.cantidad_de_clientes_comprando_simultaneamente += 1

                # Genero evento fin compra cliente
                tipo_evento = Evento.TIPO_FIN_COMPRA_CLIENTE
                # Genero cantidad de articulos y tiempo de compra
                rnd_art = truncar(random.random(), 2)
                cantidad_articulos = obtener_cantidad_articulos(rnd_art)
                rnd_tiempo_compra = truncar(random.random(), 2)
                # Genero tiempo de compra con distribucion uniforme A = 8 y B = 10 y la multiplico por la cantidad de
                # articulos
                tiempo_compra = round((rnd_tiempo_compra * 2) + 8, 2) * cantidad_articulos
                tiempo_fin = round(evento_actual.tiempo_fin + tiempo_compra, 2)

                # Agrego evento a la lista de eventos de la iteracion
                nuevo_evento = Evento(tipo_evento, rnd_cant_articulos=rnd_art, rnd_tiempo_compra=rnd_tiempo_compra,
                                      tiempo=tiempo_compra, tiempo_fin=tiempo_fin, cliente=evento_actual.cliente,
                                      articulos=cantidad_articulos)

                self.manejador_eventos.agregar_evento(nuevo_evento)

                # Agrego evento a la lista de eventos de la iteracion
                eventos_iteracion.append(nuevo_evento)

                # Genero la llegada del siguiente cliente con distribucion exponencial
                tipo_evento = Evento.TIPO_LLEGADA_CLIENTE
                # Genero nuevo cliente
                self.ultimo_id_cliente += 1
                id_cliente = self.ultimo_id_cliente
                estado_cliente = Cliente.ESTADO_COMPRANDO
                cliente = Cliente(id_cliente, estado_cliente)
                # Agrego cliente a la lista de clientes
                self.clientes.append(cliente)

                rnd = truncar(random.random(), 2)
                tiempo = round(-12 * math.log(1 - rnd), 2)
                tiempo_fin = round(evento_actual.tiempo_fin + tiempo, 2)
                nuevo_evento = Evento(tipo_evento, rnd_llegada_cliente=rnd, tiempo=tiempo, tiempo_fin=tiempo_fin,
                                      cliente=cliente)

                self.manejador_eventos.agregar_evento(nuevo_evento)

                # Agrego evento a la lista de eventos de la iteracion
                eventos_iteracion.append(nuevo_evento)

            else:
                # El cliente se va sin comprar
                self.cantidad_total_clientes += 1

        if evento_actual.tipo == Evento.TIPO_FIN_COMPRA_CLIENTE:

            # Decremento el contador porque el cliente termino de comprar
            self.cantidad_de_clientes_comprando_simultaneamente -= 1

            # Genero evento de inicio de atencion en caja de cliente que termino de comprar
            tipo_evento = Evento.TIPO_FIN_ATENCION_CLIENTE

            # Busco si hay una caja libre
            caja = self.grupo_cajas.obtener_caja_libre()
            if caja is not None:
                # Si hay una caja libre, le asigno la caja al cliente
                evento_actual.cliente.caja = caja
                # Genero tiempo de atencion con distribucion normal media 15 y desviacion 3
                rnd1 = truncar(random.random(), 2)
                rnd2 = truncar(random.random(), 2)
                tiempo_atencion = round(math.sqrt(-2 * math.log(rnd1)) * math.cos(2 * math.pi * rnd2) * 3 + 15, 2)
                tiempo_fin = round(evento_actual.tiempo_fin + tiempo_atencion, 2)

                # Cambio estado de caja a ocupada
                caja.estado = Caja.ESTADO_OCUPADO
                # asigno a la caja el cliente que esta siendo atendido
                caja.asignar_cliente(evento_actual.cliente)

                # asigno esa caja al cliente que esta siendo atendido
                evento_actual.cliente.caja = caja
                evento_actual.cliente.estado = Cliente.ESTADO_SIENDO_ATENDIDO

                # Agrego evento a la lista de eventos de la iteracion
                nuevo_evento = Evento(tipo_evento, rnd1_atencion_caja=rnd1, rnd2_atencion_caja=rnd2,
                                      tiempo=tiempo_atencion, tiempo_fin=tiempo_fin, caja=caja,
                                      cliente=evento_actual.cliente)
                self.manejador_eventos.agregar_evento(nuevo_evento)

                # Agrego evento a la lista de eventos de la iteracion
                eventos_iteracion.append(nuevo_evento)
            else:
                # Si no hay cajas libres, agrego el cliente a la cola de espera
                self.cola.agregar_cliente(evento_actual.cliente)
                evento_actual.cliente.estado = Cliente.ESTADO_ESPERANDO_ATENCION

        if evento_actual.tipo == Evento.TIPO_FIN_ATENCION_CLIENTE:
            # Genero fin de atencion de cliente
            tipo_evento = Evento.TIPO_FIN_ATENCION_CLIENTE
            tiempo_fin = round(evento_actual.tiempo_fin, 2)

            # Busco si hay clientes en la cola de espera
            existe_prox_cliente = self.cola.existe_proximo_cliente()
            if existe_prox_cliente is not None:
                # Genero tiempo de atencion con distribucion normal media 15 y desviacion 3
                tipo_evento = Evento.TIPO_FIN_ATENCION_CLIENTE
                rnd1 = truncar(random.random(), 2)
                rnd2 = truncar(random.random(), 2)
                tiempo_atencion = round(math.sqrt(-2 * math.log(rnd1)) * math.cos(2 * math.pi * rnd2) * 3 + 15, 2)
                tiempo_fin = round(evento_actual.tiempo_fin + tiempo_atencion, 2)
                cliente = self.cola.obtener_proximo_cliente()

                # Cambio estado de caja a ocupada
                evento_actual.caja.cambiar_a_estado_ocupado()

                # asigno a la caja el cliente que esta siendo atendido
                evento_actual.caja.asignar_cliente(cliente)

                # asigno esa caja al cliente que esta siendo atendido
                cliente.caja = evento_actual.caja
                cliente.estado = Cliente.ESTADO_SIENDO_ATENDIDO

                # Agrego evento a la lista de eventos de la iteracion
                nuevo_evento = Evento(tipo_evento, rnd1_atencion_caja=rnd1, rnd2_atencion_caja=rnd2,
                                      tiempo=tiempo_atencion, tiempo_fin=tiempo_fin, caja=evento_actual.caja,
                                      cliente=cliente)
                self.manejador_eventos.agregar_evento(nuevo_evento)

                # Agrego evento a la lista de eventos de la iteracion
                eventos_iteracion.append(nuevo_evento)
            else:
                # Si no hay clientes en la cola de espera, libero la caja
                evento_actual.caja.cambiar_a_estado_libre()
                evento_actual.caja.desasignar_cliente()

            if evento_actual.cliente.articulos > 0:
                self.cantidad_de_clientes_que_compran += 1
                self.cantidad_clientes += 1
                self.porcentaje_clientes_que_compran = round(
                    self.cantidad_de_clientes_que_compran / self.cantidad_clientes * 100, 2)
            else:
                self.cantidad_clientes += 1
                if self.cantidad_de_clientes_que_compran > 0:
                    self.porcentaje_clientes_que_compran = round(
                        self.cantidad_de_clientes_que_compran / self.cantidad_clientes * 100, 2)
                else:
                    self.porcentaje_clientes_que_compran = 0

            # Destruyo cliente
            evento_actual.cliente = None
            # Libero caja
            evento_actual.caja.liberar_caja()

            # Agrego evento a la lista de eventos de la iteracion
            nuevo_evento = Evento(tipo_evento, tiempo_fin=tiempo_fin, caja=evento_actual.caja)
            self.manejador_eventos.agregar_evento(nuevo_evento)

            # Agrego evento a la lista de eventos de la iteracion
            eventos_iteracion.append(nuevo_evento)
        return self.generar_vector_estado(evento_actual, eventos_iteracion)

    def simular(self):

        # Reestablezco atributos necesarios para el manejo de la simulacion
        self.manejador_eventos = None
        self.cola = None
        self.grupo_cajas = None
        self.cantidad_de_clientes_comprando_simultaneamente = 0
        self.cantidad_de_clientes_que_compran = 0
        self.cantidad_total_clientes = 0
        self.porcentaje_clientes_que_compran = 0
        self.rnd_tiempo_compra = None
        self.rnd_cantidad_articulos = None
        self.rnd_1_atencion_caja = None
        self.rnd_2_atencion_caja = None
        self.rnd_tiempo_proxima_llegada = None
        self.cantidad_articulos = 0
        self.cantidad_clientes = 0
        self.clientes = []

        # Creo el manejador de eventos
        self.manejador_eventos = ManejadorEventos()
        print(self.manejador_eventos)

        # Agrego evento de inicializacion
        tipo = Evento.TIPO_INICIALIZACION
        reloj = 0
        evento = Evento(tipo, None, None, None, tiempo_fin=reloj)
        self.manejador_eventos.agregar_evento(evento)

        # Creo grupo de cajas
        cola_espera = Cola(id_cola="cola_espera", clientes=[])
        cajas = []
        for i in range(0, self.cantidad_cajas):
            caja = Caja(id_caja=i, estado=Caja.ESTADO_LIBRE, cliente=None)
            cajas.append(caja)
        self.grupo_cajas = GrupoCajas(cajas=cajas, cola=cola_espera)

        # Calculo cada cuantas simulaciones mostrar el porcentaje de simulación
        if self.tiempo_simulacion <= 100:
            paso_muestra_datos = 1
        else:
            paso_muestra_datos = round(self.tiempo_simulacion / 50)
        proxima_muestra_datos = paso_muestra_datos

        # Flujo principal de la simulacion
        ultimo_vector_estado_agregado = True
        cantidad_iteraciones_agregadas = 0
        iteraciones_simuladas = []

        while 1:

            # Controlo que el reloj aún no supere el tiempo de simulación
            vector_estado_proximo = self.simular_iteracion()
            if vector_estado_proximo.get("reloj") > self.tiempo_simulacion:
                break

            # Si no se salió del bucle, seteo que no se agrego el último vector de estado
            ultimo_vector_estado_agregado = False

            # Seteo vector estado
            vector_estado = vector_estado_proximo

            # Agrego iteración a iteraciones simuladas si el reloj y la cantidad de iteraciones están dentro de los
            # parámetros solicitados, controlando si se agregó el último vector para no agregarlo mas tarde

            if (vector_estado.get("reloj") >= self.tiempo_desde and
                    cantidad_iteraciones_agregadas < self.cantidad_iteraciones):
                ultimo_vector_estado_agregado = True
                cantidad_iteraciones_agregadas += 1
                iteraciones_simuladas.append(vector_estado)

                # Agrego id de cliente a los ids de clientes durante las iteraciones a mostrar
                if len(self.ids_clientes_iteraciones) == 0:
                    for cliente in self.clientes:
                        self.ids_clientes_iteraciones.append(cliente.id)
                else:
                    if self.ultimo_id_cliente != self.ids_clientes_iteraciones[-1]:
                        self.ids_clientes_iteraciones.append(self.ultimo_id_cliente)

            # Muestro porcentaje de simulación cuando corresponda
            if vector_estado.get("reloj") >= proxima_muestra_datos:
                porcentaje = round(vector_estado.get("reloj") / self.tiempo_simulacion * 100)
                self.controlador.mostrar_porcentaje_simulacion(porcentaje)
                while proxima_muestra_datos <= vector_estado.get("reloj"):
                    proxima_muestra_datos += paso_muestra_datos
        # Agrego ultimo vector de estado si aún no se agregó o modifico el último agregado si si se hizo
        if not ultimo_vector_estado_agregado:
            vector_estado = vector_estado_proximo
            vector_estado["clientes"] = {}
            iteraciones_simuladas.append(vector_estado)

        # Genero diccionario con informacion sobre la simulacion

        ids_cajas = []
        if self.grupo_cajas:
            ids_cajas = [caja.id for caja in self.grupo_cajas.cajas]

        ids_cola_cajas = [self.grupo_cajas.cola.id]

        ids_clientes = self.ids_clientes_iteraciones
        informacion_simulacion = {
            "ids_cajas": ids_cajas,
            "ids_cola_cajas": ids_cola_cajas,
            "ids_clientes": ids_clientes,
            "cantidad_iteraciones_realizadas": iteraciones_simuladas[-1].get("n_iteracion"),
        }

        # Muestro porcentaje de simulación final
        self.controlador.mostrar_porcentaje_simulacion(100)

        # Devuelvo iteraciones simuladas de interés
        return iteraciones_simuladas, informacion_simulacion
