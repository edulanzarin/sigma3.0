from PyQt5.QtWidgets import QErrorMessage
from PyQt5.QtGui import QIcon


class MyErrorMessage(QErrorMessage):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Erro")
        self.setWindowIcon(QIcon(r".\assets\error.png"))
