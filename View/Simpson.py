import numpy as np
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QTextEdit
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import Model.Simpson as simpsonModel

class SimpsonPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.__initialize()

    def __initialize(self):
        layout = QVBoxLayout()

        header = QHBoxLayout()
        self.__backButton = QPushButton("<Regresar")
        header.addWidget(self.__backButton)
        header.addItem(QSpacerItem(15, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        titleLabel = QLabel("SIMPSON")
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
        aLabel = QLabel("a=")
        xRow.addWidget(aLabel)
        self.__aInput = QTextEdit()
        self.__aInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__aInput.setFixedHeight(50)
        xRow.addWidget(self.__aInput)
        bLabel = QLabel("b=")
        xRow.addWidget(bLabel)
        self.__bInput = QTextEdit()
        self.__bInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__bInput.setFixedHeight(50)
        xRow.addWidget(self.__bInput)
        nLabel = QLabel("n=")
        xRow.addWidget(nLabel)
        self.__nInput = QTextEdit()
        self.__nInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__nInput.setFixedHeight(50)
        xRow.addWidget(self.__nInput)
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
        layout.addWidget(self.__errorMsm)

        self.__runButton = QPushButton("Hallar el área bajo la curva")
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
            self.__aInput.toPlainText(),
            self.__bInput.toPlainText(),
            self.__nInput.toPlainText(),
            self.__xInicialInput.toPlainText(),
            self.__xFinalInput.toPlainText()
        ]
        if '' in data:
            self.__errorMsm.setStyleSheet("color: red")
            self.__errorMsm.setText("Diligencie todos los campos antes de empezar")
        else:
            self.__figure.clear()
            ax = self.__figure.add_subplot(111)
            resultado, error, lista, medios = simpsonModel.proceso(data)
            if "Error" in str(resultado):
                self.__errorMsm.setStyleSheet("color: red")
                self.__errorMsm.setText(resultado)
            else:
                self.__showGraph(data, lista, medios, resultado)
                self.__canvas.draw()
                # self.__toolbar.setVisible(True)
                self.__canvas.setVisible(True)
                self.__errorMsm.setStyleSheet("color: black")
                self.__errorMsm.setText("Área: "+ str(resultado)+ "\nError: "+str(error))

    def __showGraph(self, data, lista, medios, resultado):
        self.__figure.clear()
        ax = self.__figure.add_subplot(111)

        n = eval(data[3])
        fx = lambda x: eval(data[0])

        linespace = np.linspace(eval(data[4]), eval(data[5]), 100)

        ax.axvline(0, color='k')
        ax.axhline(0, 0, color='k')
        ax.plot(linespace, fx(linespace), 'c', label='f(x)')
        for i in range(n):
            plt.plot(medios[i], 0, 'ro')
            x_trap_i = [lista[i], lista[i + 1]]
            y_trap_i = [fx(lista[i]), fx(lista[i + 1])]
            if i < n - 1:
                ax.fill_between(x_trap_i, y_trap_i, color='b', alpha=0.5)
            else:
                ax.fill_between(x_trap_i, y_trap_i, color='b', alpha=0.5, label='Área: ' + str(resultado))
        ax.set_title('Simpson')
        ax.legend()