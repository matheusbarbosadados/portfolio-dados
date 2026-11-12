import os
import re
import unicodedata
import tkinter as tk
from collections import Counter
from datetime import date
from difflib import SequenceMatcher
from tkinter import filedialog

import pandas as pd

# ---------- AJUSTES ----------
CORRIGIR_NEGATIVOS = True   # True: troca -50 por 50 | False: só avisa
LIMITE_PARECIDO = 0.92      # usado só para AVISAR de nomes parecidos (nunca altera)
VAZIOS = {"", "n/a", "na", "nan", "null", "none", "-"}
MESES = {"jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
         "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12,
         "feb": 2, "apr": 4, "may": 5, "aug": 8, "sep": 9, "dec": 12}

# ---------- ESCOLHER ARQUIVO ----------
janela = tk.Tk()
janela.withdraw()
janela.attributes("-topmost", True)
ARQUIVO = filedialog.askopenfilename(
    title="Escolha a planilha",
    filetypes=[("Planilhas", "*.csv *.xlsx *.xls")])
if not ARQUIVO:
    raise SystemExit("Nenhum arquivo escolhido.")

# ---------- FUNÇÕES ----------
def sem_acento(t):
    t = unicodedata.normalize("NFD", t)
    return "".join(c for c in t if unicodedata.category(c) != "Mn")

def chave(t):
    return re.sub(r"[^a-z0-9]", "", sem_acento(t).lower())

def consertar_acentos(t):
    for _ in range(2):
        if not re.search("[ÃÂ]", t):
            break
        novo = None
        for enc in ("latin-1", "cp1252"):
            try:
                novo = t.encode(enc).decode("utf-8")
                break
            except (UnicodeEncodeError, UnicodeDecodeError):
                novo = None
        if novo is None or novo == t:
            break
        t = novo
    return t

def ler_arquivo(caminho):
    if caminho.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(caminho, dtype=str, keep_default_na=False)
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return pd.read_csv(caminho, dtype=str, keep_default_na=False,
                               sep=None, engine="python", encoding=enc)
        except UnicodeDecodeError:
            continue
    raise SystemExit("Não consegui ler o arquivo.")

RE_ISO = re.compile(r"(\d{4})-(\d{1,2})-(\d{1,2})(?:[ T].*)?")
RE_DMA = re.compile(r"(\d{1,2})[/.\-]([A-Za-z]{3}|\d{1,2})[/.\-](\d{2}|\d{4})")
RE_NOME_ID = re.compile(r"(^|[_\s])(id|cod|codigo|código)($|[_\s])", re.IGNORECASE)

def parece_data(v):
    return bool(RE_ISO.fullmatch(v) or RE_DMA.fullmatch(v))

def dia_primeiro_da_coluna(valores):
    for v in valores:
        m = RE_DMA.fullmatch(v)
        if m and not m[2].isalpha():
            if int(m[1]) > 12:
                return True
            if int(m[2]) > 12:
                return False
    return True

def ler_data(v, dia_primeiro):
    try:
        m = RE_ISO.fullmatch(v)
        if m:
            return date(int(m[1]), int(m[2]), int(m[3]))
        m = RE_DMA.fullmatch(v)
        if not m:
            return None
        a, b, ano = m.groups()
        if b.isalpha():
            mes = MESES.get(b.lower())
            if mes is None:
                return None
            dia = int(a)
        elif dia_primeiro:
            dia, mes = int(a), int(b)
        else:
            dia, mes = int(b), int(a)
        ano = int(ano)
        if ano < 100:
            ano += 2000
        return date(ano, mes, dia)
    except ValueError:
        return None

def ler_numero(v):
    t = v.replace("R$", "").replace(" ", "")
    if not t:
        return None
    if "," in t and "." in t:
        if t.rfind(",") > t.rfind("."):
            t = t.replace(".", "").replace(",", ".")
        else:
            t = t.replace(",", "")
    elif "," in t:
        if re.fullmatch(r"-?\d+,\d{1,2}", t):
            t = t.replace(",", ".")
        else:
            return None
    elif re.fullmatch(r"-?\d{1,3}(\.\d{3})+", t):
        return None
    if re.fullmatch(r"-?\d+(\.\d+)?", t):
        return t
    return None

