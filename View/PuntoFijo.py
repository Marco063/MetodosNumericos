import random

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QTextEdit, QScrollArea
from PyQt5.QtCore import Qt

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import Model.Punto_Fijo as puntoFijoModel

class PuntoFijoPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.__initialize()

    def __initialize(self):
        layout = QVBoxLayout()

        header = QHBoxLayout()
        self.__backButton = QPushButton("<Regresar")
        header.addWidget(self.__backButton)
        header.addItem(QSpacerItem(15, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        titleLabel = QLabel("PUNTO FIJO")
        header.addWidget(titleLabel)
        header.addItem(QSpacerItem(15, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addItem(header)
        layout.addItem(QSpacerItem(40, 80, QSizePolicy.Expanding, QSizePolicy.Minimum))

        fxConfigLabel = QLabel("Configuración de la función")
        layout.addWidget(fxConfigLabel)
        fxRow = QHBoxLayout()
        fx = QLabel("F(x)=")
        fxRow.addWidget(fx)
        self.__fxInput = QTextEdit()
        self.__fxInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__fxInput.setFixedHeight(50)
        fxRow.addWidget(self.__fxInput)
        layout.addItem(fxRow)
        gxRow = QHBoxLayout()
        gx = QLabel("G(x)=")
        gxRow.addWidget(gx)
        self.__gxInput = QTextEdit()
        self.__gxInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__gxInput.setFixedHeight(50)
        gxRow.addWidget(self.__gxInput)
        layout.addItem(gxRow)
        x0Row = QHBoxLayout()
        x0 = QLabel("X0=")
        x0Row.addWidget(x0)
        self.__x0Input = QTextEdit()
        self.__x0Input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__x0Input.setFixedHeight(50)
        x0Row.addWidget(self.__x0Input)
        layout.addItem(x0Row)
        layout.addItem(QSpacerItem(0, 50, QSizePolicy.Expanding, QSizePolicy.Minimum))

        graficaConfigLabel = QLabel("Configuración de la grafica")
        layout.addWidget(graficaConfigLabel)
        graficaRow = QHBoxLayout()
        xInicial = QLabel("Xi=")
        graficaRow.addWidget(xInicial)
        self.__xInicialInput = QTextEdit()
        self.__xInicialInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__xInicialInput.setFixedHeight(50)
        graficaRow.addWidget(self.__xInicialInput)
        xFinal = QLabel("Xf=")
        graficaRow.addWidget(xFinal)
        self.__xFinalInput = QTextEdit()
        self.__xFinalInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__xFinalInput.setFixedHeight(50)
        graficaRow.addWidget(self.__xFinalInput)
        layout.addItem(graficaRow)
        # layout.addItem(QSpacerItem(0, 50, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.__errorMsm = QLabel()
        self.__errorMsm.setFixedSize(500, 100)
        self.__errorMsms = QScrollArea()
        self.__errorMsms.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__errorMsms.setWidget(self.__errorMsm)
        layout.addWidget(self.__errorMsms)

        self.__runButton = QPushButton("Hallar la raíz")
        layout.addWidget(self.__runButton)

        self.__respeusta = QVBoxLayout()
        self.__figure = plt.figure()
        self.__canvas = FigureCanvas(self.__figure)
        # self.__toolbar = NavigationToolbar(self.__canvas, self)
        # self.__toolbar.setVisible(False)
        self.__canvas.setVisible(False)
        # self.__respeusta.addWidget(self.__toolbar)
        self.__respeusta.addWidget(self.__canvas)

        # layout.addItem(self.__respeusta)

        self.setLayout(layout)

    def asingController(self, controller):
        self.__backButton.clicked.connect(lambda: controller.activate('Menu'))
        self.__runButton.clicked.connect(lambda: self.__sendData(controller))

    def __sendData(self, controller):
        self.__errorMsm.setText(" ")
        # self.__toolbar.setVisible(False)
        self.__canvas.setVisible(False)

        data = [
            self.__fxInput.toPlainText(),
            self.__gxInput.toPlainText(),
            self.__x0Input.toPlainText(),
            self.__xInicialInput.toPlainText(),
            self.__xFinalInput.toPlainText()
        ]
        if '' in data:
            self.__errorMsm.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.__errorMsm.setWordWrap(True)
            self.__errorMsm.setStyleSheet("color: red")
            self.__errorMsm.setText("Diligencie todos los campos antes de empezar")
            self.__errorMsm.setFixedSize(500, 50)
        else:
            respuesta, error, tabla, iteracion = puntoFijoModel.proceso(data)
            if "Error" in str(respuesta):
                self.__errorMsm.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                self.__errorMsm.setWordWrap(True)
                self.__errorMsm.setStyleSheet("color: red")
                self.__errorMsm.setText(respuesta)
                self.__errorMsm.setFixedSize(500, 50)
            else:
                self.__errorMsm.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                self.__errorMsm.setWordWrap(True)
                respuestaFinal="Raíz: "+str(respuesta)+"\nError: "+ str(error)+"\n[  i       Xi        g(x)   ]\n"+ str(tabla)
                print(respuestaFinal)
                self.__errorMsm.setFixedSize(500, (iteracion * 35))
                self.__showGraph(respuesta, data)
                self.__canvas.draw()
                # self.__toolbar.setVisible(True)
                self.__canvas.setVisible(True)
                self.__errorMsm.setStyleSheet("color: black")
                self.__errorMsm.setText(respuestaFinal)

    def __showGraph(self, raiz, data):
        self.__figure.clear()
        ax = self.__figure.add_subplot(111)

        a = eval(data[3])
        b = eval(data[4])
        fx = lambda x: eval(data[0])
        gx = lambda x: eval(data[1])

        linespace = np.linspace(a, b, 100)

        ax.plot(linespace, gx(linespace), label='g(x)')
        ax.plot(linespace, linespace, label='(y=x)')
        ax.axvline(raiz)  # Linea vertical donde cruzan la funcion

        ax.plot(raiz, 0, 'ro', label='raíz: '+ str(raiz))
        ax.set_title('Punto Fijo')
        ax.plot(linespace, fx(linespace), label='f(x)')
        ax.axvline(0, color='k')
        ax.axhline(0, 0, color='k')
        ax.legend()




