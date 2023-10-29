import pandas as pd
from decimal import Decimal


def process_viacredi(dados_pdf):
    data_list = []
    descricao_list = []
    valor_list = []
    deb_cred_list = []
    stop_process = False

    for pagina_num, pagina in enumerate(dados_pdf.pages, 1):
        texto_pagina = pagina.extract_text()
        linhas = texto_pagina.split("\n")

        if pagina_num == 1:
            linhas_a_pular = 6
        else:
            linhas_a_pular = 1

        stop_process = False

        for linha_num, linha in enumerate(linhas, 1):
            partes = linha.split(" ")
            if (
                len(partes) >= 5
                and "SAC - " not in linha
                and "Finais de Semana" not in linha
                and "OUVIDORIA" not in linha
            ):
                if "Os dados acima" in linha:
                    stop_process = True
                    break
                if linha_num <= linhas_a_pular:
                    continue

                if ":" not in linha:
                    data = partes[-4]
                    valor_str = (
                        partes[-3].replace(".", "").replace(",", ".").replace("-", "")
                    )
                    valor = Decimal(valor_str)
                    descricao = " ".join(partes[0:-4])
                    deb_cred = "CRED" if "-" in partes[-3] else "DEB"
                else:
                    data = partes[-5]
                    valor_str = (
                        partes[-4].replace(".", "").replace(",", ".").replace("-", "")
                    )
                    valor = Decimal(valor_str)
                    descricao = " ".join(partes[0:-5])
                    deb_cred = "CRED" if "-" in partes[-4] else "DEB"

                data_list.append(data)
                descricao_list.append(descricao)
                valor_list.append(valor)
                deb_cred_list.append(deb_cred)

            if stop_process:
                break

        if stop_process:
            break

    df = pd.DataFrame(
        {
            "DATA": data_list,
            "VALOR": valor_list,
            "DEB": [37 if dc == "DEB" else None for dc in deb_cred_list],
            "CRED": [37 if dc == "CRED" else None for dc in deb_cred_list],
            "DESCRICAO": descricao_list,
        }
    )

    return df
