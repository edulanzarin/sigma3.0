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
from error_window import MyErrorMessage
from connect_database import conectar_banco


class QualitPlacasWindow(QWidget):
    def __init__(self):
        super().__init__()

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

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(
            ["Data", "Conta Débito", "Conta Crédito"]
        )
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.process_button = self.create_button("Processar", self.process_button_clicked)

        self.save_button = self.create_button("Salvar", self.save_button_clicked)
        self.save_button.setEnabled(False)

        self.init_layout()

    def create_button(self, text, on_click):
        button = QPushButton(text)
        button.setStyleSheet("QPushButton { max-width: 80px; font-size: 12px;}")
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

        main_layout.addLayout(
            self.create_icon_layout("payments.png", self.relatorio_label)
        )

        main_layout.addLayout(self.create_button_layout())
        main_layout.addWidget(self.table_widget)

        self.setLayout(main_layout)

    def choose_relatorio(self, event):
        pass

    def process_button_clicked(self):
        pass

    def save_button_clicked(self):
        pass

def main():
    app = QApplication(sys.argv)
    window = QualitPlacasWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
