import re
from tkinter import Tk, filedialog
from pathlib import Path

import pdfplumber
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter

MARGEM_TOPO = 40
MARGEM_BASE = 30
GAP_COLUNA = 12  # pt: vão entre palavras que indica "outra coluna"

# --- ESTILOS DO EXCEL ---
NEGRITO = Font(bold=True)
PREENCHIMENTO_CABECALHO = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")
BORDA_FINA = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)
ALINHAMENTO_CENTRO = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALINHAMENTO_TEXTO = Alignment(vertical="center", wrap_text=True)

# --- CONFIGURAÇÕES DE EXTRAÇÃO ---
CONFIG_LINHAS = {"vertical_strategy": "lines", "horizontal_strategy": "lines"}
CONFIG_TEXTO = {
    "vertical_strategy": "text",
    "horizontal_strategy": "text",
    "intersection_x_tolerance": 10,
    "intersection_y_tolerance": 5,
    "snap_x_tolerance": 3,
    "snap_y_tolerance": 3,
    "min_words_vertical": 2,
    "min_words_horizontal": 2,
}


# ======================================================================
# CONVERSÃO DE VALORES (igual à sua versão)
# ======================================================================
def limpar_e_converter_valor(valor):
    if not isinstance(valor, str):
        return valor, None

    texto = valor.strip().replace("\n", " ")
    if not texto or texto.lower() == "none":
        return "", None

    moeda = "R$" in texto
    limpo = texto.replace("R$", "").replace(" ", "")
    percentual = limpo.endswith("%")
    limpo = limpo.rstrip("%")

    if re.match(r"^-?0\d+", limpo):
        return f"'{texto}", None

    padrao = r"^-?\d{1,3}(\.\d{3})+(,\d+)?$|^-?\d+(,\d+)?$"
    if not re.fullmatch(padrao, limpo):
        if texto.startswith(("=", "+", "-")):
            return f"'{texto}", None
        return texto, None

    tem_decimal = "," in limpo
    try:
        numero = float(limpo.replace(".", "").replace(",", "."))
        if percentual:
            return round(numero / 100, 6), "0.00%"
        if moeda:
            return numero, "R$ #,##0.00"
        if tem_decimal:
            return numero, "#,##0.00"
        return int(numero), "0"
    except ValueError:
        if texto.startswith(("=", "+", "-")):
            return f"'{texto}", None
        return texto, None


# ======================================================================
# NEGRITO E MATRIZ RICA
# ======================================================================
def verificar_negrito(pagina, bbox):
    """Lê a região da célula no PDF e verifica se a fonte original é negrito."""
    if not bbox:
        return False
    try:
        x0 = max(0, bbox[0])
        top = max(0, bbox[1])
        x1 = min(pagina.width, bbox[2])
        bottom = min(pagina.height, bbox[3])
        if x0 >= x1 or top >= bottom:
            return False
        chars = [c for c in pagina.crop((x0, top, x1, bottom)).chars if c["text"].strip()]
        if not chars:
            return False
        negritos = sum(1 for c in chars if "bold" in c.get("fontname", "").lower())
        return (negritos / len(chars)) > 0.4
    except Exception:
        return False


def extrair_matriz_rica(pagina, tabela_obj):
    """Texto, negrito e mesclagem (span) de cada célula.
    CORREÇÃO: usa tabela.rows[i].cells[j] (antes usava tabela.cells, que é uma lista simples)."""
    conteudo = tabela_obj.extract()
    linhas_obj = tabela_obj.rows
    matriz = []
    for i, linha_txt in enumerate(conteudo):
        bboxes = linhas_obj[i].cells if i < len(linhas_obj) else []
        linha_rica = []
        for j, txt in enumerate(linha_txt):
            bbox = bboxes[j] if j < len(bboxes) else None
            is_bold = bool(bbox and txt and str(txt).strip() and verificar_negrito(pagina, bbox))
            linha_rica.append({"texto": txt, "bold": is_bold, "span": 1})
        # células mescladas: texto seguido de None = célula que se estende para a direita
        j = 0
        while j < len(linha_rica):
            if linha_rica[j]["texto"]:
                k = j + 1
                while k < len(linha_rica) and linha_rica[k]["texto"] is None:
                    k += 1
                linha_rica[j]["span"] = k - j
                j = k
            else:
                j += 1
        matriz.append(linha_rica)
    return matriz


