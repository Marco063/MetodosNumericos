from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, \
    QScrollArea, QTextEdit
from PyQt5.QtCore import Qt

class Consideraciones(QWidget):
    __no = 2

    def __init__(self):
        super().__init__()
        self.__initialize()

    def __initialize(self):
        layout = QVBoxLayout()

        header = QHBoxLayout()
        self.__backButton = QPushButton("<Regresar")
        header.addWidget(self.__backButton)
        header.addItem(QSpacerItem(15, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        titleLabel = QLabel("CONSIDERACIONES")
        header.addWidget(titleLabel)
        header.addItem(QSpacerItem(15, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addItem(header)
        layout.addItem(QSpacerItem(40, 80, QSizePolicy.Expanding, QSizePolicy.Minimum))



        self.__errorMsm = QLabel()
        self.__errorMsm.setFixedSize(500, 500)
        self.__errorMsm.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.__errorMsm.setWordWrap(True)
        self.__errorMsms = QScrollArea()
        self.__errorMsms.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__errorMsms.setWidget(self.__errorMsm)
        resultado = "n = valor a ingresar\n!!!!Para expresiones usar!!!!:\nPotencia: np.power(n, valor a elevar) o **\nSuma: +\nResta: -\nMultiplicacion: *\nDivision: /\nSeparacion de expresiones: ()\n!!!!Para funciones trigonométricas usar!!!!:\nSeno: np.sin(n)\nCoseno: np.cos(n)\nTangente: np.tan(n)\n!!!!Para caracteres especiales usar!!!!:\ne: np.exp(1)\npi: np.pi"
        self.__errorMsm.setText(resultado)
        layout.addWidget(self.__errorMsms)

        self.setLayout(layout)





    def asingController(self, controller):
        self.__backButton.clicked.connect(lambda: controller.activate('Menu'))



