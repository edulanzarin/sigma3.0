import pandas as pd
from decimal import Decimal
import re
import pandas as pd
import PyPDF2
from PyQt5.QtWidgets import QApplication, QFileDialog


def comprovante_sicoob(dados_pdf):
    data_list = []
    descricao_list = []
    valor_list = []
    desconto_list = []
    juros_list = []

    for pagina_num, pagina in enumerate(dados_pdf.pages, 1):
        texto_pagina = pagina.extract_text()
        linhas = texto_pagina.split("\n")

        for linha in linhas:
            partes = linha.split(" ")

            if "Data Pagamento:" in linha:
                data = partes[-1]
            if "Nome Fantasia Beneficiário:" in linha:
                descricao = " ".join(partes[4:])
            if "Valor Documento:" in linha:
                valor_str = partes[-1]
                valor_replace = valor_str.replace(".", "").replace(",", ".")
                valor = Decimal(valor_replace)
            if "(-)" in linha:
                desconto_str = partes[-1]
                desconto = desconto_str.replace(".", "").replace(",", ".")
            if "(+)" in linha:
                juros_str = partes[-1]
                juros = juros_str.replace(".", "").replace(",", ".")
                if data is not None and descricao is not None and valor is not None:
                    data_list.append(data)
                    descricao_list.append(descricao)
                    valor_list.append(valor)
                    desconto_list.append(desconto)
                    juros_list.append(juros)

    df = pd.DataFrame(
        {
            "DATA": data_list,
            "DESCRICAO": descricao_list,
            "VALOR": valor_list,
            "DESCONTO": desconto_list,
            "JUROS": juros_list,
        }
    )

    return df


def main():
    app = QApplication([])  # Inicializa a aplicação Qt

    # Solicita ao usuário que selecione um arquivo PDF
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    file_dialog.setNameFilter("Arquivos PDF (*.pdf)")

    if file_dialog.exec_():
        pdf_file_path = file_dialog.selectedFiles()[0]

        # Lê o arquivo PDF
        pdf_reader = PyPDF2.PdfReader(open(pdf_file_path, "rb"))
        df = comprovante_sicoob(pdf_reader)  # Processa o PDF

        if not df.empty:
            # Solicita ao usuário que selecione onde salvar o arquivo Excel
            file_dialog.setFileMode(QFileDialog.AnyFile)
            file_dialog.setNameFilter("Arquivos Excel (*.xlsx)")
            if file_dialog.exec_():
                excel_file_path = file_dialog.selectedFiles()[0]

                # Salva o DataFrame como arquivo Excel especificando o mecanismo "openpyxl"
                df.to_excel(excel_file_path, engine="openpyxl", index=False)

                print(f"DataFrame salvo em {excel_file_path}")


if __name__ == "__main__":
    main()
