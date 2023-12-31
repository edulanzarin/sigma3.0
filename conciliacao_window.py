import sys
import pandas as pd
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
    QDialog,
    QInputDialog,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from processing_window import ProcessingWindow
from empresa_sql_thread import EmpresaSQLThread
from error_window import MyErrorMessage
from listar_conciliacoes_thread import ListarConciliacoesThread
from cadastrar_conciliacoes_thread import CadastrarConciliacoesThread
from cadastrar_conciliacao_dialog import CadastrarDialog
from excel_thread import ExcelProcessingThread
from connect_database import conectar_banco


class ConciliacoesWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.combo_empresas = QComboBox()
        self.editing_row = None

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

        self.cadastrar_button = self.create_button(
            "Cadastrar", self.cadastrar_button_clicked
        )

        self.excel_button = self.create_button("Lista", self.excel_button_clicked)
        self.excel_button.setEnabled(False)

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
        layout.addWidget(self.cadastrar_button)
        layout.addWidget(self.excel_button)
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
        self.table_widget.cellDoubleClicked.connect(self.edit_cell)

    def init_sql_empresa_thread(self):
        self.sql_thread = EmpresaSQLThread()
        self.sql_thread.empresa_ready.connect(self.fill_combo_empresas)
        self.load_empresas()

    def fill_combo_empresas(self, data):
        if data:
            sorted_data = sorted(data, key=lambda x: x[0])
            self.combo_empresas.clear()
            for codigo, nome in sorted_data:
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

    def listar_button_clicked(self, event):
        codigo_empresa = self.combo_empresas.currentText()
        codigo_empresa = codigo_empresa.split(" - ")[0]
        self.listar_conciliacoes_thread = ListarConciliacoesThread(codigo_empresa)
        self.listar_conciliacoes_thread.data_ready.connect(self.update_treeview)
        self.listar_conciliacoes_thread.start()

        self.processing_window = ProcessingWindow()
        self.processing_window.show()

    def update_treeview(self, data):
        self.table_widget.setRowCount(0)

        for row_data in data:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)

            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(row_position, col, item)

        self.processing_window.close()

    def cadastrar_button_clicked(self):
        cadastrar_dialog = CadastrarDialog()
        if cadastrar_dialog.exec_() == QDialog.Accepted:
            descricao, debito_text, credito_text = cadastrar_dialog.get_input_data()
            if descricao and debito_text and credito_text:
                try:
                    debito = int(debito_text)
                    credito = int(credito_text)
                except ValueError:
                    error_dialog = MyErrorMessage(
                        "Débito e Crédito devem ser números inteiros."
                    )
                    error_dialog.exec_()
                else:
                    codigo_empresa = self.combo_empresas.currentText()
                    codigo_empresa = codigo_empresa.split(" - ")[0]
                    self.cadastrar_conciliacoes_thread = CadastrarConciliacoesThread(
                        codigo_empresa, descricao, debito, credito
                    )
                    self.cadastrar_conciliacoes_thread.cadastro_ready.connect(
                        lambda: None
                    )
                    self.cadastrar_conciliacoes_thread.start()
            else:
                error_dialog = MyErrorMessage("Preencha todos os campos.")
                error_dialog.exec_()

    def choose_excel(self, event):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Escolher arquivo Excel ou CSV",
            "",
            "Arquivos Excel (*.xlsx);;Arquivos CSV (*.csv);;Todos os arquivos (*)",
            options=options,
        )

        if file_path:
            self.file_path = file_path
            self.excel_button.setEnabled(True)
        else:
            self.excel_button.setEnabled(False)

    def excel_button_clicked(self):
        if not hasattr(self, "file_path"):
            return

        codigo_empresa = self.combo_empresas.currentText().split(" - ")[0]
        self.excel_thread = ExcelProcessingThread(self.file_path, codigo_empresa)
        self.excel_thread.data_ready.connect(self.excel_processing_done)
        self.excel_thread.start()

        self.processing_window = ProcessingWindow()
        self.processing_window.show()

    def excel_processing_done(self):
        self.excel_button.setEnabled(False)
        self.listar_button_clicked(None)

    def edit_cell(self, row, column):
        if column == 0:
            # Editar descrição
            self.editing_row = row
            item = self.table_widget.item(row, column)
            current_value = item.text()
            new_value, ok = QInputDialog.getText(
                self, "Editar Descrição", "Nova descrição:", text=current_value
            )
            if ok:
                item.setText(new_value)
                self.update_database("descricao", new_value)
        elif column == 1:
            # Editar débito
            self.editing_row = row
            item = self.table_widget.item(row, column)
            current_value = item.text()
            new_value, ok = QInputDialog.getInt(
                self, "Editar Débito", "Novo valor de débito:", value=int(current_value)
            )
            if ok:
                item.setText(str(new_value))
                self.update_database("conta_debito", new_value)
        elif column == 2:
            # Editar crédito
            self.editing_row = row
            item = self.table_widget.item(row, column)
            current_value = item.text()
            new_value, ok = QInputDialog.getInt(
                self,
                "Editar Crédito",
                "Novo valor de crédito:",
                value=int(current_value),
            )
            if ok:
                item.setText(str(new_value))
                self.update_database("conta_credito", new_value)

    def update_database(self, field_name, new_value):
        if self.editing_row is not None:
            codigo_empresa = self.combo_empresas.currentText().split(" - ")[0]
            descricao = self.table_widget.item(self.editing_row, 0).text()
            try:
                connection = conectar_banco()
                cursor = connection.cursor()
                update_query = f"UPDATE conciliacao_{codigo_empresa} SET {field_name} = %s WHERE descricao = %s"
                cursor.execute(update_query, (new_value, descricao))
                connection.commit()
                cursor.close()
                connection.close()
            except Exception as e:
                error_message = MyErrorMessage()
                error_message.showMessage("Erro ao alterar conciliação " + str(e))
                error_message.exec_()
                return False
            self.editing_row = None


def main():
    app = QApplication(sys.argv)
    window = ConciliacoesWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
