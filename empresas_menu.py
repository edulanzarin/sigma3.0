from PyQt5.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QIcon
import sys
from qualitplacas_window import QualitPlacasWindow


class EmpresasMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        menu_bar = self.menuBar()
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)

        qualitplacas_tab = QWidget()

        self.tabs.addTab(qualitplacas_tab, "Qualitplacas")

        qualitplacas_tab_layout = QVBoxLayout()
        self.qualitplacas_window = QualitPlacasWindow()
        qualitplacas_tab_layout.addWidget(self.qualitplacas_window)
        qualitplacas_tab_layout.setContentsMargins(0, 0, 0, 0)
        qualitplacas_tab.setLayout(qualitplacas_tab_layout)

        self.setMenuBar(menu_bar)
        main_layout.addWidget(self.tabs)
        self.central_widget.setLayout(main_layout)

    def open_start_window(self):
        self.start_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmpresasMenu()
    window.show()
    sys.exit(app.exec_())
