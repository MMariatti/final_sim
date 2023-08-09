import math
from PyQt5 import uic
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from supermercado.dominio.controlador_supermercado import *
from supermercado.soporte.validador_enteros import ValidadorEnteros
from supermercado.soporte.validador_decimales import ValidadorDecimales
from supermercado.soporte.ruta import Ruta


class VentanaSupermercado(QMainWindow):
    # Atributos para interacción con el controlador
    app = None
    controlador = None
    iteraciones_simuladas = None
    informacion_simulacion = None

    pagina_actual = None
    cantidad_paginas = None
    tamanio_pagina = 100

    def __init__(self, app):
        # Guardo app
        self.app = app
        # Genero ventana a partir de la ui y creo controlador
        QMainWindow.__init__(self)
        uic.loadUi(Ruta.generar_ruta("interfaz/ventana_supermercado.ui"), self)
        self.controlador = ControlladorSupermercado(self)

        # Agrego validadores a los campos
        validador_7_enteros = ValidadorEnteros(7)
        validador_3_enteros = ValidadorEnteros(3)
        validador_2_enteros = ValidadorEnteros(2)
        validador_decimales = ValidadorDecimales(4, 2)
        self.txt_tiempo_simulacion.setValidator(validador_7_enteros)
        self.txt_tiempo_desde.setValidator(validador_7_enteros)
        self.txt_cantidad_iteraciones.setValidator(validador_7_enteros)

        # Conecto los botones con los eventos
        self.btn_pagina_anterior_1.clicked.connect(self.accion_volver_1_pagina)
        self.btn_pagina_anterior_10.clicked.connect(self.accion_volver_10_paginas)
        self.btn_pagina_siguiente_1.clicked.connect(self.accion_siguiente_1_pagina)
        self.btn_pagina_siguiente_10.clicked.connect(self.accion_siguiente_10_paginas)

        self.btn_limpiar.clicked.connect(self.accion_limpiar)
        self.btn_simular.clicked.connect(self.accion_simular)

    def accion_volver_1_pagina(self):

        # verifico que se haya realizado una simulación
        if self.iteraciones_simuladas is not None:

            # Calculo nueva página controlando límites
            nueva_pagina = self.pagina_actual
            if (nueva_pagina - 1) < 1:
                nueva_pagina = 1
            else:
                nueva_pagina -= 1

            # Vuelvo a carga la tabla si corresponde
            if nueva_pagina != self.pagina_actual:
                self.pagina_actual = nueva_pagina
                self.cargar_tabla_iteraciones_simuladas()
                self.lbl_informacion_paginas.setText(str(self.pagina_actual) + "/" + str(self.cantidad_paginas))

    def accion_volver_10_paginas(self):

        # verifico que se haya realizado una simulación
        if self.iteraciones_simuladas is not None:

            # Calculo nueva página controlando límites
            nueva_pagina = self.pagina_actual
            if (nueva_pagina - 10) < 1:
                nueva_pagina = 1
            else:
                nueva_pagina -= 10

            # Vuelvo a carga la tabla si corresponde
            if nueva_pagina != self.pagina_actual:
                self.pagina_actual = nueva_pagina
                self.cargar_tabla_iteraciones_simuladas()
                self.lbl_informacion_paginas.setText(str(self.pagina_actual) + "/" + str(self.cantidad_paginas))

    def accion_siguiente_1_pagina(self):

        # verifico que se haya realizado una simulación
        if self.iteraciones_simuladas is not None:

            # Calculo nueva página controlando límites
            nueva_pagina = self.pagina_actual
            if (nueva_pagina + 1) > self.cantidad_paginas:
                nueva_pagina = self.cantidad_paginas
            else:
                nueva_pagina += 1

            # Vuelvo a carga la tabla si corresponde
            if nueva_pagina != self.pagina_actual:
                self.pagina_actual = nueva_pagina
                self.cargar_tabla_iteraciones_simuladas()
                self.lbl_informacion_paginas.setText(str(self.pagina_actual) + "/" + str(self.cantidad_paginas))

    def accion_siguiente_10_paginas(self):

        # verifico que se haya realizado una simulación
        if self.iteraciones_simuladas is not None:

            # Calculo nueva página controlando límites
            nueva_pagina = self.pagina_actual
            if (nueva_pagina + 10) > self.cantidad_paginas:
                nueva_pagina = self.cantidad_paginas
            else:
                nueva_pagina += 10

            # Vuelvo a carga la tabla si corresponde
            if nueva_pagina != self.pagina_actual:
                self.pagina_actual = nueva_pagina
                self.cargar_tabla_iteraciones_simuladas()
                self.lbl_informacion_paginas.setText(str(self.pagina_actual) + "/" + str(self.cantidad_paginas))

    def accion_limpiar(self):

        # Restauro valores por defecto de interfaz y limpio tabla
        self.limpiar_datos()
        self.limpiar_interfaz()
        self.limpiar_tabla()
        self.preparar_tabla()
        self.mostrar_porcentaje_simulacion()
        self.mostrar_porcentaje_datos()
        self.mostrar_cantidad_iteraciones_realizadas()

    def accion_simular(self):
        tiempo_simulacion = None
        tiempo_desde = None
        cantidad_iteraciones = None
        tiempo_llegada_cliente = None
        if self.txt_tiempo_simulacion.text() != "":
            tiempo_simulacion = int(self.txt_tiempo_simulacion.text())
        if self.txt_tiempo_desde.text() != "":
            tiempo_desde = int(self.txt_tiempo_desde.text())
        if self.txt_cantidad_iteraciones.text() != "":
            cantidad_iteraciones = int(self.txt_cantidad_iteraciones.text())

        if tiempo_simulacion is None or tiempo_simulacion <= 0:
            self.mostrar_mensaje("Error", "El tiempo a simular tiene que ser mayor a cero")
            return
        if tiempo_desde is None:
            self.mostrar_mensaje("Error", "El tiempo desde el cuál mostrar la simulación no puede ser vacío")
            return
        if cantidad_iteraciones is None or cantidad_iteraciones <= 0:
            self.mostrar_mensaje("Error", "La cantidad de iteraciones a mostrar de la simulación tiene que ser mayor a "
                                          "cero")
            return
        if tiempo_desde > tiempo_simulacion:
            self.mostrar_mensaje("Error", "El tiempo desde el cuál mostrar la simulación no puede ser mayor a la "
                                          "cantidad de tiempo simulado")
            return

        # Limpio elementos de interfaz
        self.limpiar_tabla()
        self.mostrar_porcentaje_simulacion()
        self.mostrar_porcentaje_datos()
        self.mostrar_cantidad_iteraciones_realizadas()

        # Realizo simulacion y obtengo iteraciones a mostrar
        self.iteraciones_simuladas, self.informacion_simulacion = self.controlador.simular(tiempo_simulacion,
                                                                                           tiempo_desde,
                                                                                           cantidad_iteraciones,
                                                                                           tiempo_llegada_cliente=tiempo_llegada_cliente,
                                                                                           tiempo_atencion_caja=None,
                                                                                           tiempo_compra_articulos_cliente=None,
                                                                                           cantidad_cajas=3,
                                                                                           cantidad_clientes=None,
                                                                                           cantidad_maxima_clientes=None,
                                                                                           cantidad_de_clientes_que_compran=None,
                                                                                           cantidad_total_clientes=None,
                                                                                           porcentaje_clientes_que_compran=None,
                                                                                           )
        ids_cajas = self.informacion_simulacio.get("ids_cajas")
        ids_clientes = self.informacion_simulacion.get("ids_clientes")
        ids_cola = self.informacion_simulacion.get("ids_cola")
        self.preparar_tabla(cajas=True, ids_clientes=ids_clientes, ids_cajas=ids_cajas, ids_cola=ids_cola)

        self.pagina_actual = 1
        self.cantidad_paginas = math.ceil(len(self.iteraciones_simuladas) / self.tamanio_pagina)
        self.lbl_informacion_paginas.setText(str(self.pagina_actual) + "/" + str(self.cantidad_paginas))

        # Cargo tabl
        self.cargar_tabla_iteraciones_simuladas()

    def limpiar_datos(self):

        # Limpio datos
        self.iteraciones_simuladas = None
        self.informacion_simulacion = None
        self.pagina_actual = None
        self.cantidad_paginas = None

    def limpiar_interfaz(self):

        # Limpio txts
        self.txt_tiempo_simulacion.clear()
        self.txt_tiempo_desde.clear()
        self.txt_cantidad_iteraciones.clear()

        # Cargo valores por defecto en labels relacionados con paginación e iteraciones a mostrar
        self.lbl_informacion_paginas.setText("0/0")
        self.lbl_informacion_cantidad_total_iteraciones_realizadas.setText("0")

    def limpiar_tabla(self):

        # Limpio grilla de semanas simuladas
        self.grid_iteraciones_simuladas.clearSelection()
        self.grid_iteraciones_simuladas.setCurrentCell(-1, -1)
        self.grid_iteraciones_simuladas.setRowCount(0)

    def preparar_tabla(self, cajas=True, ids_clientes=None, ids_cajas=None, ids_cola=None):

        # Genero listas vacias en caso de parametros nulos
        if ids_clientes is None:
            ids_clientes = [0]
        if ids_cajas is None:
            ids_cajas = []
        if ids_cola is None:
            ids_cola = []

        # calculo cantidad de columnas a generar
        cantidad_cajas = len(ids_cajas)
        cantidad_colas = len(ids_cola)
        cantidad_clientes = len(ids_clientes)
        cantidad_columnas = 20
        if cajas:
            cantidad_columnas += cantidad_cajas

        # Preparo tabla de tiempo simulado
        self.grid_iteraciones_simuladas.setColumnCount(cantidad_columnas)
        i = 0

        header = QTableWidgetItem("N° iteración")
        header.setBackground(QColor(204, 204, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("Evento")
        header.setBackground(QColor(204, 204, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("Reloj")
        header.setBackground(QColor(204, 204, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("RND")
        header.setBackground(QColor(255, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("T. entre clientes")
        header.setBackground(QColor(255, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("Prox. Cliente")
        header.setBackground(QColor(255, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("RND")
        header.setBackground(QColor(205, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("Cant Articulos")
        header.setBackground(QColor(205, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("RND Compra")
        header.setBackground(QColor(205, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("Tiempo Compra")
        header.setBackground(QColor(205, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        for id_cliente in ids_clientes:
            header = QTableWidgetItem("Fin Compra (" + str(id_cliente) + ")")
            header.setBackground(QColor(205, 242, 204))
            self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)

        i += 1
        header = QTableWidgetItem("RND 1")
        header.setBackground(QColor(155, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("RND 2")
        header.setBackground(QColor(155, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("Tiempo At")
        header.setBackground(QColor(155, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)

        i += 1
        for id_caja in ids_cajas:
            header = QTableWidgetItem("Fin At (" + str(id_caja) + ")")
            header.setBackground(QColor(155, 242, 204))
            self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)

        i += 1
        for id_caja in ids_cajas:
            header = QTableWidgetItem("Estado (" + str(id_caja) + ")")
            header.setBackground(QColor(100, 242, 204))
            self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)

        i += 1
        header = QTableWidgetItem("Cola")
        header.setBackground(QColor(200, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)

        i += 1
        header = QTableWidgetItem("Cant clientes que compran")
        header.setBackground(QColor(140, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)

        i += 1
        header = QTableWidgetItem("Cant clientes totales")
        header.setBackground(QColor(140, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)

        i += 1
        header = QTableWidgetItem("% cliente que compran")
        header.setBackground(QColor(140, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)

        i += 1
        for id_cliente in ids_clientes:
            header = QTableWidgetItem("Cliente (" + str(id_cliente) + ")")
            header.setBackground(QColor(230, 242, 204))
            self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)

    def mostrar_porcentaje_simulacion(self, porcenjate=0):
        porcenjate_str = str(porcenjate).replace(".", ",")
        self.lbl_informacion_porcentaje_simulacion.setText(porcenjate_str)
        self.app.processEvents()

    def mostrar_porcentaje_datos(self, porcenjate=0):
        porcenjate_str = str(porcenjate).replace(".", ",")
        self.lbl_informacion_porcentaje_datos.setText(porcenjate_str)
        self.app.processEvents()

    def mostrar_cantidad_iteraciones_realizadas(self, cantidad_iteraciones=0):
        cantidad_iteraciones_str = str(cantidad_iteraciones)
        self.lbl_informacion_cantidad_total_iteraciones_realizadas.setText(cantidad_iteraciones_str)
        self.app.processEvents()

    def mostrar_mensaje(self, titulo, mensaje):

        # Muestro mensaje
        box = QMessageBox()
        box.setWindowTitle(titulo)
        box.setText(mensaje)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()

    def obtener_pagina_iteraciones_simuladas(self):

        # Obtengo página a partir de datos de paginación
        if len(self.iteraciones_simuladas) < self.tamanio_pagina:
            pagina = self.iteraciones_simuladas[0:len(self.iteraciones_simuladas)]
        else:
            index_inf = (self.pagina_actual - 1) * self.tamanio_pagina
            index_sup = index_inf + self.tamanio_pagina
            if index_sup > len(self.iteraciones_simuladas):
                index_sup = len(self.iteraciones_simuladas)
            pagina = self.iteraciones_simuladas[index_inf:index_sup]

        return pagina

    def cargar_tabla_iteraciones_simuladas(self):

        # Obtengo datos necesarios para generacion de headers
        ids_clientes = self.informacion_simulacion.get("ids_clientes")

        # Obtengo página de iteraciones simuladas a mostrar
        iteraciones_a_mostrar = self.obtener_pagina_iteraciones_simuladas()

        # Calculo cada cuantas filas mostrar el porcentaje de datos cargados
        if len(iteraciones_a_mostrar) <= 100:
            paso_muestra_datos = 1
        else:
            paso_muestra_datos = round(len(iteraciones_a_mostrar) / 50)
        proxima_muestra_datos = paso_muestra_datos

        # Genero filas de tabla
        self.grid_iteraciones_simuladas.setRowCount(len(iteraciones_a_mostrar))
        index_f = 0
        for iteracion_a_mostrar in iteraciones_a_mostrar:
            index_c = 0

            # Obtengo datos en formato conveniente y agrego a fila

            n_iteracion = iteracion_a_mostrar.get("n_iteracion")
            n_iteracion_str = str(n_iteracion) if n_iteracion is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(n_iteracion_str))
            index_c += 1

            evento_str = iteracion_a_mostrar.get("evento")
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(evento_str))
            index_c += 1

            reloj = iteracion_a_mostrar.get("reloj")
            reloj_str = str(reloj).replace(".", ",") if reloj is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(reloj_str))
            index_c += 1

            rnd_llegada_cliente = iteracion_a_mostrar.get("rnd_tiempo_proxima_llegada")
            rnd_llegada_cliente_str = str(rnd_llegada_cliente).replace(".",
                                                                       ",") if rnd_llegada_cliente is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(rnd_llegada_cliente_str))
            index_c += 1

            tiempo_proxima_llegada_cliente = iteracion_a_mostrar.get("tiempo_proxima_llegada")
            tiempo_proxima_llegada_cliente_str = str(tiempo_proxima_llegada_cliente).replace(".",
                                                                                             ",") if tiempo_proxima_llegada_cliente is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c,
                                                    QTableWidgetItem(tiempo_proxima_llegada_cliente_str))
            index_c += 1

            proxima_llegada_cliente = iteracion_a_mostrar.get("proxima_llegada")
            proxima_llegada_cliente_str = str(proxima_llegada_cliente).replace(".",
                                                                               ",") if proxima_llegada_cliente is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(proxima_llegada_cliente_str))
            index_c += 1

            rnd_cantidad_articulos = iteracion_a_mostrar.get("rnd_cantidad_articulos")
            rnd_cantidad_articulos_str = str(rnd_cantidad_articulos).replace(".",
                                                                             ",") if rnd_cantidad_articulos is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(rnd_cantidad_articulos_str))
            index_c += 1

            cantidad_articulos = iteracion_a_mostrar.get("cantidad_articulos")
            cantidad_articulos_str = str(cantidad_articulos) if cantidad_articulos is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(cantidad_articulos_str))
            index_c += 1

            rnd_tiempo_compra = iteracion_a_mostrar.get("rnd_tiempo_compra")
            rnd_tiempo_compra_str = str(rnd_tiempo_compra).replace(".", ",") if rnd_tiempo_compra is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(rnd_tiempo_compra_str))
            index_c += 1

            for fin_compra in iteracion_a_mostrar.get("fines_compra"):
                fin_compra_str = str(fin_compra).replace(".", ",") if fin_compra is not None else ""
                self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(fin_compra_str))
                index_c += 1

            rnd_1_atencion_caja = iteracion_a_mostrar.get("rnd_1_atencion_caja")
            rnd_1_atencion_caja_str = str(rnd_1_atencion_caja).replace(".",
                                                                       ",") if rnd_1_atencion_caja is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(rnd_1_atencion_caja_str))
            index_c += 1

            rnd_2_atencion_caja = iteracion_a_mostrar.get("rnd_2_atencion_caja")
            rnd_2_atencion_caja_str = str(rnd_2_atencion_caja).replace(".",
                                                                       ",") if rnd_2_atencion_caja is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(rnd_2_atencion_caja_str))
            index_c += 1

            tiempo_atencion_caja = iteracion_a_mostrar.get("tiempo_atencion_caja")
            tiempo_atencion_caja_str = str(tiempo_atencion_caja).replace(".",
                                                                         ",") if tiempo_atencion_caja is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(tiempo_atencion_caja_str))
            index_c += 1

            for fin_at_caja in iteracion_a_mostrar.get("fines_atencion_caja"):
                fin_at_caja_str = str(fin_at_caja).replace(".", ",") if fin_at_caja is not None else ""
                self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(fin_at_caja_str))
                index_c += 1

            for estado_caja in iteracion_a_mostrar.get("estado_cajas"):
                self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(estado_caja))
                index_c += 1

            cola = iteracion_a_mostrar.get("cola")
            cola_str = str(cola) if cola is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(cola_str))
            index_c += 1

            cantidad_clientes_que_compran = iteracion_a_mostrar.get("cantidad_clientes_que_compran")
            cantidad_clientes_que_compran_str = str(
                cantidad_clientes_que_compran) if cantidad_clientes_que_compran is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c,
                                                    QTableWidgetItem(cantidad_clientes_que_compran_str))
            index_c += 1

            cantidad_total_clientes = iteracion_a_mostrar.get("cantidad_total_clientes")
            cantidad_total_clientes_str = str(cantidad_total_clientes) if cantidad_total_clientes is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(cantidad_total_clientes_str))
            index_c += 1

            porcentaje_clientes_que_compran = iteracion_a_mostrar.get("porcentaje_clientes_que_compran")
            porcentaje_clientes_que_compran_str = str(porcentaje_clientes_que_compran).replace(".",
                                                                                               ",") if porcentaje_clientes_que_compran is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c,
                                                    QTableWidgetItem(porcentaje_clientes_que_compran_str))
            index_c += 1

            if ids_clientes is not None:
                for id_cliente in ids_clientes:
                    cliente = iteracion_a_mostrar.get("clientes").get(id_cliente)
                    if cliente:
                        estado_str = cliente.get("estado")
                        if cliente.get("caja") is not None:
                            estado_str += " (" + str(cliente.get("caja").id) + ")"
                        self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(estado_str))
                        index_c += 1
                    else:
                        estado_str = ""
                        self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(estado_str))
                        index_c += 1

            index_f += 1

            # Muestro porcentaje de datos cargados cuando corresponda

            if index_f >= proxima_muestra_datos:
                porcentaje = round(index_f * 100 / len(iteraciones_a_mostrar))
                self.mostrar_porcentaje_datos(porcentaje)
                while proxima_muestra_datos <= porcentaje:
                    proxima_muestra_datos += paso_muestra_datos

        # Muestro porcentajes de datos cargados final
        self.mostrar_porcentaje_datos(100)

    # Evento show
    def showEvent(self, QShowEvent):
        self.accion_limpiar()
