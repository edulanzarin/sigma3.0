from PyQt5.QtCore import QThread, pyqtSignal
from connect_database import conectar_banco
from error_window import MyErrorMessage


class EmpresaSQLThread(QThread):
    empresa_ready = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def execute_query_empresa(self, query):
        try:
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            self.empresa_ready.emit(data)
            cursor.close()
            conn.close()
        except Exception as e:
            error_message = MyErrorMessage()
            error_message.showMessage("Erro ao carregar empresas. " + str(e))
            error_message.exec_()
