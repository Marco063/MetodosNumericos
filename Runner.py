import sys

from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import QApplication
from View.MainWindow import MainWindow

app = QApplication(sys.argv)
app.setFont(QFont("Comic Sans MS",12))

window = MainWindow()

app.exec()

