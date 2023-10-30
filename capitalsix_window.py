import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
)


class CapitalSixWindow(QWidget):
    def __init__(self):
        super().__init__()


    

def main():
    app = QApplication(sys.argv)
    window = CapitalSixWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
