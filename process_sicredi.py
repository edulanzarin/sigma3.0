import pandas as pd
import re
from decimal import Decimal


def process_sicredi(dados_pdf):
    data_list = []
    descricao_list = []
    valor_list = []
    linhas_imprimir = True
    deb_cred_list = []

    for pagina_num, pagina in enumerate(dados_pdf.pages, 1):
        texto_pagina = pagina.extract_text()
        linhas = texto_pagina.split("\n")

        for linha_num, linha in enumerate(linhas, 1):
            partes = linha.split()
            if len(partes) >= 5:
                if pagina_num == 1 and linha_num < 6:
                    continue
                if "Saldo da conta" in linha:
                    linhas_imprimir = False
                    break

                data = partes[0]
                descricao = " ".join(partes[1:-2])
                deb_cred = "CRED" if "-" in partes[-2] else "DEB"
                valor_str = re.sub(r"[a-zA-Z]", "", partes[-2])
                valor_replace = (
                    valor_str.replace(".", "").replace(",", ".").replace("-", "")
                )
                valor = Decimal(valor_replace)

                data_list.append(data)
                descricao_list.append(descricao)
                valor_list.append(valor)
                deb_cred_list.append(deb_cred)

        if not linhas_imprimir:
            break

    df = pd.DataFrame(
        {
            "DATA": data_list,
            "DEB": [23 if dc == "DEB" else None for dc in deb_cred_list],
            "CRED": [23 if dc == "CRED" else None for dc in deb_cred_list],
            "VALOR": valor_list,
            "DESCRICAO": descricao_list,
        }
    )

    return df
