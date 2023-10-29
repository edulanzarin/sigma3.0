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
from PyQt5.QtCore import Qt, pyqtSignal
from processing_window import ProcessingWindow
from empresa_sql_thread import EmpresaSQLThread
from error_window import MyErrorMessage
from banco_sql_thread import BancoSQLThread
from carregar_thread import CarregarThread
from processar_thread import ProcessarThread


class EmpresasWindow(QWidget):
    carregamento_finished = pyqtSignal()
    processamento_finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.combined_df = None
        self.folder_path = ""
        self.carregar_thread = None
        self.processar_thread = None

        self.combo_empresas = QComboBox()
        self.combo_bancos = QComboBox()

        self.extrato_label = QLabel("Clique para selecionar o extrato")
        self.extrato_label.setStyleSheet(
            "QLabel {"
            "border: 0.5px solid silver;"
            "border-radius: 1.2px;"
            "padding: 2.6px;"
            "font-size: 11px;"
            "}"
        )
        self.extrato_label.setCursor(Qt.PointingHandCursor)
        self.extrato_label.setOpenExternalLinks(False)
        self.extrato_label.mousePressEvent = self.choose_extrato
        self.is_extrato = False

        self.pagamentos_label = QLabel("Clique para selecionar os comprovantes")
        self.pagamentos_label.setStyleSheet(
            "QLabel {"
            "border: 0.5px solid silver;"
            "border-radius: 1.2px;"
            "padding: 2.6px;"
            "font-size: 11px;"
            "}"
        )
        self.pagamentos_label.setCursor(Qt.PointingHandCursor)
        self.pagamentos_label.setOpenExternalLinks(False)
        self.pagamentos_label.mousePressEvent = self.choose_pagamentos
        self.is_folder = False
        self.carregar_button = self.create_carregar_button(
            "", self.carregar_button_clicked
        )
        self.carregar_button.setEnabled(self.is_folder)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(
            ["Data", "Débito", "Crédito", "Valor", "Descrição"]
        )
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.process_button = self.create_button(
            "Processar", self.process_button_clicked
        )
        self.process_button.setEnabled(self.is_extrato)

        self.conciliar_button = self.create_button(
            "Conciliar", self.conciliar_button_clicked
        )
        self.conciliar_button.setEnabled(False)

        self.save_button = self.create_button("Salvar", self.save_button_clicked)
        self.save_button.setEnabled(False)

        self.init_layout()
        self.init_sql_empresa_thread()
        self.init_sql_banco_thread()

    def create_button(self, text, on_click):
        button = QPushButton(text)
        button.setStyleSheet("QPushButton { max-width: 80px; font-size: 12px;}")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(on_click)
        return button

    def create_carregar_button(self, text, on_click):
        button = QPushButton(text)
        button.setStyleSheet(
            "QPushButton { max-width: 18px; max-height: 18px; font-size: 10px;}"
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

    def create_pagamentos_layout(self, icon_name, widget, button):
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
        layout.addWidget(self.process_button)
        layout.addWidget(self.conciliar_button)
        layout.addWidget(self.save_button)
        layout.addStretch(1)
        return layout

    def init_layout(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        main_layout.addLayout(self.create_icon_layout("list.png", self.combo_empresas))
        main_layout.addLayout(self.create_icon_layout("bank.png", self.combo_bancos))
        main_layout.addLayout(self.create_icon_layout("pdf.png", self.extrato_label))
        main_layout.addLayout(
            self.create_pagamentos_layout(
                "pagamento.png", self.pagamentos_label, self.carregar_button
            )
        )

        main_layout.addLayout(self.create_button_layout())
        main_layout.addWidget(self.table_widget)

        self.setLayout(main_layout)

    def init_sql_empresa_thread(self):
        self.sql_thread = EmpresaSQLThread()
        self.sql_thread.empresa_ready.connect(self.fill_combo_empresas)
        self.load_empresas()

    def init_sql_banco_thread(self):
        self.sql_thread = BancoSQLThread()
        self.sql_thread.banco_ready.connect(self.fill_combo_bancos)
        self.load_bancos()

    def fill_combo_empresas(self, data):
        if data:
            self.combo_empresas.clear()
            for codigo, nome in data:
                self.combo_empresas.addItem(f"{codigo} - {nome}")

    def load_empresas(self):
        query = "SELECT codigo_empresa, nome_empresa FROM empresas"
        self.sql_thread.execute_query_empresa(query)

    def fill_combo_bancos(self, data):
        if data:
            self.combo_bancos.clear()
            for codigo, nome in data:
                self.combo_bancos.addItem(f"{codigo} - {nome}")

    def load_bancos(self):
        query = "SELECT codigo_banco, nome_banco FROM bancos"
        self.sql_thread.execute_query_banco(query)

    def choose_extrato(self, event):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Escolher o extrato em PDF",
            "",
            "Arquivos PDF (*.pdf);;Todos os Arquivos (*)",
            options=options,
        )
        if file_name:
            self.extrato_file_path = file_name
            self.extrato_label.setText(file_name)
            self.is_extrato = True
        else:
            self.is_extrato = False
        self.process_button.setEnabled(self.is_extrato)

    def process_button_clicked(self, event):
        if self.extrato_file_path:
            self.process_button.setEnabled(False)
            self.processing_window = ProcessingWindow(self)
            self.processing_window.show()
            selected_banco = self.combo_bancos.currentText()
            selected_banco = selected_banco.split(" - ")[0]
            self.processar_thread = ProcessarThread(
                self.extrato_file_path, selected_banco, self.combined_df
            )
            self.processar_thread.pdf_processed.connect(self.processar_thread_finished)
            self.processar_thread.finished.connect(self.processing_window.close)
            self.processar_thread.finished.connect(
                lambda: self.extrato_label.setText("Extrato carregado")
            )
            self.processar_thread.start()

    def processar_thread_finished(self, extrato_df):
        self.extrato_df = extrato_df
        self.processamento_finished.emit()

    def choose_pagamentos(self, event):
        self.folder_path = QFileDialog.getExistingDirectory(
            self, "Escolher uma pasta com comprovantes de pagamentos"
        )
        if self.folder_path:
            self.pagamentos_label.setText(self.folder_path)
            self.is_folder = True
        else:
            self.is_folder = False
        self.carregar_button.setEnabled(self.is_folder)

    def carregar_button_clicked(self):
        if self.folder_path:
            self.carregar_button.setEnabled(False)
            self.processing_window = ProcessingWindow(self)
            self.processing_window.show()
            self.carregar_thread = CarregarThread(self.folder_path)
            self.carregar_thread.finished.connect(self.carregar_thread_finished)
            self.carregar_thread.finished.connect(self.processing_window.close)
            self.carregar_thread.finished.connect(
                lambda: self.pagamentos_label.setText("Comprovantes carregados")
            )
            self.carregar_thread.start()

    def carregar_thread_finished(self, combined_df):
        self.combined_df = combined_df
        self.carregamento_finished.emit()

    def conciliar_button_clicked(self):
        pass

    def save_button_clicked(self):
        if hasattr(self, "processing_window"):
            self.processing_window.close()


def main():
    app = QApplication(sys.argv)
    window = EmpresasWindow()
    window.show()
    processing_window = ProcessingWindow(window)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
