from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QIcon


class CadastrarDialog(QDialog):
    def __init__(self):
        super().__init__()

        icon = QIcon(r".\assets\cadastro.ico")
        self.setWindowIcon(icon)
        self.setWindowTitle("Sigma")
        self.setWindowTitle("Cadastrar Conciliações")
        self.setFixedSize(300, 250)

        layout = QVBoxLayout()

        self.descricao_label = QLabel("Descrição:")
        self.descricao_input = QLineEdit()

        self.debito_label = QLabel("Débito:")
        self.debito_input = QLineEdit()

        self.credito_label = QLabel("Crédito:")
        self.credito_input = QLineEdit()

        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.accept)
        self.save_button.setEnabled(False)

        layout.addWidget(self.descricao_label)
        layout.addWidget(self.descricao_input)
        layout.addWidget(self.debito_label)
        layout.addWidget(self.debito_input)
        layout.addWidget(self.credito_label)
        layout.addWidget(self.credito_input)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.descricao_input.textChanged.connect(self.check_fields)
        self.debito_input.textChanged.connect(self.check_fields)
        self.credito_input.textChanged.connect(self.check_fields)

    def check_fields(self):
        descricao = self.descricao_input.text()
        debito = self.debito_input.text()
        credito = self.credito_input.text()
        self.save_button.setEnabled(bool(descricao and debito and credito))

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return:
            if self.save_button.isEnabled():
                self.accept()

    def get_input_data(self):
        return (
            self.descricao_input.text(),
            int(self.debito_input.text()),
            int(self.credito_input.text()),
        )
