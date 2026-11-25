import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import pandas as pd

pasta_script = Path(__file__).resolve().parent

janela = tk.Tk()
janela.withdraw()
caminho = filedialog.askopenfilename(
    title="Escolha o arquivo CSV",
    initialdir=pasta_script,
    filetypes=[("CSV", "*.csv")],
)
janela.destroy()

if not caminho:
    print("Nenhum arquivo escolhido.")
    raise SystemExit

df = pd.read_csv(caminho, encoding="utf-8-sig")

print("Linhas e colunas:", df.shape)
print()
print("Colunas:", list(df.columns))
print()
print("Primeiras linhas:")
print(df.head())
print()

for coluna in ["situacao", "sexo", "faixa_etaria", "regiao"]:
    print(coluna, "->", df[coluna].unique().tolist())
print()

print("Anos encontrados:", sorted(df["ano"].unique().tolist()))
print("Meses encontrados:", sorted(df["mes"].unique().tolist()))
print()
print("Total de pessoas por situacao:")
print(df.groupby("situacao")["pessoas"].sum())
print()
print("Total de pessoas por ano (Desaparecida):")
print(df[df["situacao"] == "Desaparecida"].groupby("ano")["pessoas"].sum())
print()
print("Valores vazios por coluna:")
print(df.isna().sum())