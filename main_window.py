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
from conciliacao_window import ConciliacoesWindow
from capitalsix_window import CapitalSixWindow
from sqlquery_window import SqlQueryWindow


class MainWindow(QMainWindow):
    def __init__(self, id_usuario):
        super().__init__()

        self.id_usuario = id_usuario
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
        capitalsix_tab = QWidget()
        sqlquery_tab = QWidget()

        empresas_icon = QIcon(r".\assets\company.png")
        conciliacoes_icon = QIcon(r".\assets\lupe.png")
        capitalsix_icon = QIcon(r".\assets\capitalsix.png")
        sqlquery_icon = QIcon(r".\assets\sql.png")

        self.tabs.addTab(empresas_tab, empresas_icon, "Empresas")
        self.tabs.addTab(conciliacoes_tab, conciliacoes_icon, "Conciliações")
        self.tabs.addTab(capitalsix_tab, capitalsix_icon, "Capital Six")
        self.tabs.addTab(sqlquery_tab, sqlquery_icon, "Sql Query")

        empresas_tab_layout = QVBoxLayout()
        self.empresas_window = EmpresasWindow()
        empresas_tab_layout.addWidget(self.empresas_window)
        empresas_tab_layout.setStretch(0, 1)
        empresas_tab.setLayout(empresas_tab_layout)

        conciliacoes_tab_layout = QVBoxLayout()
        self.conciliacoes_window = ConciliacoesWindow()
        conciliacoes_tab_layout.addWidget(self.conciliacoes_window)
        conciliacoes_tab_layout.setStretch(0, 1)
        conciliacoes_tab.setLayout(conciliacoes_tab_layout)

        capitalsix_tab_layout = QVBoxLayout()
        self.capitalsix_window = CapitalSixWindow()
        capitalsix_tab_layout.addWidget(self.capitalsix_window)
        capitalsix_tab_layout.setStretch(0, 1)
        capitalsix_tab.setLayout(capitalsix_tab_layout)

        sqlquery_tab_layout = QVBoxLayout()
        self.sqlquery_window = SqlQueryWindow()
        sqlquery_tab_layout.addWidget(self.sqlquery_window)
        sqlquery_tab_layout.setStretch(0, 1)
        sqlquery_tab.setLayout(sqlquery_tab_layout)

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
