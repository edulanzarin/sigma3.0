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
from empresas_menu import EmpresasMenu
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

        lancamentos_tab = QWidget()
        conciliacoes_tab = QWidget()
        empresas_tab = QWidget()
        sqlquery_tab = QWidget()

        lancamentos_icon = QIcon(r".\assets\dolar.png")
        conciliacoes_icon = QIcon(r".\assets\lupe.png")
        empresas_icon = QIcon(r".\assets\company.png")
        sqlquery_icon = QIcon(r".\assets\sql.png")

        self.tabs.addTab(lancamentos_tab, lancamentos_icon, "Lançamentos")
        self.tabs.addTab(conciliacoes_tab, conciliacoes_icon, "Conciliações")
        self.tabs.addTab(empresas_tab, empresas_icon, "Empresas")
        self.tabs.addTab(sqlquery_tab, sqlquery_icon, "Sql Query")

        lancamentos_tab_layout = QVBoxLayout()
        self.lancamentos_window = EmpresasWindow()
        lancamentos_tab_layout.addWidget(self.lancamentos_window)
        lancamentos_tab_layout.setContentsMargins(0, 0, 0, 0)  # Remova as margens
        lancamentos_tab.setLayout(lancamentos_tab_layout)

        conciliacoes_tab_layout = QVBoxLayout()
        self.conciliacoes_window = ConciliacoesWindow()
        conciliacoes_tab_layout.addWidget(self.conciliacoes_window)
        conciliacoes_tab_layout.setContentsMargins(0, 0, 0, 0)  # Remova as margens
        conciliacoes_tab.setLayout(conciliacoes_tab_layout)

        empresas_tab_layout = QVBoxLayout()
        self.empresas_window = EmpresasMenu()
        empresas_tab_layout.addWidget(self.empresas_window)
        empresas_tab_layout.setContentsMargins(0, 0, 0, 0)  # Remova as margens
        empresas_tab.setLayout(empresas_tab_layout)

        sqlquery_tab_layout = QVBoxLayout()
        self.sqlquery_window = SqlQueryWindow()
        sqlquery_tab_layout.addWidget(self.sqlquery_window)
        sqlquery_tab_layout.setContentsMargins(0, 0, 0, 0)  # Remova as margens
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
