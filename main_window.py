from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
)
from PyQt5.QtGui import QIcon
import sys
from empresas_window import EmpresasWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        icon = QIcon(r".\assets\icon.ico")
        self.setWindowIcon(icon)
        self.setWindowTitle("Sigma")
        self.setGeometry(100, 100, 800, 600)
        self.showMaximized()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        menu_bar = self.menuBar()
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)

        empresas_tab = QWidget()
        conciliacoes_tab = QWidget()

        self.tabs.addTab(empresas_tab, "Empresas")
        self.tabs.addTab(conciliacoes_tab, "Conciliações")

        empresas_tab_layout = QVBoxLayout()
        self.empresas_window = EmpresasWindow()
        empresas_tab_layout.addWidget(self.empresas_window)
        empresas_tab_layout.setStretch(0, 1)
        empresas_tab.setLayout(empresas_tab_layout)

        conciliacoes_tab_layout = QVBoxLayout()
        conciliacoes_tab.setLayout(conciliacoes_tab_layout)

        self.setMenuBar(menu_bar)
        main_layout.addWidget(self.tabs)
        self.central_widget.setLayout(main_layout)

    def open_start_window(self):
        self.start_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
