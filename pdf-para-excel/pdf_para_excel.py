import re
import sys
from pathlib import Path

import pdfplumber
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

MARGEM_TOPO = 40   # pontos ignorados no topo (número da página)
MARGEM_BASE = 30   # pontos ignorados no rodapé
NEGRITO = Font(bold=True)

CONFIG_LINHAS = {"vertical_strategy": "lines", "horizontal_strategy": "lines"}
CONFIG_TEXTO = {
    "vertical_strategy": "text",
    "horizontal_strategy": "text",
    "min_words_vertical": 2,
    "min_words_horizontal": 2,
}


def converter_valor(valor):
    """Retorna (valor_convertido, formato_do_excel)."""
    if not isinstance(valor, str):
        return valor, None
    texto = valor.strip()
    if not texto:
        return None, None

    moeda = texto.startswith("R$")
    limpo = texto.replace("R$", "").replace(" ", "")
    percentual = limpo.endswith("%")
    limpo = limpo.rstrip("%")

    if re.match(r"^-?0\d", limpo):  # preserva códigos como 00123
        return valor, None

    padrao = r"-?\d{1,3}(\.\d{3})+(,\d+)?|-?\d+(,\d+)?"
    if not re.fullmatch(padrao, limpo):
        return valor, None

    tem_decimal = "," in limpo
    numero = float(limpo.replace(".", "").replace(",", "."))

    if percentual:
        return round(numero / 100, 6), "0.00%"
    if moeda:
        return numero, "R$ #,##0.00"
    if tem_decimal:
        return numero, "#,##0.00"
    return int(numero), None


def tabela_valida(linhas):
    """Evita tratar parágrafos como se fossem tabelas."""
    if len(linhas) < 2:
        return False
    if max(len(l) for l in linhas) < 2:
        return False
    preenchidas = sum(
        1 for l in linhas if sum(1 for c in l if c and str(c).strip()) >= 2
    )
    return preenchidas >= len(linhas) * 0.6


def achar_tabelas(area):
    """Tenta primeiro por linhas desenhadas; se não achar, pelo alinhamento do texto."""
    for config in (CONFIG_LINHAS, CONFIG_TEXTO):
        achadas = [t for t in area.find_tables(config) if tabela_valida(t.extract())]
        if achadas:
            return achadas
    return []


def linhas_fora_das_tabelas(area, caixas):
    def fora(obj):
        if obj.get("object_type") != "char":
            return True
        cx = (obj["x0"] + obj["x1"]) / 2
        cy = (obj["top"] + obj["bottom"]) / 2
        return not any(x0 <= cx <= x1 and t <= cy <= b for x0, t, x1, b in caixas)

    return area.filter(fora).extract_text_lines(return_chars=False)


def processar_pagina(pagina, aba):
    area = pagina.crop(
        (0, MARGEM_TOPO, pagina.width, pagina.height - MARGEM_BASE)
    )
    tabelas = achar_tabelas(area)
    caixas = [t.bbox for t in tabelas]

    itens = []
    for t in tabelas:
        itens.append((round(t.bbox[1]), t.bbox[0], "tabela", t.extract()))
    for l in linhas_fora_das_tabelas(area, caixas):
        itens.append((round(l["top"]), l["x0"], "texto", l["text"]))
    itens.sort(key=lambda i: (i[0], i[1]))

    linha = 1
    larguras = {}
    n_texto = 0

    for _, _, tipo, conteudo in itens:
        if tipo == "texto":
            aba.cell(row=linha, column=1, value=conteudo)
            n_texto += 1
            linha += 1
            continue

        for i, linha_tabela in enumerate(conteudo):
            for col, bruto in enumerate(linha_tabela, start=1):
                if i == 0:
                    valor, formato = (bruto or None), None
                else:
                    valor, formato = converter_valor(bruto)
                celula = aba.cell(row=linha, column=col, value=valor)
                if i == 0:
                    celula.font = NEGRITO
                if formato:
                    celula.number_format = formato
                if valor is not None:
                    maior = max(len(p) for p in str(valor).split("\n"))
                    larguras[col] = max(larguras.get(col, 0), maior)
            linha += 1
        linha += 1  # linha em branco após a tabela

    for col, largura in larguras.items():
        aba.column_dimensions[get_column_letter(col)].width = min(largura + 2, 60)

    avisos = []
    if not itens:
        aba["A1"] = "Página sem texto (pode ser imagem)"
        avisos.append("sem texto - pode ser imagem")
    if pagina.images:
        avisos.append(f"{len(pagina.images)} imagem(ns) não extraída(s)")
    return len(tabelas), n_texto, avisos


def extrair_pdf(caminho_pdf):
    caminho_pdf = Path(caminho_pdf)
    caminho_excel = caminho_pdf.with_suffix(".xlsx")

    wb = Workbook()
    wb.remove(wb.active)

    with pdfplumber.open(caminho_pdf) as pdf:
        for n, pagina in enumerate(pdf.pages, start=1):
            aba = wb.create_sheet(f"Pagina_{n}")
            n_tab, n_txt, avisos = processar_pagina(pagina, aba)
            resumo = f"Página {n}: {n_tab} tabela(s), {n_txt} linha(s) de texto"
            if avisos:
                resumo += " | AVISO: " + "; ".join(avisos)
            print(resumo)

    wb.save(caminho_excel)
    print(f"\nArquivo salvo em {caminho_excel}")


if __name__ == "__main__":
    arquivo = sys.argv[1] if len(sys.argv) > 1 else "entrada.pdf"
    extrair_pdf(arquivo)