def limpar_matriz_rica(matriz, remover_vazias=True):
    """Junta 'R$' solto com o valor ao lado. Só remove colunas vazias quando remover_vazias=True
    (use True para tabelas vindas da estratégia de texto, que criam colunas fantasmas)."""
    tabela_ajustada = []
    for linha in matriz:
        nova_linha = []
        pular = False
        for i, celula in enumerate(linha):
            if pular:
                pular = False
                continue
            texto = str(celula["texto"]).strip() if celula["texto"] is not None else ""
            if texto in ("R$", "R\\$") and i + 1 < len(linha):
                proximo = str(linha[i + 1]["texto"]).strip() if linha[i + 1]["texto"] is not None else ""
                nova_linha.append({
                    "texto": f"R$ {proximo}",
                    "bold": celula["bold"] or linha[i + 1]["bold"],
                    "span": 1,
                })
                pular = True
            else:
                nova_linha.append(celula)
        tabela_ajustada.append(nova_linha)

    if not tabela_ajustada:
        return []

    num_cols = max(len(l) for l in tabela_ajustada)
    if remover_vazias:
        cols_validas = [
            c for c in range(num_cols)
            if any(c < len(l) and l[c]["texto"] and str(l[c]["texto"]).strip() for l in tabela_ajustada)
        ]
    else:
        cols_validas = list(range(num_cols))

    final = []
    for linha in tabela_ajustada:
        nova = [dict(linha[i]) if i < len(linha) else {"texto": "", "bold": False, "span": 1}
                for i in cols_validas]
        if remover_vazias:
            for c in nova:
                c["span"] = 1
        final.append(nova)
    return final


# ======================================================================
# DETECÇÃO DE TABELAS
# ======================================================================
def tabela_valida_conteudo(linhas):
    """Validação por conteúdo (usada só na estratégia de texto, que gera falsos positivos)."""
    if len(linhas) < 2:
        return False
    if max(len(l) if l else 0 for l in linhas) < 2:
        return False
    preenchidas = sum(1 for l in linhas if l and sum(1 for c in l if c and str(c).strip()) >= 2)
    return preenchidas >= len(linhas) * 0.5


def tabela_valida_estrutura(linhas):
    """Tabela desenhada com bordas vale mesmo com células vazias (ex.: linha 'Totais' a preencher)."""
    return bool(linhas) and max(len(l) if l else 0 for l in linhas) >= 2


def celula_tem_colunas_internas(pagina, bbox):
    """True se, dentro de UMA célula, palavras da mesma linha estão separadas por vão grande
    (sinal de que o pdfplumber juntou várias colunas numa célula só)."""
    try:
        palavras = pagina.crop(bbox).extract_words()
    except Exception:
        return False
    linhas = {}
    for w in palavras:
        linhas.setdefault(round(w["top"] / 3), []).append(w)
    for ws in linhas.values():
        ws.sort(key=lambda w: w["x0"])
        for a, b in zip(ws, ws[1:]):
            if b["x0"] - a["x1"] > GAP_COLUNA:
                return True
    return False


def tabela_degenerada(pagina, t):
    """Tabela com borda externa, mas sem divisórias internas: várias linhas/colunas viram uma célula."""
    conteudo = t.extract()
    for i, linha in enumerate(t.rows):
        for j, bbox in enumerate(linha.cells):
            txt = conteudo[i][j] if i < len(conteudo) and j < len(conteudo[i]) else None
            if bbox and txt and str(txt).count("\n") >= 2 and celula_tem_colunas_internas(pagina, bbox):
                return True
    return False


