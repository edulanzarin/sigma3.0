from PyQt5.QtCore import QThread, pyqtSignal
from ..functions.connect_database import conectar_banco
from ..error_window import MyErrorMessage


class BancoSQLThread(QThread):
    banco_ready = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def execute_query_banco(self, query):
        try:
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            self.banco_ready.emit(data)
            cursor.close()
            conn.close()
        except Exception as e:
            error_message = MyErrorMessage()
            error_message.showMessage("Erro ao carregar bancos. " + str(e))
            error_message.exec_()
