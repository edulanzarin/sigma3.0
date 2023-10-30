from PyQt5.QtCore import QThread, pyqtSignal
import pandas as pd
import os
import PyPDF2
from datetime import datetime
from decimal import Decimal

from process_sicredi import process_sicredi
from process_cresol import process_cresol
from process_sicoob import process_sicoob
from process_viacredi import process_viacredi
from process_safra import process_safra
from connect_database import conectar_banco
from error_window import MyErrorMessage


class ProcessarThread(QThread):
    pdf_processed = pyqtSignal(pd.DataFrame)

    def __init__(self, extrato_file_path, selected_banco):
        super(ProcessarThread, self).__init__()
        self.extrato_file_path = extrato_file_path
        self.selected_banco = selected_banco

        pdf_path = os.path.join(self.extrato_file_path)
        self.dados_pdf = PyPDF2.PdfReader(open(pdf_path, "rb"))
        self.extrato_df = None

    def run(self):
        extrato_df = pd.DataFrame()
        if self.selected_banco == "37":
            extrato_df = process_viacredi(self.dados_pdf)
        elif self.selected_banco == "23":
            extrato_df = process_sicredi(self.dados_pdf)
        elif self.selected_banco == "14":
            extrato_df = process_safra(self.dados_pdf)
        elif self.selected_banco == "35":
            extrato_df = process_cresol(self.dados_pdf)
        elif self.selected_banco == "30":
            extrato_df = process_sicoob(self.dados_pdf)

        if extrato_df is not None:
            try:
                conn = conectar_banco()
                cursor = conn.cursor()
                cursor.execute("TRUNCATE TABLE transacoes")

                for _, row in extrato_df.iterrows():
                    data_transacao = datetime.strptime(row["DATA"], "%d/%m/%Y").date()
                    debito = int(row["DEB"]) if not pd.isna(row["DEB"]) else None
                    credito = int(row["CRED"]) if not pd.isna(row["CRED"]) else None
                    valor = Decimal(row["VALOR"])
                    descricao = str(row["DESCRICAO"])

                    insert_query = """
                    INSERT INTO transacoes (data_transacao, debito, credito, valor, descricao)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(
                        insert_query,
                        (
                            data_transacao,
                            debito,
                            credito,
                            valor,
                            descricao,
                        ),
                    )

                if self.selected_banco == "30":
                    update_query = """
                    UPDATE transacoes AS t
                    JOIN comprovantes AS c
                    ON t.data_transacao = c.data AND t.valor = c.valor
                    SET t.descricao = c.descricao
                    """
                    cursor.execute(update_query)

                conn.commit()
                conn.close()

                self.pdf_processed.emit(extrato_df)
            except Exception as e:
                error_message = MyErrorMessage()
                error_message.showMessage("Erro ao processar extrato " + str(e))
                error_message.exec_()
