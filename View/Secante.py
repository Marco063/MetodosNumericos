import numpy as np
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem, QTextEdit, QScrollArea
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import Model.Secante as secanteModel

class SecantePanel(QWidget):
    def __init__(self):
        super().__init__()
        self.__initialize()

    def __initialize(self):
        layout = QVBoxLayout()

        header = QHBoxLayout()
        self.__backButton = QPushButton("<Regresar")
        header.addWidget(self.__backButton)
        header.addItem(QSpacerItem(15, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        titleLabel = QLabel("SECANTE")
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
        xRow = QHBoxLayout()
        xiLabel = QLabel("Xi=")
        xRow.addWidget(xiLabel)
        self.__xiInput = QTextEdit()
        self.__xiInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__xiInput.setFixedHeight(50)
        xRow.addWidget(self.__xiInput)
        xuLabel = QLabel("Xu=")
        xRow.addWidget(xuLabel)
        self.__xuInput = QTextEdit()
        self.__xuInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__xuInput.setFixedHeight(50)
        xRow.addWidget(self.__xuInput)
        layout.addItem(xRow)
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
        self.__runButton.clicked.connect(lambda: self.__sendData())

    def __sendData(self):
        self.__errorMsm.setText(" ")
        # self.__toolbar.setVisible(False)
        self.__canvas.setVisible(False)

        data = [
            self.__fxInput.toPlainText(),
            self.__xiInput.toPlainText(),
            self.__xuInput.toPlainText(),
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
            self.__figure.clear()
            ax = self.__figure.add_subplot(111)
            error, respuesta, tabla, iteracion = secanteModel.proceso(data)
            if "Error" in str(respuesta):
                self.__errorMsm.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                self.__errorMsm.setWordWrap(True)
                self.__errorMsm.setStyleSheet("color: red")
                self.__errorMsm.setText(respuesta)
                self.__errorMsm.setText(respuesta)
                self.__errorMsm.setFixedSize(500, 50)
            else:
                self.__errorMsm.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                self.__errorMsm.setWordWrap(True)
                resultado ="Raíz: "+str(respuesta)+"\nError: "+ str(error) + "\n[        i                 Xi              xi+1           ((xi+1)-xi)  ]\n"+str(tabla)
                print(resultado)
                self.__showGraph(tabla, respuesta, data)
                self.__canvas.draw()
                # self.__toolbar.setVisible(True)
                self.__canvas.setVisible(True)
                self.__errorMsm.setStyleSheet("color: black")
                self.__errorMsm.setText(resultado)
                self.__errorMsm.setFixedSize(500, (iteracion * 35))

    def __showGraph(self, tabla, raiz, data):
        self.__figure.clear()
        ax = self.__figure.add_subplot(111)

        a = eval(data[3])
        b = eval(data[4])
        fx = lambda x: eval(data[0])

        linespace = np.linspace(a, b, 100)

        ax.axvline(0, color='k')
        ax.axhline(0, 0, color='k')
        ax.plot(linespace, fx(linespace), 'c', label='f(x)')

        xi = eval(data[2])
        xi1 = eval(data[1])
        for i in range(len(tabla)):
            plt.plot(xi, fx(xi), 'go')
            plt.plot(xi1, fx(xi1), 'go')
            plt.plot(np.linspace(xi, xi1, 2), np.linspace(fx(xi), fx(xi1), 2), 'g')

            xi1 = xi
            xi = tabla[i][1]

        # if raiz != np.nan:
        ax.axvline(raiz)
        ax.plot(raiz, 0, 'ro', label='Raíz: '+ str(raiz))
        ax.set_title('Secante')
        ax.legend()
