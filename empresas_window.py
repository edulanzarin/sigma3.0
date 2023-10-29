import sys
import pandas as pd
from unidecode import unidecode
from datetime import date
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
    QTableWidgetItem,
    QInputDialog,
    QMessageBox,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from processing_window import ProcessingWindow
from empresa_sql_thread import EmpresaSQLThread
from banco_sql_thread import BancoSQLThread
from carregar_thread import CarregarThread
from processar_thread import ProcessarThread
from load_data_thread import LoadDataThread
from conciliar_thread import ConciliarThread
from connect_database import conectar_banco
from error_window import MyErrorMessage


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
        self.table_widget.setColumnCount(6)
        self.table_widget.setColumnHidden(0, True)
        self.table_widget.setHorizontalHeaderLabels(
            ["Id", "Data", "Débito", "Crédito", "Valor", "Descrição"]
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
        button.setIcon((QIcon(r".\assets\upload.png")))
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
        self.table_widget.itemDoubleClicked.connect(self.edit_table_cell)

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
            sorted_data = sorted(data, key=lambda x: x[0])
            self.combo_empresas.clear()
            for codigo, nome in sorted_data:
                self.combo_empresas.addItem(f"{codigo} - {nome}")

    def load_empresas(self):
        query = "SELECT codigo_empresa, nome_empresa FROM empresas"
        self.sql_thread.execute_query_empresa(query)

    def fill_combo_bancos(self, data):
        if data:
            sorted_data = sorted(data, key=lambda x: x[0])
            self.combo_bancos.clear()
            for codigo, nome in sorted_data:
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
            self.disable_buttons
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
        self.start_load_data_thread()

    def start_load_data_thread(self):
        self.load_data_thread = LoadDataThread()
        self.load_data_thread.data_loaded.connect(self.update_table_widget)
        self.load_data_thread.start()

    def update_table_widget(self, data):
        self.table_widget.setRowCount(0)
        for row in data:
            rowPosition = self.table_widget.rowCount()
            self.table_widget.insertRow(rowPosition)

            for col, value in enumerate(row):
                if col == 1 and isinstance(
                    value, date
                ):  # Ajuste para a segunda coluna (data)
                    value = value.strftime("%d/%m/%Y")
                if (
                    col == 2 or col == 3
                ) and value is None:  # Ajuste para as colunas de débito e crédito
                    value = ""
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(rowPosition, col, item)
        self.save_button.setEnabled(True)
        self.conciliar_button.setEnabled(True)

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
        self.conciliar_button.setEnabled(False)
        self.processing_window = ProcessingWindow(self)
        self.processing_window.show()
        codigo_empresa = self.combo_empresas.currentText().split(" - ")[0]
        self.conciliar_thread = ConciliarThread(codigo_empresa)
        self.conciliar_thread.conciliacao_done.connect(self.start_load_data_thread)
        self.conciliar_thread.finished.connect(self.processing_window.close)
        self.conciliar_thread.start()

    def save_button_clicked(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar em Excel",
            "",
            "Arquivos Excel (*.xlsx);;Todos os Arquivos (*)",
            options=options,
        )
        if file_name:
            df = pd.DataFrame()
            header_items = []

            for col in range(1, self.table_widget.columnCount()):
                header_items.append(self.table_widget.horizontalHeaderItem(col).text())

            data = []
            for row in range(self.table_widget.rowCount()):
                row_data = []
                for col in range(1, self.table_widget.columnCount()):
                    item = self.table_widget.item(row, col)
                    if item:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                data.append(row_data)
            df = pd.DataFrame(data, columns=header_items)
            try:
                df.to_excel(file_name, index=False)
                QMessageBox.information(
                    self, "Salvo com sucesso", f"A tabela foi salva em {file_name}."
                )
            except Exception as e:
                error_message = MyErrorMessage()
                error_message.showMessage("Erro ao salvar arquivo " + str(e))
                error_message.exec_()

    def disable_buttons(self):
        self.carregar_button.setEnabled(False)
        self.process_button.setEnabled(False)
        self.conciliar_button.setEnabled(False)
        self.save_button.setEnabled(False)

    def atualizar_coluna_na_bd(self, row, col, new_value):
        conn = conectar_banco()
        cursor = conn.cursor()

        id_transacao = self.table_widget.item(row, 0).text()
        col_name = self.table_widget.horizontalHeaderItem(col).text()
        col_name = unidecode(col_name).replace("ç", "c").lower()
        update_query = f"UPDATE transacoes SET {col_name} = %s WHERE id_transacao = %s"
        values = (new_value, id_transacao)

        cursor.execute(update_query, values)
        conn.commit()
        cursor.close()
        conn.close()

    def edit_table_cell(self, item):
        col_index = item.column()
        if col_index in [2, 3]:
            current_value = item.text()
            new_value, ok = QInputDialog.getText(
                self,
                f"Editar {self.table_widget.horizontalHeaderItem(col_index).text()}",
                f"Editar {self.table_widget.horizontalHeaderItem(col_index).text()}:",
                text=current_value,
            )
            if ok:
                item.setText(new_value)
                row = item.row()
                self.atualizar_coluna_na_bd(row, col_index, new_value)


def main():
    app = QApplication(sys.argv)
    window = EmpresasWindow()
    window.show()
    processing_window = ProcessingWindow(window)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
