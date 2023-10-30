import re
import pandas as pd
from decimal import Decimal
import re
import pandas as pd
import PyPDF2
from PyQt5.QtWidgets import QApplication, QFileDialog


def process_sicoob(dados_pdf):
    data_list = []
    descricao_list = []
    valor_list = []
    deb_cred_list = []
    data_anterior = None
    descricao_anterior = None

    for pagina_num, pagina in enumerate(dados_pdf.pages, 1):
        texto_pagina = pagina.extract_text()
        linhas = texto_pagina.split("\n")

        if pagina_num == 1:
            linhas_a_pular = 6
        else:
            linhas_a_pular = 0

        stop_process = False

        for linha_num, linha in enumerate(linhas, 1):
            partes = linha.split(" ")
            if (
                len(partes) >= 1
                and "SALDO ANTERIOR" not in linha
                and "BLOQUEADO" not in linha
                and "Acesse" not in linha
                and "SALDO DO DIA" not in linha
                and "*" not in linha
            ):
                if "(+)" in linha or "(-)" in linha:
                    stop_process = True
                    break

                if linha_num <= linhas_a_pular:
                    continue

                if "/" in partes[0]:
                    if "," in partes[-1]:
                        data = partes[0]
                        descricao = " ".join(partes[2:-1])
                        deb_cred = "CRED" if "D" in partes[-1] else "DEB"
                        valor_str = re.sub(r"[a-zA-Z]", "", partes[-1])
                        valor_replace = valor_str.replace(".", "").replace(",", ".")
                        valor = Decimal(valor_replace)
                        entry_started = True
                    else:
                        data_anterior = partes[0]
                        descricao_anterior = " ".join(partes[1:])
                        entry_started = True
                        continue

                else:
                    if "," in partes[-1]:
                        data = data_anterior
                        descricao = "".join(descricao_anterior)
                        deb_cred = "CRED" if "D" in partes[-1] else "DEB"
                        valor_str = re.sub(r"[a-zA-Z]", "", partes[-1])
                        valor_replace = valor_str.replace(".", "").replace(",", ".")
                        valor = Decimal(valor_replace)
                        valor = valor_str.replace(".", "").replace(",", ".")
                    else:
                        continue

                if entry_started:
                    data_list.append(data)
                    descricao_list.append(descricao)
                    valor_list.append(valor)
                    deb_cred_list.append(deb_cred)
                    entry_started = False

            if stop_process:
                break

        if stop_process:
            break

    df = pd.DataFrame(
        {
            "DATA": data_list,
            "DEB": [30 if dc == "DEB" else None for dc in deb_cred_list],
            "CRED": [30 if dc == "CRED" else None for dc in deb_cred_list],
            "VALOR": valor_list,
            "DESCRICAO": descricao_list,
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
        df = process_sicoob(pdf_reader)  # Processa o PDF

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