def unificar(serie):
    # Junta só diferenças de maiúsculas/minúsculas, espaços e hífen.
    # Acentos e letras diferentes NÃO são juntados.
    cont = Counter(v for v in serie if v.lower() not in VAZIOS)
    grupos = {}
    for v in cont:
        grupos.setdefault(re.sub(r"[\s\-_]", "", v.lower()), []).append(v)
    mapa = {}
    for vs in grupos.values():
        melhor = max(vs, key=lambda x: (cont[x], x != x.upper() and x != x.lower()))
        for v in vs:
            mapa[v] = melhor
    return serie.map(lambda v: mapa.get(v, v))

def achar_parecidos(serie):
    # Só AVISA. Nunca altera nada.
    cont = Counter(v for v in serie if v.lower() not in VAZIOS)
    lista = sorted(cont, key=lambda v: -cont[v])
    pares = []
    for n, b in enumerate(lista):
        kb = chave(b)
        for a in lista[:n]:
            ka = chave(a)
            if ka == kb or (len(ka) >= 5 and len(kb) >= 5
                            and SequenceMatcher(None, ka, kb).ratio() >= LIMITE_PARECIDO):
                pares.append((b, a))
                break
    return pares

def para_numero(v):
    if re.fullmatch(r"-?\d+(\.\d+)?", v):
        return float(v)
    return v

# ---------- LEITURA E LIMPEZA DE TEXTO ----------
df = ler_arquivo(ARQUIVO)
df.columns = [str(c).strip() for c in df.columns]
df = df.astype(str)
df = df.apply(lambda s: s.map(lambda v: re.sub(r"\s+", " ", consertar_acentos(v)).strip()))

print(f"Arquivo: {os.path.basename(ARQUIVO)}")
print(f"Linhas: {len(df)} | Colunas: {len(df.columns)}")

# ---------- DESCOBRIR O TIPO DE CADA COLUNA ----------
tipos = {}
for col in df.columns:
    valores = [v for v in df[col] if v.lower() not in VAZIOS]
    n = len(valores)
    if n == 0:
        tipos[col] = "vazia"
    elif sum(parece_data(v) for v in valores) / n >= 0.6:
        tipos[col] = "data"
    elif sum(ler_numero(v) is not None for v in valores) / n >= 0.6:
        tipos[col] = "numero"
    else:
        u = len(set(valores))
        tipos[col] = "categoria" if u <= 50 and u / n <= 0.5 else "texto"

ids = set()          # identificadores: não sofrem troca de sinal nem alerta de valor alto
ids_unicos = set()   # identificadores que nunca se repetem: ignorados na busca de repetidas
for col, tipo in tipos.items():
    if tipo == "numero":
        valores = [v for v in df[col] if v.lower() not in VAZIOS]
        unico = (len(valores) > 0 and len(set(valores)) == len(valores)
                 and all(re.fullmatch(r"-?\d+", v) for v in valores))
        if unico:
            ids_unicos.add(col)
        if unico or RE_NOME_ID.search(col):
            ids.add(col)

print("\nTIPO DETECTADO EM CADA COLUNA")
for col, tipo in tipos.items():
    extra = " (identificador, não é alterado)" if col in ids else ""
    print(f"  {col}: {tipo}{extra}")

# ---------- CORREÇÕES ----------
alertas = {i: [] for i in df.index}
print("\nCORREÇÕES")

