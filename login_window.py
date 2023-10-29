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
from login_function import (
    verificar_credenciais,
    registrar_login,
)
from empresas_window import EmpresasWindow


class LoginWindow(QWidget):
    login_success = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        icon = QIcon(r".\assets\login.png")
        self.setWindowIcon(icon)
        self.setWindowTitle("Login")
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

        self.button_login = QPushButton("Entrar")
        self.button_login.clicked.connect(self.login)

        self.message_label = QLabel("")

        layout.addWidget(self.label_user)
        layout.addWidget(self.text_user)
        layout.addWidget(self.label_password)
        layout.addWidget(self.text_password)
        layout.addWidget(self.button_login)
        layout.addWidget(self.message_label)

        self.setLayout(layout)

        enter_shortcut = QKeySequence(Qt.Key_Return)
        self.button_login.setShortcut(enter_shortcut)

    def login(self):
        user = self.text_user.text()
        password = self.text_password.text()

        id_usuario = verificar_credenciais(user, password)

        if id_usuario:
            self.message_label.setText("Login bem-sucedido")
            self.login_success.emit(id_usuario[0])
            registrar_login(id_usuario[0])
        else:
            self.message_label.setText("Falha no login")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    empresas_window = EmpresasWindow()
    window.login_success.connect(empresas_window.show_empresas_window)
    window.login_success.connect(empresas_window.load_user_id)
    sys.exit(app.exec_())
