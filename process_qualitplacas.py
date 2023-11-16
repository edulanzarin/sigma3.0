import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
)
import pandas as pd
import sys
from decimal import Decimal
from PyPDF2 import PdfReader
import re


def process_qualitplacas(dados_pdf):
    registros_qualitplacas = []
    linhas_imprimir = False
    linha_anterior_valor_zero = False
    quebra_condicao = "QUALITPLACAS"

    for pagina_num, pagina in enumerate(dados_pdf.pages, 1):
        texto_pagina = pagina.extract_text()
        linhas = texto_pagina.split("\n")
        quebra_pagina = False
        linhas_quebra = 0

        for linha in linhas:
            if quebra_condicao in linha:
                quebra_pagina = True
                linhas_quebra = 0

            if quebra_pagina and pagina_num == 1:
                linhas_quebra += 1
                if (
                    linhas_quebra >= 8
                    and "Histórico" not in linha
                    and "Complemento" not in linha
                ):
                    linhas_quebra = 0
                    linhas_imprimir = True
                    quebra_pagina = False

            if linhas_imprimir:
                if (
                    "Histórico" not in linha
                    and "Complemento" not in linha
                    and "Página:" not in linha
                ):
                    partes = linha.split()
                    if len(partes) > 2:
                        if "BANCO SAFRA MATRIZ" in linha or "9VIACREDI" in linha:
                            partes = [partes[0]] + partes[-3:] + partes
                            data = partes[0]
                            if (
                                "RECEITA DE REBATE" not in linha
                                and "DEVOLUÇÃO DE COMPRA" not in linha
                            ):
                                valor_str = (
                                    partes[2]
                                    .replace("-", "")
                                    .replace(".", "")
                                    .replace(",", ".")
                                )
                                valor = Decimal(valor_str)
                                credito = None
                            else:
                                valor_str = (
                                    partes[1]
                                    .replace("-", "")
                                    .replace(".", "")
                                    .replace(",", ".")
                                )
                                valor = Decimal(valor_str)
                                credito = Decimal(valor_str)

                            if (
                                valor != Decimal(0)
                                and "DESPESAS BANCARIA" not in linha
                                and "ALUGUEIS MAQUINA" not in linha
                            ):
                                if valor == credito:
                                    linha_anterior_valor_zero = False
                                    valor = None
                                else:
                                    linha_anterior_valor_zero = False
                            else:
                                linha_anterior_valor_zero = True
                        else:
                            if linha_anterior_valor_zero:
                                linha_anterior_valor_zero = False
                            else:
                                if "REC.REF.DOC.:" in linha:
                                    partes[0] = partes[0].replace("REC.REF.DOC.:", "")
                                if "PAG.REF.DOC.:" in linha:
                                    partes[0] = partes[0].replace("PAG.REF.DOC.:", "")
                                if (
                                    "PAG.REF.DOC.:AGR" not in linha
                                    and "REC.REF.DOC.:AGR" not in linha
                                ):
                                    if "-" in partes[0]:
                                        partes[0] = partes[0].split("-", 1)[0].lstrip()
                                else:
                                    partes[0] = partes[0].replace(
                                        "PAG.REF.DOC.:AGR", ""
                                    )
                                    partes[0] = partes[0].replace(
                                        "REC.REF.DOC.:AGR", ""
                                    )
                                    if "-" in partes[0]:
                                        partes[0] = partes[0].split("-")[1]
                                    if "/" in partes[0]:
                                        partes[0] = partes[0].split("/")[1]
                                    if "-" in partes[0]:
                                        partes[0] = partes[0].split("-", 1)[1].lstrip()
                                if "SACADO" in linha:
                                    partes[1] = partes[1].replace("SACADO:", "")
                                if "DESC.TITULO" in linha:
                                    partes[0] = partes[0].replace("DESC.TITULO", "")
                                    if "-" in partes[1]:
                                        partes[1] = partes[1].split("-", 1)[0].lstrip()
                                    if "/" in partes[1]:
                                        partes[1] = partes[1].split("/", 1)[0].lstrip()
                                    fornecedor = "DESCONTO DO TITULO " + nota
                                else:
                                    if "-" in partes[1]:
                                        partes[1] = partes[1].split("-", 1)[1].lstrip()

                                if "PAG.REF.DOC.: " in linha:
                                    fornecedor = " ".join(partes[2::])
                                    nota = partes[1]
                                else:
                                    fornecedor = " ".join(partes[1:])
                                    nota = partes[0]

                                    nota = re.sub(r"[a-zA-Z]", "", nota)

                                    registros_qualitplacas.append(
                                        {
                                            "DATA": data,
                                            "FORNECEDOR": fornecedor,
                                            "NOTA": nota,
                                            "VALOR": valor,
                                            "DESCONTO": credito,
                                        }
                                    )

    df_qualit = pd.DataFrame(registros_qualitplacas)
    return df_qualit
