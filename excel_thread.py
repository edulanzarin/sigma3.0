from PyQt5.QtCore import QThread, pyqtSignal
import pandas as pd
from connect_database import conectar_banco


class ExcelProcessingThread(QThread):
    data_ready = pyqtSignal(bool)

    def __init__(self, file_path, codigo_empresa):
        super().__init__()
        self.file_path = file_path
        self.codigo_empresa = codigo_empresa

    def run(self):
        try:
            df = pd.read_excel(self.file_path)
            df = df.rename(
                columns={
                    "DESCRICAO": "descricao",
                    "DEBITO": "conta_debito",
                    "CREDITO": "conta_credito",
                }
            )
            connection = conectar_banco()
            cursor = connection.cursor()

            for index, row in df.iterrows():
                descricao = row["descricao"]
                debito = row["conta_debito"]
                credito = row["conta_credito"]

                insert_query = f"INSERT INTO conciliacao_{self.codigo_empresa} (descricao, conta_debito, conta_credito) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (descricao, debito, credito))

            connection.commit()
            cursor.close()
            connection.close()

            self.data_ready.emit(True)
        except Exception as e:
            print(f"Erro ao processar o Excel: {e}")
            self.data_ready.emit(False)
