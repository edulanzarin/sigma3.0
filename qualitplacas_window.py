import sys
import pandas as pd
<<<<<<< HEAD
from unidecode import unidecode
from datetime import date
=======
>>>>>>> 1c51f4b6d017f1df829b3efd13b77bfaf1aa5d67
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
<<<<<<< HEAD
    QInputDialog,
    QMessageBox,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QSize

from process_qualitplacas import process_qualitplacas
from processing_window import ProcessingWindow
from relatorio_qualit import RelatorioQualit


class QualitplacasWindow(QWidget):
    carregamento_finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.relatorio_file_path = ""
        self.relatorio_qualit = None

        self.title_label = QLabel("Qualitplacas")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            "QLabel {"
            "font-size: 15px; font-family: Arial; font: bold; min-height: 40px;"
            "}"
        )

=======
    QDialog,
    QInputDialog,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from processing_window import ProcessingWindow
from error_window import MyErrorMessage
from connect_database import conectar_banco


class QualitPlacasWindow(QWidget):
    def __init__(self):
        super().__init__()

>>>>>>> 1c51f4b6d017f1df829b3efd13b77bfaf1aa5d67
        self.relatorio_label = QLabel("Clique para selecionar o relatório")
        self.relatorio_label.setStyleSheet(
            "QLabel {"
            "border: 0.5px solid silver;"
            "border-radius: 1.2px;"
            "padding: 2.6px;"
            "font-size: 11px;"
            "}"
        )
        self.relatorio_label.setCursor(Qt.PointingHandCursor)
        self.relatorio_label.setOpenExternalLinks(False)
        self.relatorio_label.mousePressEvent = self.choose_relatorio
<<<<<<< HEAD
        self.is_relatorio = False
        self.carregar_button = self.create_carregar_button(
            "", self.carregar_button_clicked
        )
        self.carregar_button.setEnabled(self.is_relatorio)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(6)
        self.table_widget.setColumnHidden(0, True)
        self.table_widget.setHorizontalHeaderLabels(
            ["Data", "Débito", "Crédito", "Valor", "Descrição"]
=======

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(
            ["Data", "Conta Débito", "Conta Crédito"]
>>>>>>> 1c51f4b6d017f1df829b3efd13b77bfaf1aa5d67
        )
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

<<<<<<< HEAD
        self.process_button = self.create_button(
            "Processar", self.process_button_clicked
        )
        self.process_button.setEnabled(self.is_relatorio)
=======
        self.process_button = self.create_button("Processar", self.process_button_clicked)
>>>>>>> 1c51f4b6d017f1df829b3efd13b77bfaf1aa5d67

        self.save_button = self.create_button("Salvar", self.save_button_clicked)
        self.save_button.setEnabled(False)

        self.init_layout()

    def create_button(self, text, on_click):
        button = QPushButton(text)
        button.setStyleSheet("QPushButton { max-width: 80px; font-size: 12px;}")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(on_click)
        return button

<<<<<<< HEAD
    def create_relatorio_layout(self, icon_name, widget, button):
=======
    def create_icon_layout(self, icon_name, widget):
>>>>>>> 1c51f4b6d017f1df829b3efd13b77bfaf1aa5d67
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
<<<<<<< HEAD
        layout.addWidget(button)
=======
>>>>>>> 1c51f4b6d017f1df829b3efd13b77bfaf1aa5d67
        return layout

    def create_button_layout(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addStretch(1)
        layout.addWidget(self.process_button)
        layout.addWidget(self.save_button)
        layout.addStretch(1)
        return layout

<<<<<<< HEAD
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

=======
>>>>>>> 1c51f4b6d017f1df829b3efd13b77bfaf1aa5d67
    def init_layout(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

<<<<<<< HEAD
        main_layout.addWidget(self.title_label)
        main_layout.addLayout(
            self.create_relatorio_layout(
                "relatorio.png", self.relatorio_label, self.carregar_button
            )
=======
        main_layout.addLayout(
            self.create_icon_layout("payments.png", self.relatorio_label)
>>>>>>> 1c51f4b6d017f1df829b3efd13b77bfaf1aa5d67
        )

        main_layout.addLayout(self.create_button_layout())
        main_layout.addWidget(self.table_widget)

        self.setLayout(main_layout)

    def choose_relatorio(self, event):
<<<<<<< HEAD
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Escolher o relatório em PDF",
            "",
            "Arquivos PDF (*.pdf);;Todos os Arquivos (*)",
            options=options,
        )
        if file_name:
            self.relatorio_file_path = file_name
            self.relatorio_label.setText(file_name)
            self.is_relatorio = True
        else:
            self.is_relatorio = False
        self.carregar_button.setEnabled(self.is_relatorio)
=======
        pass
>>>>>>> 1c51f4b6d017f1df829b3efd13b77bfaf1aa5d67

    def process_button_clicked(self):
        pass

<<<<<<< HEAD
    def carregar_button_clicked(self):
        if self.relatorio_file_path:
            self.carregar_button.setEnabled(False)
            self.processing_window = ProcessingWindow(self)
            self.processing_window.show()
            self.relatorio_qualit = RelatorioQualit(self.relatorio_file_path)
            self.relatorio_qualit.finished.connect(self.relatorio_qualit_finished)
            self.relatorio_qualit.finished.connect(self.processing_window.close)
            self.relatorio_qualit.finished.connect(
                lambda: self.relatorio_label.setText("Relatório carregado")
            )
            self.relatorio_qualit.start()

    def relatorio_qualit_finished(self):
        self.carregamento_finished.emit()

    def save_button_clicked(self):
        pass


def main():
    app = QApplication(sys.argv)
    window = QualitplacasWindow()
=======
    def save_button_clicked(self):
        pass

def main():
    app = QApplication(sys.argv)
    window = QualitPlacasWindow()
>>>>>>> 1c51f4b6d017f1df829b3efd13b77bfaf1aa5d67
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
