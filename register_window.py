import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from functions.register_function import cadastrar_usuario


class RegisterWindow(QWidget):
    register_success = pyqtSignal()

    def __init__(self):
        super().__init__()

        icon = QIcon(r".\assets\register.png")
        self.setWindowIcon(icon)
        self.setWindowTitle("Cadastro")
        self.setGeometry(100, 100, 300, 250)

        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

        layout = QVBoxLayout()

        self.label_user = QLabel("Usuário:")
        self.text_user = QLineEdit()

        self.label_password = QLabel("Senha:")
        self.text_password = QLineEdit()
        self.text_password.setEchoMode(QLineEdit.Password)

        self.button_register = QPushButton("Cadastrar")
        self.button_register.clicked.connect(self.register)

        self.message_label = QLabel("")

        layout.addWidget(self.label_user)
        layout.addWidget(self.text_user)
        layout.addWidget(self.label_password)
        layout.addWidget(self.text_password)
        layout.addWidget(self.button_register)
        layout.addWidget(self.message_label)

        self.setLayout(layout)

        enter_shortcut = QKeySequence(Qt.Key_Return)
        self.button_register.setShortcut(enter_shortcut)

    def register(self):
        user = self.text_user.text()
        password = self.text_password.text()

        if cadastrar_usuario(user, password):
            self.message_label.setText("Cadastro bem-sucedido")
            self.register_success.emit()
        else:
            self.message_label.setText("Erro ao cadastrar")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec_())
