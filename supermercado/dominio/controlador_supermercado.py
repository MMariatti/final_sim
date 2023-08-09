from supermercado.dominio.clases.simulador import Simulador


class ControlladorSupermercado:
    # Atributos para interaccion con la ventana
    ventana = None

    def __init__(self, ventana=None):
        self.ventana = ventana

    def mostrar_porcentaje_simulacion(self, porcentaje):
        self.ventana.mostrar_porcentaje_simulacion(porcentaje)

    def simular(self, tiempo_simulacion, tiempo_desde, cantidad_iteraciones, tiempo_llegada_cliente,
                tiempo_atencion_caja, tiempo_compra_articulos_cliente, cantidad_cajas, cantidad_clientes,
                cantidad_maxima_clientes, cantidad_de_clientes_que_compran, cantidad_total_clientes,
                porcentaje_clientes_que_compran):
        simulador = Simulador(self, tiempo_simulacion, tiempo_desde, cantidad_iteraciones, tiempo_llegada_cliente,
                              tiempo_atencion_caja, tiempo_compra_articulos_cliente, cantidad_cajas, cantidad_clientes,
                              cantidad_maxima_clientes, cantidad_de_clientes_que_compran, cantidad_total_clientes,
                              porcentaje_clientes_que_compran)

        # Realizo simulación
        iteraciones_simuladas, informacion_simulacion = simulador.simular()

        # Retorno iteraciones simuladas
        return iteraciones_simuladas, informacion_simulacion
