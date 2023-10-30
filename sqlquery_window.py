import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QListWidget,
    QMessageBox,
    QInputDialog,
    QSizePolicy,
    QLabel,
)
from PyQt5.QtCore import Qt, pyqtSlot, QSize
from PyQt5.QtGui import QIcon, QKeyEvent

from connect_database import conectar_banco
from error_window import MyErrorMessage


class SqlQueryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        self.check_password_button = QPushButton("", self)
        self.check_password_button.setIcon(QIcon(r".\assets\lock.png"))
        self.check_password_button.setIconSize(QSize(22, 22))
        self.check_password_button.setStyleSheet(
            "QPushButton { max-width: 18px; max-height: 18px; font-size: 10px; border: none; color: #333333;}"
        )
        self.check_password_button.setCursor(Qt.PointingHandCursor)
        self.check_password_button.clicked.connect(self.check_password)
        main_layout.addWidget(self.check_password_button, alignment=Qt.AlignHCenter)

        horizont_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        title_layout = QHBoxLayout()

        fetch_label = QLabel("Fetch")
        fetch_label.setStyleSheet("color: #333333; font: bold; font-size: 12px;")
        self.sql_input_fetch = MyLineEdit(self)
        self.sql_input_fetch.setStyleSheet(
            "border-radius: 3px; border: 1px solid silver; color: #333333; font: bold; font-size: 12px;"
        )
        self.sql_input_fetch.setAlignment(Qt.AlignTop)
        self.sql_input_fetch.setEnabled(False)
        self.sql_input_fetch.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        commit_label = QLabel("Commit")
        commit_label.setStyleSheet("color: #333333; font: bold; font-size: 12px;")
        self.sql_input_commit = MyLineEdit(self)
        self.sql_input_commit.setStyleSheet(
            "border-radius: 3px; border: 1px solid silver; color: #333333; font: bold; font-size: 12px;"
        )
        self.sql_input_commit.setAlignment(Qt.AlignTop)
        self.sql_input_commit.setEnabled(False)
        self.sql_input_commit.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )

        input_layout.addWidget(self.sql_input_fetch)
        input_layout.addWidget(self.sql_input_commit)

        title_layout.addWidget(fetch_label, alignment=Qt.AlignHCenter)
        title_layout.addWidget(commit_label, alignment=Qt.AlignHCenter)
        horizont_layout.addLayout(input_layout)

        main_layout.addLayout(title_layout)
        main_layout.addLayout(horizont_layout)

        result_label = QLabel("Result")
        result_label.setStyleSheet("color: #333333; font: bold; font-size: 12px;")
        main_layout.addWidget(result_label, alignment=Qt.AlignHCenter)

        self.result_display = QListWidget(self)
        self.result_display.setStyleSheet(
            "border-radius: 3px; border: 1px solid silver; color: #333333; font: bold; font-size: 12px; font-family: Consolas"
        )
        main_layout.addWidget(self.result_display)

        self.setLayout(main_layout)

        self.sql_input_fetch.returnPressed.connect(self.execute_query_fetch)
        self.sql_input_commit.returnPressed.connect(self.execute_query_commit)

    def check_password(self):
        password, ok = QInputDialog.getText(
            self, "Acesso", "Insira a senha:", QLineEdit.Password
        )

        if ok and password == "dudu@007":
            self.sql_input_fetch.setEnabled(True)
            self.sql_input_commit.setEnabled(True)
        else:
            QMessageBox.warning(
                self,
                "Senha Incorreta",
                "A senha inserida está incorreta.",
                QMessageBox.Ok,
            )

    @pyqtSlot()
    def execute_query_fetch(self):
        query = self.sql_input_fetch.text()
        if query:
            try:
                conn = conectar_banco()
                cursor = conn.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                conn.close()

                self.result_display.clear()
                for result in results:
                    self.result_display.addItem(str(result))
            except Exception as e:
                error_message = MyErrorMessage()
                error_message.showMessage("Erro ao processar query " + str(e))
                error_message.exec_()

    @pyqtSlot()
    def execute_query_commit(self):
        query = self.sql_input_commit.text()
        if query:
            try:
                conn = conectar_banco()
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                conn.close()

                self.sql_input_commit.clear()
                QMessageBox.information(
                    self, "Sucesso", "Comando executado e comitado com sucesso."
                )
            except Exception as e:
                error_message = MyErrorMessage()
                error_message.showMessage("Erro ao processar query " + str(e))
                error_message.exec_()


class MyLineEdit(QLineEdit):
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return and event.modifiers() & Qt.ShiftModifier:
            cursor_position = self.cursorPosition()
            text = self.text()
            text = text[:cursor_position] + "\n" + text[cursor_position:]
            self.setText(text)
        else:
            super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)
    window = SqlQueryWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
