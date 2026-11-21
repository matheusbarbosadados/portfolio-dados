from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import pandas as pd

PASTA = Path(__file__).resolve().parent

COLUNAS = [
    "NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO", "NR_ZONA",
    "DS_CARGO", "QT_APTOS", "QT_COMPARECIMENTO", "QT_ABSTENCOES", "QT_ELEITORES_SECOES_NAO_INSTALADAS",
    "ST_VOTO_EM_TRANSITO", "QT_VOTOS_BRANCOS", "QT_TOTAL_VOTOS_NULOS",
]
NUMEROS = ["QT_APTOS", "QT_COMPARECIMENTO", "QT_ABSTENCOES",
           "QT_VOTOS_BRANCOS", "QT_TOTAL_VOTOS_NULOS",
           "QT_ELEITORES_SECOES_NAO_INSTALADAS"]


def escolher_arquivo():
    janela = tk.Tk()
    janela.withdraw()
    janela.attributes("-topmost", True)
    caminho = filedialog.askopenfilename(
        title="Escolha o arquivo detalhe_votacao_munzona_2026.csv",
        initialdir=Path(__file__).resolve().parent,
        filetypes=[("CSV", "*.csv"), ("Todos", "*.*")],
    )
    janela.destroy()
    return caminho


def ler_csv(caminho):
    try:
        return pd.read_csv(caminho, sep=";", encoding="utf-8-sig",
                           usecols=COLUNAS, dtype=str)
    except UnicodeDecodeError:
        return pd.read_csv(caminho, sep=";", encoding="latin-1",
                           usecols=COLUNAS, dtype=str)


caminho = escolher_arquivo()
if not caminho:
    print("Nenhum arquivo escolhido.")
    raise SystemExit

df = ler_csv(caminho)
print("Linhas lidas:", len(df))
print("\nCargos no arquivo:")
print(df["DS_CARGO"].value_counts())

df = df[df["DS_CARGO"] == "Presidente"].copy()
for coluna in NUMEROS:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce").fillna(0).astype(int)
df = df.rename(columns={"QT_VOTOS_BRANCOS": "QT_BRANCOS",
                        "QT_TOTAL_VOTOS_NULOS": "QT_NULOS"})

print("\nLinhas de Presidente:", len(df))
print("\nVoto em trânsito:")
print(df["ST_VOTO_EM_TRANSITO"].value_counts())

chave = ["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NR_ZONA"]
print("\nLinhas repetidas pela chave:", df.duplicated(chave).sum())
soma = df["QT_COMPARECIMENTO"] + df["QT_ABSTENCOES"] + df["QT_ELEITORES_SECOES_NAO_INSTALADAS"]
erros = (soma != df["QT_APTOS"]).sum()
print("Linhas que continuam sem fechar com aptos:", erros)

saida = PASTA / "02_dados_limpos"
saida.mkdir(exist_ok=True)
df.to_csv(saida / "presidente_munzona.csv", sep=";", decimal=",",
          encoding="utf-8-sig", index=False)

resumo = df.groupby(["NR_TURNO", "SG_UF"], as_index=False)[
    ["QT_APTOS", "QT_COMPARECIMENTO", "QT_ABSTENCOES", "QT_BRANCOS", "QT_NULOS",
     "QT_ELEITORES_SECOES_NAO_INSTALADAS"]
].sum()
resumo["PCT_ABSTENCAO"] = (resumo["QT_ABSTENCOES"] / resumo["QT_APTOS"] * 100).round(2)
resumo["PCT_BRANCOS"] = (resumo["QT_BRANCOS"] / resumo["QT_COMPARECIMENTO"] * 100).round(2)
resumo["PCT_NULOS"] = (resumo["QT_NULOS"] / resumo["QT_COMPARECIMENTO"] * 100).round(2)
resumo.to_csv(saida / "resumo_por_uf.csv", sep=";", decimal=",",
              encoding="utf-8-sig", index=False)

print("\nResumo por estado, turno 1:")
print(resumo[resumo["NR_TURNO"] == "1"].to_string(index=False))
print("\nPronto. Arquivos salvos em:", saida)