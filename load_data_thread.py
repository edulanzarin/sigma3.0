from PyQt5.QtCore import QThread, pyqtSignal

from connect_database import conectar_banco
from error_window import MyErrorMessage


class LoadDataThread(QThread):
    data_loaded = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def run(self):
        data = []
        try:
            conn = conectar_banco()
            cursor = conn.cursor()
            query = "SELECT data_transacao, debito, credito, valor, descricao FROM transacoes"
            cursor.execute(query)
            data = cursor.fetchall()
            conn.close()
            self.data_loaded.emit(data)
        except Exception as e:
            error_message = MyErrorMessage()
            error_message.showMessage("Erro ao carregar transações " + str(e))
            error_message.exec_()
