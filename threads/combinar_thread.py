import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal


class CombinarThread(QThread):
    combined_data = pyqtSignal(pd.DataFrame)

    def __init__(self, extrato_df, combined_df):
        super(CombinarThread, self).__init__()
        self.extrato_df = extrato_df
        self.combined_df = combined_df

    def run(self):
        self.combined_data.emit(self.extrato_df)