def matriz_por_palavras(pagina, bbox):
    """Reconstrói uma tabela a partir das palavras da região:
    linhas por altura, colunas por sobreposição horizontal."""
    palavras = pagina.crop(bbox).extract_words()
    linhas = []
    for w in sorted(palavras, key=lambda w: (w["top"], w["x0"])):
        if linhas and abs(w["top"] - linhas[-1]["top"]) <= 3:
            linhas[-1]["ws"].append(w)
        else:
            linhas.append({"top": w["top"], "bottom": w["bottom"], "ws": [w]})

    frases = []
    for li, l in enumerate(linhas):
        atual = []
        for w in sorted(l["ws"], key=lambda w: w["x0"]):
            if atual and w["x0"] - atual[-1]["x1"] > GAP_COLUNA:
                frases.append((li, atual))
                atual = []
            atual.append(w)
        if atual:
            frases.append((li, atual))

    colunas = []  # [x0, x1]
    for _, ws in sorted(frases, key=lambda f: f[1][0]["x0"]):
        x0, x1 = ws[0]["x0"], ws[-1]["x1"]
        for c in colunas:
            if x0 <= c[1] + 2 and x1 >= c[0] - 2:
                c[0], c[1] = min(c[0], x0), max(c[1], x1)
                break
        else:
            colunas.append([x0, x1])
    colunas.sort()

    matriz = [[{"texto": "", "bold": False, "span": 1} for _ in colunas] for _ in linhas]
    for li, ws in frases:
        x0, x1 = ws[0]["x0"], ws[-1]["x1"]
        j = next(k for k, c in enumerate(colunas) if x0 <= c[1] + 2 and x1 >= c[0] - 2)
        matriz[li][j] = {
            "texto": " ".join(w["text"] for w in ws),
            "bold": verificar_negrito(pagina, (x0, ws[0]["top"], x1, ws[0]["bottom"])),
            "span": 1,
        }
    return matriz, [l["top"] for l in linhas]


def achar_tabelas(pagina, area):
    """Devolve lista de dicts com: matriz, bbox, row_tops."""
    achadas = [t for t in area.find_tables(CONFIG_LINHAS) if tabela_valida_estrutura(t.extract())]
    resultado = []
    if achadas:
        for t in achadas:
            if tabela_degenerada(pagina, t):
                m, tops = matriz_por_palavras(pagina, t.bbox)
                resultado.append({"matriz": m, "bbox": t.bbox, "row_tops": tops})
            else:
                m = limpar_matriz_rica(extrair_matriz_rica(pagina, t), remover_vazias=False)
                resultado.append({"matriz": m, "bbox": t.bbox, "row_tops": [r.bbox[1] for r in t.rows]})
        return resultado

    # sem bordas na página: estratégia de texto, com validação por conteúdo
    for t in area.find_tables(CONFIG_TEXTO):
        if tabela_valida_conteudo(t.extract()):
            m = limpar_matriz_rica(extrair_matriz_rica(pagina, t), remover_vazias=True)
            resultado.append({"matriz": m, "bbox": t.bbox, "row_tops": [r.bbox[1] for r in t.rows]})
    return resultado


# ======================================================================
# TEXTO SOLTO (fora das tabelas)
# ======================================================================
def segmentos_fora_das_tabelas(pagina, area, caixas):
    """Texto fora das tabelas, quebrado em segmentos quando há vão grande (colunas).
    Descarta número de página solto no topo/rodapé."""
    def fora(obj):
        if obj.get("object_type") != "char":
            return True
        cx = (obj["x0"] + obj["x1"]) / 2
        cy = (obj["top"] + obj["bottom"]) / 2
        return not any(x0 <= cx <= x1 and t <= cy <= b for x0, t, x1, b in caixas)

    palavras = area.filter(fora).extract_words()
    linhas = []
    for w in sorted(palavras, key=lambda w: (w["top"], w["x0"])):
        if linhas and abs(w["top"] - linhas[-1]["top"]) <= 3:
            linhas[-1]["ws"].append(w)
        else:
            linhas.append({"top": w["top"], "bottom": w["bottom"], "ws": [w]})

    segs = []
    for l in linhas:
        ws = sorted(l["ws"], key=lambda w: w["x0"])
        texto_linha = " ".join(w["text"] for w in ws)
        if re.fullmatch(r"\d{1,3}", texto_linha) and (
                l["top"] > pagina.height * 0.9 or l["top"] < pagina.height * 0.06):
            continue
        grupos, atual = [], []
        for w in ws:
            if atual and w["x0"] - atual[-1]["x1"] > GAP_COLUNA:
                grupos.append(atual)
                atual = []
            atual.append(w)
        if atual:
            grupos.append(atual)
        for g in grupos:
            segs.append({
                "tipo": "texto",
                "texto": " ".join(w["text"] for w in g),
                "x0": g[0]["x0"], "x1": g[-1]["x1"],
                "top": l["top"], "bottom": l["bottom"],
            })
    return segs


