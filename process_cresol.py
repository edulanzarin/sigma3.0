import re
import pandas as pd
from decimal import Decimal


def process_cresol(dados_pdf):
    data_list = []
    descricao_list = []
    valor_list = []
    deb_cred_list = []
    stop_process = False

    for pagina_num, pagina in enumerate(dados_pdf.pages, 1):
        texto_pagina = pagina.extract_text()
        linhas = texto_pagina.split("\n")

        if pagina_num == 1:
            linhas_a_pular = 24
        else:
            linhas_a_pular = 6

        for linha_num, linha in enumerate(linhas, 1):
            partes = linha.split(" ")

            if "(=)" in linha or "(+)" in linha or "(-)" in linha:
                stop_process = True
                break

            if (
                len(partes) >= 5
                and "SALDO ANTERIOR" not in linha
                and "página" not in linha
            ):
                if linha_num <= linhas_a_pular:
                    continue

                valores_monetarios = re.findall(
                    r"\b\d{1,3}(?:\.\d{3})*(?:,\d{2})\b", linha
                )

                for valorr in valores_monetarios:
                    linha = re.sub(r"\b\d{1,3}(?:\.\d{3})*(?:,\d{2})\b", "", linha)

                partes = linha.split(" ", 1)

                data = partes[0]
                descricao = partes[1]

                deb_cred = "CRED" if " D " in descricao else "DEB"
                valor_str = re.sub(r"[a-zA-Z]", "", valorr)
                valor_replace = valor_str.replace(".", "").replace(",", ".")
                valor = Decimal(valor_replace)

                data_list.append(data)
                descricao_list.append(descricao)
                valor_list.append(valor)
                deb_cred_list.append(deb_cred)

            if stop_process:
                break

    df = pd.DataFrame(
        {
            "DATA": data_list,
            "DEB": [35 if dc == "DEB" else None for dc in deb_cred_list],
            "CRED": [35 if dc == "CRED" else None for dc in deb_cred_list],
            "VALOR": valor_list,
            "DESCRICAO": descricao_list,
        }
    )
    return df
