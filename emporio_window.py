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


class EmporioWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.title_label = QLabel("Empório Astral")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            "QLabel {"
            "font-size: 15px; font-family: Arial; font: bold; min-height: 40px;"
            "}"
        )

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
        self.carregar_button = self.create_carregar_button(
            "", self.carregar_button_clicked
        )
        self.carregar_button.setEnabled(False)

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
        self.process_button.setEnabled(False)

        self.save_button = self.create_button("Salvar", self.save_button_clicked)
        self.save_button.setEnabled(False)

        self.init_layout()

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
        layout.addWidget(self.save_button)
        layout.addStretch(1)
        return layout

    def init_layout(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        main_layout.addWidget(self.title_label)
        main_layout.addLayout(
            self.create_pagamentos_layout(
                "relatorio.png", self.relatorio_label, self.carregar_button
            )
        )

        main_layout.addLayout(self.create_button_layout())
        main_layout.addWidget(self.table_widget)

        self.setLayout(main_layout)

    def choose_relatorio(self, event):
        pass

    def carregar_button_clicked(self):
        pass

    def process_button_clicked(self):
        pass

    def save_button_clicked(self):
        pass


def main():
    app = QApplication(sys.argv)
    window = EmporioWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
