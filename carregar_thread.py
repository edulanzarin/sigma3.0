from PyQt5.QtCore import QThread, pyqtSignal
import pandas as pd
import os
from datetime import datetime
from decimal import Decimal
import PyPDF2
from mysql.connector import connect, Error

from comprovante_sicoob import comprovante_sicoob
from error_window import MyErrorMessage
from connect_database import conectar_banco

class CarregarThread(QThread):
    finished = pyqtSignal(str)  

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path

    def run(self):
        try:
                conn = conectar_banco()
                cursor = conn.cursor()
                cursor.execute("TRUNCATE TABLE comprovantes")

                for file_name in os.listdir(self.folder_path):
                    if file_name.endswith(".pdf"):
                        pdf_path = os.path.join(self.folder_path, file_name)
                        pdf_reader = PyPDF2.PdfReader(open(pdf_path, "rb"))
                        df = comprovante_sicoob(pdf_reader)
                        for _, row in df.iterrows():
                            data = datetime.strptime(row["DATA"], "%d/%m/%Y").date()
                            descricao = str(row["DESCRICAO"])
                            valor = Decimal(row["VALOR"])
                            desconto = Decimal(row["DESCONTO"]) if not pd.isna(row["DESCONTO"]) else None
                            juros = Decimal(row["JUROS"]) if not pd.isna(row["JUROS"]) else None

                            insert_query = """
                            INSERT INTO comprovantes (data, descricao, valor, desconto, juros)
                            VALUES (%s, %s, %s, %s, %s)
                            """
                            cursor.execute(
                                insert_query,
                                (
                                    data,
                                    descricao,
                                    valor,
                                    desconto,
                                    juros,
                                ),
                            )

                        conn.commit()
                        self.finished.emit("Dados carregados com sucesso!")

        except Error as e:
            error_message = MyErrorMessage()
            error_message.showMessage("Erro ao carregar pagamentos: " + str(e))
            error_message.exec_()
            self.finished.emit("Erro ao carregar pagamentos: " + str(e))