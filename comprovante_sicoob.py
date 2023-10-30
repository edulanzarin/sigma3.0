import pandas as pd
from decimal import Decimal
import pandas as pd

def comprovante_sicoob(dados_pdf):
    data_list = []
    descricao_list = []
    valor_list = []
    desconto_list = []
    juros_list = []

    coleta_ativa = False
    elementos_coletados = {"data": None, "descricao": None, "valor": None, "desconto": None, "juros": None}

    for pagina_num, pagina in enumerate(dados_pdf.pages, 1):
        texto_pagina = pagina.extract_text()
        linhas = texto_pagina.split("\n")

        for linha in linhas:
            partes = linha.split(" ")

            if "Pagamento de Boleto" in linha:
                coleta_ativa = True

            if coleta_ativa and "Pagador:" not in linha and "CPF/" not in linha and "Nome/" not in linha:
                if "Nome Fantasia Beneficiário:" in linha or "Nome Fantasia  Beneficiário:" in linha or "Nome Fantasia:" in linha or "Beneficiário:" in linha:
                    elementos_coletados["descricao"] = " ".join(partes[4:])
                if "Data Pagamento:" in linha:
                    elementos_coletados["data"] = partes[-1]
                if "Valor Documento:" in linha:
                    valor_str = partes[-1]
                    valor_replace = valor_str.replace(".", "").replace(",", ".")
                    elementos_coletados["valor"] = Decimal(valor_replace)
                if "(-)" in linha:
                    desconto_str = partes[-1]
                    elementos_coletados["desconto"] = desconto_str.replace(".", "").replace(",", ".")
                if "(+)" in linha:
                    juros_str = partes[-1]
                    elementos_coletados["juros"] = juros_str.replace(".", "").replace(",", ".")

                if all(elementos_coletados.values()):
                    # Todos os elementos foram encontrados, podemos sair do loop de coleta
                    data_list.append(elementos_coletados["data"])
                    descricao_list.append(elementos_coletados["descricao"])
                    valor_list.append(elementos_coletados["valor"])
                    desconto_list.append(elementos_coletados["desconto"])
                    juros_list.append(elementos_coletados["juros"])
                    elementos_coletados = {"data": None, "descricao": None, "valor": None, "desconto": None, "juros": None}
                    coleta_ativa = False

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
