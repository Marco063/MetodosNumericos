from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy


class MenuPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.__initialize()


    def __initialize(self):
        layout = QVBoxLayout()

        self.__menuLabel = QLabel("MENÚ")
        layout.addWidget(self.__menuLabel)

        layout.addItem(QSpacerItem(40, 80, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.__consideraciones = QPushButton("Consideraciones")
        layout.addWidget(self.__consideraciones)

        self.__puntoFijoButton = QPushButton("Punto Fijo")
        layout.addWidget(self.__puntoFijoButton)

        self.__biseccionButton = QPushButton("Bisección")
        layout.addWidget(self.__biseccionButton)

        self.__secanteButton = QPushButton("Secante")
        layout.addWidget(self.__secanteButton)

        self.__trapecioButton = QPushButton("Trapecio")
        layout.addWidget(self.__trapecioButton)

        self.__simpsonButton = QPushButton("Simpson")
        layout.addWidget(self.__simpsonButton)

        self.__gaussButton = QPushButton("Gauss-Seidel")
        layout.addWidget(self.__gaussButton)

        self.setLayout(layout)

    def asingController(self, controller):
        self.__consideraciones.clicked.connect(lambda: controller.activate('Consideraciones'))
        self.__puntoFijoButton.clicked.connect(lambda: controller.activate('PuntoFijo'))
        self.__biseccionButton.clicked.connect(lambda: controller.activate('Biseccion'))
        self.__secanteButton.clicked.connect(lambda: controller.activate('Secante'))
        self.__trapecioButton.clicked.connect(lambda: controller.activate('Trapecio'))
        self.__simpsonButton.clicked.connect(lambda: controller.activate('Simpson'))
        self.__gaussButton.clicked.connect(lambda: controller.activate('GaussSeidel'))