# ======================================================================
# LAYOUT: faixas horizontais, tabelas e textos lado a lado
# ======================================================================
def agrupar_em_faixas(itens):
    """Itens que se sobrepõem na vertical ficam na mesma faixa (ficam lado a lado na planilha)."""
    itens = sorted(itens, key=lambda i: (i["top"], i["x0"]))
    faixas = []
    for it in itens:
        if faixas and it["top"] < faixas[-1]["bottom"] - 2:
            faixas[-1]["itens"].append(it)
            faixas[-1]["bottom"] = max(faixas[-1]["bottom"], it["bottom"])
        else:
            faixas.append({"top": it["top"], "bottom": it["bottom"], "itens": [it]})
    return faixas


def linha_relativa(faixa, y):
    """Em qual linha da tabela principal da faixa fica a altura y (alinha textos ao lado de tabelas)."""
    tabelas = [i for i in faixa["itens"] if i["tipo"] == "tabela"]
    if not tabelas:
        return 0
    ref = max(tabelas, key=lambda i: len(i["row_tops"]))
    off = 0
    for k, tp in enumerate(ref["row_tops"]):
        if tp <= y + 2:
            off = k
    return off


def blocos_da_faixa(faixa):
    """Ordena tabelas e colunas de texto da esquerda para a direita e define a coluna inicial de cada bloco."""
    blocos = [
        {"tipo": "tabela", "x0": i["x0"], "larg": max(len(l) for l in i["matriz"]), "item": i}
        for i in faixa["itens"] if i["tipo"] == "tabela"
    ]
    textos = sorted([i for i in faixa["itens"] if i["tipo"] == "texto"], key=lambda i: i["x0"])
    cluster = []
    for t in textos:
        if cluster and t["x0"] - cluster[-1]["x0"] > 6:
            blocos.append({"tipo": "texto", "x0": cluster[0]["x0"], "larg": 1, "itens": cluster})
            cluster = []
        cluster.append(t)
    if cluster:
        blocos.append({"tipo": "texto", "x0": cluster[0]["x0"], "larg": 1, "itens": cluster})

    blocos.sort(key=lambda b: b["x0"])
    col = 1
    for k, b in enumerate(blocos):
        if k and (b["tipo"] == "tabela" or blocos[k - 1]["tipo"] == "tabela"):
            col += 1  # coluna de respiro ao lado de tabelas
        b["col"] = col
        col += b["larg"]
    return blocos


# ======================================================================
# ESCRITA NO EXCEL
# ======================================================================
def escrever_tabela(aba, matriz, linha0, col0, larguras):
    tem_bold = any(c["bold"] for l in matriz for c in l)
    for i, linha_tabela in enumerate(matriz):
        nao_vazias = [c for c in linha_tabela if c["texto"]]
        pct_bold = (sum(1 for c in nao_vazias if c["bold"]) / len(nao_vazias)) if nao_vazias else 0
        # cabeçalho: 1ª linha em negrito no PDF; se o PDF não tem nenhum negrito, 1ª linha de tabela com 3+ linhas
        eh_cab = i == 0 and (pct_bold >= 0.5 or (not tem_bold and len(matriz) >= 3))

        for j, cr in enumerate(linha_tabela):
            col = col0 + j
            valor, formato = limpar_e_converter_valor(cr["texto"])
            celula = aba.cell(row=linha0 + i, column=col, value=valor)
            celula.border = BORDA_FINA
            celula.alignment = ALINHAMENTO_TEXTO

            if cr["bold"] or eh_cab:
                celula.font = NEGRITO
            if eh_cab:
                celula.fill = PREENCHIMENTO_CABECALHO
                celula.alignment = ALINHAMENTO_CENTRO
            if formato:
                celula.number_format = formato

            if valor != "" and cr["span"] == 1:
                tam = max(len(p) for p in str(valor).replace("'", "").split("\n"))
                larguras[col] = max(larguras.get(col, 10), tam)

            if cr["span"] > 1:
                for k in range(1, cr["span"]):
                    aba.cell(row=linha0 + i, column=col + k).border = BORDA_FINA
                aba.merge_cells(start_row=linha0 + i, start_column=col,
                                end_row=linha0 + i, end_column=col + cr["span"] - 1)
                celula.alignment = ALINHAMENTO_CENTRO
    return len(matriz), (max(len(l) for l in matriz) if matriz else 0)


