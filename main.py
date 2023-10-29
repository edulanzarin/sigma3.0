import sys
from PyQt5.QtWidgets import QApplication
from open_window import OpenWindow
from main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    main_window = None

    def on_login_success(id_usuario):
        nonlocal main_window
        main_window = MainWindow(id_usuario)
        open_window.close()
        main_window.show()

    open_window = OpenWindow()
    open_window.login_success.connect(on_login_success)
    open_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
