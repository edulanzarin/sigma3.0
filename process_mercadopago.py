import re
import pandas as pd
from decimal import Decimal
import PyPDF2
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QFileDialog


def process_mercadopago(dados_pdf):
    data_list = []
    descricao_list = []
    valor_list = []
    deb_cred_list = []
    data_anterior = None
    descricao_anterior = None
    entry_started = False  # Adicionei uma variável para controlar o início da entrada

    for pagina_num, pagina in enumerate(dados_pdf.pages, 1):
        texto_pagina = pagina.extract_text()
        linhas = texto_pagina.split("\n")

        if pagina_num == 1:
            linhas_a_pular = 7
        else:
            linhas_a_pular = 0  # Alterei para 0 para não pular linhas nas outras páginas

        stop_process = False

        for linha_num, linha in enumerate(linhas, 1):
            partes = linha.split(" ")

            if "Data de geração" in linha:
                stop_process = True
                break

            if (
                len(partes) >= 5
                and "ID da operação" not in linha
            ):
                if linhas_a_pular > 0:
                    linhas_a_pular -= 1
                    continue

                if "-" in partes[0]:
                    match = re.match(r"(\d{2}-\d{2}-\d{4})(.*)", partes[0])
                    if match:
                        data = match.group(1)
                        data = datetime.strptime(data, "%d-%m-%Y").strftime("%d/%m/%Y")
                        texto_grudado = match.group(2)
                    if "," in partes[-3]:
                        descricao = texto_grudado + " " + " ".join(partes[1:-5])
                        deb_cred = "CRED" if "-" in partes[-3] else "DEB"
                        valor_str = re.sub(r"[a-zA-Z]", "", partes[-3])
                        valor_replace = valor_str.replace(".", "").replace(",", ".").replace("-", "")
                        valor = Decimal(valor_replace)
                        entry_started = True
                    else:
                        data_anterior = match.group(1)
                        data_anterior = datetime.strptime(data_anterior, "%d-%m-%Y").strftime("%d/%m/%Y")
                        descricao_anterior = texto_grudado + " " + " ".join(partes[1:])
                        entry_started = True
                        continue

                else:
                    if "," in partes[-3]:
                        data = data_anterior
                        descricao = "".join(descricao_anterior)
                        deb_cred = "CRED" if "-" in partes[-3] else "DEB"
                        valor_str = re.sub(r"[a-zA-Z]", "", partes[-3])
                        valor_replace = valor_str.replace(".", "").replace(",", ".").replace("-", "")
                        valor = Decimal(valor_replace)
                        entry_started = True
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
            "DEB": [1 if dc == "DEB" else None for dc in deb_cred_list],
            "CRED": [1 if dc == "CRED" else None for dc in deb_cred_list],
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
        df = process_mercadopago(pdf_reader)  # Processa o PDF

        if not df.empty:
            # Solicita ao usuário que selecione onde salvar o arquivo Excel
            file_dialog.setFileMode(QFileDialog.AnyFile)
            file_dialog.setNameFilter("Arquivos Excel (*.xlsx);;Todos os arquivos (*)")  # Correção aqui
            if file_dialog.exec_():
                excel_file_path = file_dialog.selectedFiles()[0]

                # Salva o DataFrame como arquivo Excel especificando o mecanismo "openpyxl"
                df.to_excel(excel_file_path, engine="openpyxl", index=False)

                print(f"DataFrame salvo em {excel_file_path}")


if __name__ == "__main__":
    main()