def processar_pagina(pagina, aba):
    area = pagina.crop((0, MARGEM_TOPO, pagina.width, pagina.height - MARGEM_BASE))
    achadas = achar_tabelas(pagina, area)
    caixas = [a["bbox"] for a in achadas]

    itens = [{
        "tipo": "tabela", "matriz": a["matriz"], "row_tops": a["row_tops"],
        "x0": a["bbox"][0], "x1": a["bbox"][2], "top": a["bbox"][1], "bottom": a["bbox"][3],
    } for a in achadas]
    segs = segmentos_fora_das_tabelas(pagina, area, caixas)
    itens += segs

    avisos = []
    if not itens:
        aba["A1"] = "Página sem texto detectado."
        avisos.append("sem texto detectado")
        return 0, 0, avisos

    larguras = {}
    linha_atual = 1
    fim_anterior = None

    for faixa in agrupar_em_faixas(itens):
        if fim_anterior is not None:
            gap = faixa["top"] - fim_anterior
            linha_atual += 0 if gap < 6 else (1 if gap < 28 else 2)

        max_linhas = 1
        for b in blocos_da_faixa(faixa):
            if b["tipo"] == "tabela":
                n_l, _ = escrever_tabela(aba, b["item"]["matriz"], linha_atual, b["col"], larguras)
                max_linhas = max(max_linhas, n_l)
            else:
                for it in b["itens"]:
                    off = linha_relativa(faixa, it["top"])
                    valor, formato = limpar_e_converter_valor(it["texto"])
                    if isinstance(valor, str):
                        valor = it["texto"]  # texto solto: grava como está (sem apóstrofo)
                    celula = aba.cell(row=linha_atual + off, column=b["col"], value=valor)
                    if isinstance(valor, str) and valor.startswith("="):
                        celula.data_type = "s"
                    if formato:
                        celula.number_format = formato
                    celula.font = Font(italic=True, color="333333")
                    max_linhas = max(max_linhas, off + 1)

        linha_atual += max_linhas
        fim_anterior = faixa["bottom"]

    for col, largura in larguras.items():
        aba.column_dimensions[get_column_letter(col)].width = min(largura + 3, 50)

    return len(achadas), len(segs), avisos


# ======================================================================
# ENTRADA / SAÍDA
# ======================================================================
def escolher_pdf():
    janela = Tk()
    janela.withdraw()
    janela.attributes("-topmost", True)
    arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")],
    )
    janela.destroy()
    if not arquivo:
        raise SystemExit("Operação cancelada. Nenhum PDF escolhido.")
    return arquivo


def extrair_pdf(caminho_pdf):
    caminho_pdf = Path(caminho_pdf)
    caminho_excel = caminho_pdf.with_suffix(".xlsx")

    wb = Workbook()
    wb.remove(wb.active)

    with pdfplumber.open(caminho_pdf) as pdf:
        for n, pagina in enumerate(pdf.pages, start=1):
            aba = wb.create_sheet(f"Página_{n}")
            n_tab, n_txt, avisos = processar_pagina(pagina, aba)

            resumo = f"Página {n}: {n_tab} tabela(s), {n_txt} bloco(s) de texto"
            if avisos:
                resumo += " | Avisos: " + "; ".join(avisos)
            print(resumo)

    wb.save(caminho_excel)
    print(f"\nExtração concluída com sucesso! Arquivo salvo em:\n{caminho_excel}")


if __name__ == "__main__":
    print("Selecione o arquivo PDF na janela que foi aberta...")
    arquivo = escolher_pdf()
    extrair_pdf(arquivo)