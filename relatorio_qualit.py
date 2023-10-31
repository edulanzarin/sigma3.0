# pdf_processor.py

from PyQt5.QtCore import pyqtSignal, QObject, QThread
from PyPDF2 import PdfReader
import pandas as pd
import os
import PyPDF2
from datetime import datetime
from decimal import Decimal

from connect_database import conectar_banco
from error_window import MyErrorMessage
from process_qualitplacas import process_qualitplacas


class RelatorioQualit(QThread):
    process_completed = pyqtSignal(pd.DataFrame)

    def __init__(self, file_path):
        super(RelatorioQualit, self).__init__()
        self.file_path = file_path

        pdf_path = os.path.join(self.file_path)
        self.dados_pdf = PyPDF2.PdfReader(open(pdf_path, "rb"))
        self.qualit_df = None

    def run(self):
        qualit_df = process_qualitplacas(self.dados_pdf)
        self.process_completed.emit(qualit_df)

        if qualit_df is not None:
            try:
                conn = conectar_banco()
                cursor = conn.cursor()
                cursor.execute("TRUNCATE TABLE relatorio_qualit")

                for _, row in qualit_df.iterrows():
                    data = datetime.strptime(row["DATA"], "%d/%m/%Y").date()
                    fornecedor = str(row["FORNECEDOR"])
                    nota = str(row["NOTA"])
                    valor = Decimal(row["VALOR"]) if row["VALOR"] is not None else 0
                    desconto = (
                        Decimal(row["DESCONTO"]) if row["DESCONTO"] is not None else 0
                    )
                    insert_query = "INSERT INTO relatorio_qualit (data, fornecedor, nota, valor, desconto) VALUES (%s, %s, %s, %s, %s)"
                    values = (data, fornecedor, nota, valor, desconto)

                    cursor.execute(insert_query, values)

                conn.commit()
                print("Dados inseridos com sucesso!")

            except Exception as e:
                error_message = MyErrorMessage()
                error_message.showMessage("Erro ao processar relatório " + str(e))
                error_message.exec_()

                cursor.close()
                conn.close()