for col, tipo in tipos.items():
    antes = df[col].copy()

    if tipo == "data":
        valores = [v for v in df[col] if v.lower() not in VAZIOS]
        dp = dia_primeiro_da_coluna(valores)
        novos = []
        for i, v in df[col].items():
            if v.lower() in VAZIOS:
                alertas[i].append(f"{col} vazio")
                novos.append(v)
                continue
            d = ler_data(v, dp)
            if d is None:
                alertas[i].append(f"{col} data inválida")
                novos.append(v)
            else:
                novos.append(d.strftime("%Y-%m-%d"))
        df[col] = novos
        print(f"  {col}: {(df[col] != antes).sum()} datas convertidas "
              f"({'dia/mês/ano' if dp else 'mês/dia/ano'})")

    elif tipo == "numero":
        novos = []
        for i, v in df[col].items():
            if v.lower() in VAZIOS:
                alertas[i].append(f"{col} vazio")
                novos.append(v)
                continue
            r = ler_numero(v)
            if r is None:
                alertas[i].append(f"{col} número inválido ou ambíguo")
                novos.append(v)
            else:
                novos.append(r)
        df[col] = novos
        trocados = int((df[col] != antes).sum())
        negativos = 0
        if col not in ids:
            n = pd.to_numeric(df[col], errors="coerce")
            neg = n < 0
            negativos = int(neg.sum())
            if negativos:
                if CORRIGIR_NEGATIVOS:
                    df.loc[neg, col] = df.loc[neg, col].str.lstrip("-")
                else:
                    for i in df.index[neg]:
                        alertas[i].append(f"{col} negativo")
            n = pd.to_numeric(df[col], errors="coerce")
            positivos = n[n > 0]
            if len(positivos) >= 10:
                mediana = positivos.median()
                for i in df.index[n > mediana * 10]:
                    alertas[i].append(f"{col} muito acima do normal")
        print(f"  {col}: {trocados} números convertidos, {negativos} negativos "
              f"{'corrigidos' if CORRIGIR_NEGATIVOS else 'marcados'}")

    elif tipo == "categoria":
        df[col] = unificar(df[col])
        for i, v in df[col].items():
            if v.lower() in VAZIOS:
                alertas[i].append(f"{col} vazio")
        print(f"  {col}: {(df[col] != antes).sum()} células padronizadas")
        for rara, comum in achar_parecidos(df[col]):
            print(f"      parecido, NÃO alterado: '{rara}' e '{comum}' - confira")
            for i in df.index[df[col] == rara]:
                alertas[i].append(f"{col} parecido com '{comum}'")

    elif tipo == "texto":
        df[col] = df[col].map(lambda v: v.title() if v and (v.isupper() or v.islower()) else v)
        for i, v in df[col].items():
            if v.lower() in VAZIOS:
                alertas[i].append(f"{col} vazio")
        print(f"  {col}: {(df[col] != antes).sum()} células ajustadas")

# ---------- LINHAS REPETIDAS ----------
cols_cmp = [c for c in df.columns if c not in ids_unicos]
rep = pd.Series(False, index=df.index)
if cols_cmp:
    rep = df[cols_cmp].apply(lambda s: s.str.lower()).duplicated(keep="first")
print(f"\nLINHAS REPETIDAS REMOVIDAS: {int(rep.sum())}")
if rep.sum():
    print(f"  linhas do arquivo original: {(df.index[rep] + 2).tolist()}")

# ---------- RESULTADO ----------
final = df.copy()
final.insert(0, "linha_original", final.index + 2)
final["alerta"] = ["; ".join(alertas[i]) for i in final.index]
final = final[~rep]

com_alerta = final[final["alerta"] != ""]
print(f"\nLinhas finais: {len(final)} | Linhas com alerta: {len(com_alerta)}")
print("LINHAS COM ALERTA (número da linha no arquivo original):")
for _, r in com_alerta.head(40).iterrows():
    print(f"  linha {r['linha_original']}: {r['alerta']}")
if len(com_alerta) > 40:
    print(f"  ... e mais {len(com_alerta) - 40} linhas (veja a coluna alerta no arquivo)")

base = os.path.splitext(ARQUIVO)[0]
final.to_csv(base + "_limpo.csv", index=False, encoding="utf-8-sig")
print(f"\nSalvo: {base}_limpo.csv")

# Excel: números de verdade e colunas com largura ajustada
try:
    from openpyxl.utils import get_column_letter
    planilha = final.copy()
    for col, tipo in tipos.items():
        if tipo == "numero" and col not in ids:
            planilha[col] = planilha[col].map(para_numero)
    caminho_xlsx = base + "_limpo.xlsx"
    with pd.ExcelWriter(caminho_xlsx, engine="openpyxl") as escritor:
        planilha.to_excel(escritor, index=False, sheet_name="Dados")
        aba = escritor.sheets["Dados"]
        for n, col in enumerate(planilha.columns, start=1):
            maior = max([len(str(col))] + [len(str(v)) for v in planilha[col]])
            aba.column_dimensions[get_column_letter(n)].width = min(maior + 3, 50)
    print(f"Salvo: {caminho_xlsx}")
except Exception:
    print("Não gerei o .xlsx (falta o pacote openpyxl). O .csv está pronto.")