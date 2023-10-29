from PyQt5.QtCore import QThread, pyqtSignal
import pandas as pd
import os
import PyPDF2

from comprovante_sicoob import comprovante_sicoob
from error_window import MyErrorMessage


class CarregarThread(QThread):
    finished = pyqtSignal(pd.DataFrame)

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path

    def run(self):
        combined_df = pd.DataFrame()

        try:
            for file_name in os.listdir(self.folder_path):
                if file_name.endswith(".pdf"):
                    pdf_path = os.path.join(self.folder_path, file_name)
                    pdf_reader = PyPDF2.PdfReader(open(pdf_path, "rb"))
                    df = comprovante_sicoob(pdf_reader)
                    combined_df = pd.concat([combined_df, df], ignore_index=True)

            self.finished.emit(combined_df)
        except Exception as e:
            error_message = MyErrorMessage()
            error_message.showMessage("Erro ao carregar pagamentos " + str(e))
            error_message.exec_()
