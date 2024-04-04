from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, \
    QScrollArea, QTextEdit
from PyQt5.QtCore import Qt
import numpy as np

import Model.Seidel as seidelModel

class GaussSeidelPanel(QWidget):
    __no = 2

    def __init__(self):
        super().__init__()
        self.__initialize()
        self.__render()

    def __initialize(self):
        layout = QVBoxLayout()

        header = QHBoxLayout()
        self.__backButton = QPushButton("<Regresar")
        header.addWidget(self.__backButton)
        header.addItem(QSpacerItem(15, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        titleLabel = QLabel("GAUSS-SEIDEL")
        header.addWidget(titleLabel)
        header.addItem(QSpacerItem(15, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addItem(header)
        layout.addItem(QSpacerItem(40, 80, QSizePolicy.Expanding, QSizePolicy.Minimum))

        noLabelRow = QHBoxLayout()
        noLabelRow.addItem(QSpacerItem(15, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        noLabelRow.addWidget(QLabel("Numero de ecuaciones"))
        noLabelRow.addItem(QSpacerItem(15, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addItem(noLabelRow)
        noRow = QHBoxLayout()
        noRow.addItem(QSpacerItem(15, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.__less = QPushButton("-1")
        noRow.addWidget(self.__less)
        self.__noLabel = QLabel(str(self.__no))
        noRow.addWidget(self.__noLabel)
        self.__more = QPushButton("+1")
        noRow.addWidget(self.__more)
        noRow.addItem(QSpacerItem(15, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addItem(noRow)

        ecuacionLabel = QLabel("Sistema de ecuaciones")
        layout.addWidget(ecuacionLabel)
        self.__ecuacion = QScrollArea()
        self.__ecuacion.setFixedHeight(200)
        layout.addWidget(self.__ecuacion)
        layout.addItem(QSpacerItem(0, 50, QSizePolicy.Expanding, QSizePolicy.Minimum))

        xtLabel = QLabel("Xt")
        layout.addWidget(xtLabel)
        self.__xt = QScrollArea()
        self.__xt.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.__xt)
        # layout.addItem(QSpacerItem(0, 50, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.__errorMsm = QLabel()
        self.__errorMsm.setFixedSize(500, 100)
        self.__errorMsms = QScrollArea()
        self.__errorMsms.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__errorMsms.setWidget(self.__errorMsm)
        layout.addWidget(self.__errorMsms)


        self.__runButton = QPushButton("Hallar vector solución")
        layout.addWidget(self.__runButton)

        self.__respeusta = QVBoxLayout()
        layout.addItem(self.__respeusta)

        self.setLayout(layout)

    def __render(self):
        self.__noLabel.setText(str(self.__no))

        self.__sistemaEcuaciones = QVBoxLayout()
        self.__xtLayout = QHBoxLayout()
        # Genera lso inputs necesarios
        for i in range(self.__no):
            ecuacionLayout = QHBoxLayout()
            # inputs sistema de ecuaciones
            for j in range(self.__no):
                xInput = QTextEdit()
                xInput.setPlainText("0")
                xInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                xInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                xInput.setFixedHeight(50)
                xInput.setFixedWidth(120)
                ecuacionLayout.addWidget(xInput)
                if (j < (self.__no - 1)):
                    ecuacionLayout.addWidget(QLabel("X" + str(j+1) + "+"))
                else:
                    ecuacionLayout.addWidget(QLabel("X" + str(j+1) + "="))
            # solucion al sistema de ecuaciones
            xInput = QTextEdit()
            xInput.setPlainText("0")
            xInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            xInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            xInput.setFixedHeight(50)
            xInput.setFixedWidth(120)
            ecuacionLayout.addWidget(xInput)
            self.__sistemaEcuaciones.addItem(ecuacionLayout)
            # Xt vector solucion propuesto
            xtInput = QTextEdit()
            xtInput.setPlainText("0")
            xtInput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            xtInput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            xtInput.setFixedHeight(50)
            xtInput.setFixedWidth(200)
            self.__xtLayout.addWidget(QLabel("X"+str(i+1)+"="))
            self.__xtLayout.addWidget(xtInput)

        # Actualiza los scroll area
        ecuacionWidget = QWidget()
        ecuacionWidget.setLayout(self.__sistemaEcuaciones)
        ecuacionWidget.adjustSize()
        self.__ecuacion.setWidget(ecuacionWidget)
        xtWidget = QWidget()
        xtWidget.setLayout(self.__xtLayout)
        xtWidget.adjustSize()
        self.__xt.setWidget(xtWidget)

    def __setNo(self, value):

        # sistema de ecuaciones de 2 a 10 incognitas
        if ((self.__no + value) > 1 and (self.__no + value) < 11):
            self.__no += value
            self.__render()
            print(self.__no)

    def asingController(self, controller):
        self.__backButton.clicked.connect(lambda: controller.activate('Menu'))
        self.__less.clicked.connect(lambda: self.__setNo(-1))
        self.__more.clicked.connect(lambda: self.__setNo(+1))
        self.__runButton.clicked.connect(lambda: self.__sendData())

    def __sendData(self):

        sistemaEcuaciones = []
        b = []
        xt = []
        try:
            for i in range(self.__sistemaEcuaciones.count()):
                row = []
                for j in range(self.__no):
                    row.append(eval(self.__sistemaEcuaciones.itemAt(i).itemAt(j * 2).widget().toPlainText()))
                b.append(eval(self.__sistemaEcuaciones.itemAt(i).itemAt(
                    (self.__sistemaEcuaciones.itemAt(i).count()) - 1).widget().toPlainText()))
                sistemaEcuaciones.append(row)
            # print(sistemaEcuaciones)
            for i in range(self.__sistemaEcuaciones.count()):
                xt.append(eval(self.__xtLayout.itemAt((i * 2) + 1).widget().toPlainText()))


            dominante = True

            for i in range(len(sistemaEcuaciones)):
                diagonal_element = abs(sistemaEcuaciones[i][i])
                sum_of_non_diagonal_elements = sum(abs(sistemaEcuaciones[i][j]) for j in range(len(sistemaEcuaciones)) if j != i)
                if diagonal_element <= sum_of_non_diagonal_elements:
                    dominante = False
                    break
            if dominante:
                # self.__errorMsm.setStyleSheet("color: black")
                # self.__errorMsm.setText("Para obetener el resultado, adquiere la version premium por tan solo $8.99")
                resultado, dec, frac, iteracion=seidelModel.calcular(sistemaEcuaciones, b, xt)
                # print(sistemaEcuaciones)
                # print(b)
                # print(xt)
                # print(dec)
                # print(frac)
                # print(resultado)
                resultadofinal = "Despeje en decimal:\n"+dec+"Despeje en Fracción:\n"+frac+resultado
                if 'Error, verifique' in resultado:
                    self.__errorMsm.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                    self.__errorMsm.setWordWrap(True)
                    self.__errorMsm.setStyleSheet("color: red")
                    self.__errorMsm.setText(str(resultado))
                    self.__errorMsm.setFixedSize(500, 200)
                else:
                    self.__errorMsm.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                    self.__errorMsm.setWordWrap(True)
                    self.__errorMsm.setStyleSheet("color: black")
                    self.__errorMsm.setText(str(resultadofinal))

                    self.__errorMsm.setFixedSize(500, (iteracion*1000))
            else:
                self.__errorMsm.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                self.__errorMsm.setWordWrap(True)
                self.__errorMsm.setStyleSheet("color: red")
                self.__errorMsm.setText("La matriz no es dominante")
                self.__errorMsm.setFixedSize(500, 50)

        except:
            self.__errorMsm.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.__errorMsm.setWordWrap(True)
            self.__errorMsm.setStyleSheet("color: red")
            self.__errorMsm.setText("Error de sintaxis")
            self.__errorMsm.setFixedSize(500, 50)


