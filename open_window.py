import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QLineEdit,
)
from PyQt5.QtGui import QPixmap, QIcon, QKeySequence
from PyQt5.QtCore import Qt, pyqtSignal
from register_window import RegisterWindow
from login_function import (
    verificar_credenciais,
    registrar_login,
)
from empresas_window import EmpresasWindow


class OpenWindow(QWidget):
    login_success = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        icon = QIcon(r".\assets\icon.ico")
        self.setWindowIcon(icon)
        self.setWindowTitle("Sigma")
        self.setFixedSize(800, 500)
        self.register_window = None
        self.login_window = None
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

        main_layout = QHBoxLayout()

        left_container = QVBoxLayout()

        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(r".\assets\sigmastart.png"))
        icon_label.setAlignment(Qt.AlignCenter)
        sigma_label = QLabel("Sigma")
        sigma_label.setStyleSheet("QLabel {font-size: 20px; font: bold;}")
        sigma_label.setAlignment(Qt.AlignCenter)

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

        enter_shortcut = QKeySequence(Qt.Key_Return)
        self.button_login.setShortcut(enter_shortcut)

        register_button = QPushButton("Cadastrar novo usuário")
        register_button.setCursor(Qt.PointingHandCursor)
        register_button.setStyleSheet(
            "QPushButton { min-height: 20px; font-size: 12px; font: bold; min-width: 250px; max-width: 2500px;}"
        )
        register_button.clicked.connect(self.open_register_window)

        left_container.addWidget(icon_label, alignment=Qt.AlignTop)
        left_container.addWidget(sigma_label, alignment=Qt.AlignTop)
        left_container.addSpacerItem(
            QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        left_container.addLayout(layout)
        left_container.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        left_container.addWidget(register_button)
        left_container.addSpacerItem(
            QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        right_container = QHBoxLayout()

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer2 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        right_container.addSpacerItem(spacer)

        image_label = QLabel()
        image_label.setPixmap(QPixmap(r".\assets\contador.png"))
        right_container.addWidget(image_label)
        right_container.setAlignment(Qt.AlignVCenter)

        main_layout.addSpacerItem(spacer2)
        main_layout.addLayout(left_container)
        main_layout.addSpacerItem(spacer2)
        main_layout.addLayout(right_container)

        self.setLayout(main_layout)

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

    def open_register_window(self):
        if not self.register_window:
            self.register_window = RegisterWindow()
        self.register_window.show()


def main():
    app = QApplication(sys.argv)
    window = OpenWindow()
    window.show()
    empresas_window = EmpresasWindow()
    window.login_success.connect(empresas_window.show_empresas_window)
    window.login_success.connect(empresas_window.load_user_id)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
