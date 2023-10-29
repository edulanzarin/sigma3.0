import pandas as pd
import re
from datetime import datetime
from decimal import Decimal
import re
import pandas as pd
import PyPDF2
from PyQt5.QtWidgets import QApplication, QFileDialog


def process_safra(dados_pdf):
    data_list = []
    descricao_list = []
    valor_list = []
    deb_cred_list = []

    ano_atual = datetime.now().year

    for pagina_num, pagina in enumerate(dados_pdf.pages):
        linhas = pagina.extract_text().split("\n")
        if pagina_num == 0:
            start_line = 8
        else:
            start_line = 2
        last_date = ""
        descricao_anterior = ""
        linhas_puladas = 0
        for i, linha in enumerate(linhas[start_line:]):
            if "Banco Safra S/A" in linha:
                linhas_puladas = 10
                continue
            if linhas_puladas > 0:
                linhas_puladas -= 1
                continue
            if "SALDO" not in linha:
                partes = linha.split()
                if len(partes) >= 3:
                    if "/" in partes[0]:
                        if any(char.isdigit() for char in partes[-1]):
                            deb_cred = "CRED" if "-" in partes[-1] else "DEB"
                            valor_str = (
                                partes[-1]
                                .replace("-", "")
                                .replace(".", "")
                                .replace(",", ".")
                            )
                            valor = Decimal(valor_str)
                            data = re.sub(r"[^0-9/]", "", partes[0])
                            data += f"/{ano_atual}"
                            data = datetime.strptime(data, "%d/%m/%Y").date()
                            descricao = " ".join(partes[1:-2])
                            last_date = data
                        else:
                            descricao_anterior = partes[1:-2]
                            continue
                    else:
                        deb_cred = "CRED" if "-" in partes[-1] else "DEB"
                        valor_str = (
                            partes[-1]
                            .replace("-", "")
                            .replace(".", "")
                            .replace(",", ".")
                        )
                        valor = Decimal(valor_str)
                        descricao = (
                            " ".join(descricao_anterior) + " " + " ".join(partes[0:-2])
                        )
                        data = last_date

                    data_list.append(data)
                    descricao_list.append(descricao)
                    valor_list.append(valor)
                    deb_cred_list.append(deb_cred)

    df = pd.DataFrame(
        {
            "DATA": data_list,
            "DEB": [14 if dc == "DEB" else None for dc in deb_cred_list],
            "CRED": [14 if dc == "CRED" else None for dc in deb_cred_list],
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
        df = process_safra(pdf_reader)  # Processa o PDF

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
