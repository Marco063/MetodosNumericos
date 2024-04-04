from PyQt5.QtWidgets import *

from win32api import GetSystemMetrics

from View.Biseccion import BiseccionPanel
from View.GaussSeidel import GaussSeidelPanel
from View.Menu import MenuPanel
from View.PuntoFijo import PuntoFijoPanel
from View.Secante import SecantePanel
from View.Trapecio import TrapecioPanel
from View.Simpson import SimpsonPanel
from View.Consideraciones import Consideraciones


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proyecto")
        self.__initialize()
        self.__asingController()
        self.setCentralWidget(self.__stack)
        self.setFixedSize(540, GetSystemMetrics(1)-130)
        self.show()

    def __initialize(self):
        self.__stack = QStackedWidget()
        self.__menu = MenuPanel()
        self.__stack.addWidget(self.__menu)
        self.__puntoFijo = PuntoFijoPanel()
        self.__stack.addWidget(self.__puntoFijo)
        self.__biseccion = BiseccionPanel()
        self.__stack.addWidget(self.__biseccion)
        self.__secante = SecantePanel()
        self.__stack.addWidget(self.__secante)
        self.__trapecio = TrapecioPanel()
        self.__stack.addWidget(self.__trapecio)
        self.__simpson = SimpsonPanel()
        self.__stack.addWidget(self.__simpson)
        self.__gaussSeidel = GaussSeidelPanel()
        self.__stack.addWidget(self.__gaussSeidel)
        self.__consideraciones = Consideraciones()
        self.__stack.addWidget(self.__consideraciones)

    def __asingController(self):
        self.__menu.asingController(self)
        self.__puntoFijo.asingController(self)
        self.__biseccion.asingController(self)
        self.__secante.asingController(self)
        self.__trapecio.asingController(self)
        self.__simpson.asingController(self)
        self.__gaussSeidel.asingController(self)
        self.__consideraciones.asingController(self)

    def activate(self, section):
        if section == 'Menu':
            self.__stack.setCurrentIndex(0)
        elif section == 'PuntoFijo':
            self.__stack.setCurrentIndex(1)
        elif section == 'Biseccion':
            self.__stack.setCurrentIndex(2)
        elif section == 'Secante':
            self.__stack.setCurrentIndex(3)
        elif section == 'Trapecio':
            self.__stack.setCurrentIndex(4)
        elif section == 'Simpson':
            self.__stack.setCurrentIndex(5)
        elif section == 'GaussSeidel':
            self.__stack.setCurrentIndex(6)
        elif section == 'Consideraciones':
            self.__stack.setCurrentIndex(7)


