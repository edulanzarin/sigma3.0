import sys
import os
import pandas as pd
import PyPDF2
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QComboBox,
    QTableWidget,
    QHeaderView,
    QSizePolicy,
    QFileDialog,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from processing_window import ProcessingWindow
from empresa_sql_thread import EmpresaSQLThread
from error_window import MyErrorMessage


class EmpresasWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.combo_empresas = QComboBox()

        self.excel_label = QLabel("Clique para selecionar a lista de conciliações")
        self.excel_label.setStyleSheet(
            "QLabel {"
            "border: 0.5px solid silver;"
            "border-radius: 1.2px;"
            "padding: 2.6px;"
            "font-size: 11px;"
            "}"
        )
        self.excel_label.setCursor(Qt.PointingHandCursor)
        self.excel_label.setOpenExternalLinks(False)
        self.excel_label.mousePressEvent = self.choose_excel
        self.is_folder = False
        self.modelo_button = self.create_modelo_button("", self.modelo_button_clicked)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(
            ["Data", "Conta Débito", "Conta Crédito"]
        )
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.listar_button = self.create_button("Atualizar", self.listar_button_clicked)

        self.conciliar_button = self.create_button(
            "Cadastrar", self.cadastrar_button_clicked
        )
        self.conciliar_button.setEnabled(False)

        self.save_button = self.create_button("Lista", self.excel_button_clicked)
        self.save_button.setEnabled(False)

        self.init_layout()
        self.init_sql_empresa_thread()

    def create_button(self, text, on_click):
        button = QPushButton(text)
        button.setStyleSheet("QPushButton { max-width: 80px; font-size: 12px;}")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(on_click)
        return button

    def create_modelo_button(self, text, on_click):
        button = QPushButton(text)
        button.setIcon((QIcon(r".\assets\download.png")))
        button.setIconSize(QSize(15, 15))
        button.setStyleSheet(
            "QPushButton { max-width: 18px; max-height: 18px; font-size: 10px; border: none;}"
        )
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(on_click)
        return button

    def create_icon_layout(self, icon_name, widget):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        icon = QIcon(f".\\assets\\{icon_name}")
        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(18, 18))
        icon_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        max_width = int(self.width() * 0.03)
        icon_label.setMaximumWidth(max_width)
        layout.addWidget(icon_label)
        layout.addWidget(widget)
        return layout

    def create_excel_layout(self, icon_name, widget, button):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        icon = QIcon(f".\\assets\\{icon_name}")
        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(18, 18))
        icon_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        max_width = int(self.width() * 0.03)
        icon_label.setMaximumWidth(max_width)
        layout.addWidget(icon_label)
        layout.addWidget(widget)
        layout.addWidget(button)
        return layout

    def create_button_layout(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addStretch(1)
        layout.addWidget(self.listar_button)
        layout.addWidget(self.conciliar_button)
        layout.addWidget(self.save_button)
        layout.addStretch(1)
        return layout

    def init_layout(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        main_layout.addLayout(self.create_icon_layout("list.png", self.combo_empresas))
        main_layout.addLayout(
            self.create_excel_layout("excel.png", self.excel_label, self.modelo_button)
        )

        main_layout.addLayout(self.create_button_layout())
        main_layout.addWidget(self.table_widget)

        self.setLayout(main_layout)

    def init_sql_empresa_thread(self):
        self.sql_thread = EmpresaSQLThread()
        self.sql_thread.empresa_ready.connect(self.fill_combo_empresas)
        self.load_empresas()

    def fill_combo_empresas(self, data):
        if data:
            self.combo_empresas.clear()
            for codigo, nome in data:
                self.combo_empresas.addItem(f"{codigo} - {nome}")

    def load_empresas(self):
        query = "SELECT codigo_empresa, nome_empresa FROM empresas"
        self.sql_thread.execute_query_empresa(query)

    def choose_excel(self, event):
        pass

    def modelo_button_clicked(self):
        data = {"DESCRICAO": [], "DEBITO": [], "CREDITO": []}
        df = pd.DataFrame(data)
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Lista de Conciliações",
            "",
            "Arquivos Excel (*.xlsx);;Todos os arquivos (*)",
            options=options,
        )
        if file_name:
            df.to_excel(file_name, index=False)

    def listar_button_clicked(self):
        pass

    def cadastrar_button_clicked(self):
        pass

    def excel_button_clicked(self):
        pass


def main():
    app = QApplication(sys.argv)
    window = EmpresasWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
