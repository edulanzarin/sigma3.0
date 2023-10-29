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
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from register_window import RegisterWindow
from login_window import LoginWindow


class OpenWindow(QWidget):
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

        login_button = QPushButton("Entrar")
        login_button.setCursor(Qt.PointingHandCursor)
        login_button.setStyleSheet(
            "QPushButton { min-height: 20px; font-size: 12px; font: bold; min-width: 120px; max-width: 120px;}"
        )
        login_button.clicked.connect(self.open_login_window)

        register_button = QPushButton("Cadastrar")
        register_button.setCursor(Qt.PointingHandCursor)
        register_button.setStyleSheet(
            "QPushButton { min-height: 20px; font-size: 12px; font: bold; min-width: 120px; max-width: 120px;}"
        )
        register_button.clicked.connect(self.open_register_window)

        left_container.addWidget(icon_label, alignment=Qt.AlignTop)
        left_container.addWidget(sigma_label, alignment=Qt.AlignTop)
        left_container.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        left_container.addWidget(login_button)
        left_container.addWidget(register_button)
        left_container.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        right_container = QHBoxLayout()

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer2 = QSpacerItem(50, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        right_container.addSpacerItem(spacer)

        image_label = QLabel()
        image_label.setPixmap(QPixmap(r".\assets\contador.png"))
        right_container.addWidget(image_label)
        right_container.setAlignment(Qt.AlignVCenter)

        main_layout.addSpacerItem(spacer2)
        main_layout.addLayout(left_container)
        main_layout.addLayout(right_container)

        self.setLayout(main_layout)

    def open_login_window(self):
        if not self.login_window:
            self.login_window = LoginWindow()
        self.login_window.show()

    def open_register_window(self):
        if not self.register_window:
            self.register_window = RegisterWindow()
        self.register_window.show()


def main():
    app = QApplication(sys.argv)
    window = OpenWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
