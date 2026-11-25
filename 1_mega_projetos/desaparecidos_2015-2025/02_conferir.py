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
desap = df[df["situacao"] == "Desaparecida"]

print("Quantidade de UFs:", df["uf"].nunique())
chaves = ["situacao", "uf", "ano", "mes", "sexo", "faixa_etaria"]
print("Linhas repetidas:", df.duplicated(subset=chaves).sum())
print("Linhas com pessoas menor ou igual a 0:", (df["pessoas"] <= 0).sum())
print()

esperado = pd.MultiIndex.from_product(
    [sorted(df["uf"].unique()), sorted(df["ano"].unique()), range(1, 13)],
    names=["uf", "ano", "mes"],
)
existente = pd.MultiIndex.from_frame(desap[["uf", "ano", "mes"]].drop_duplicates())
faltando = esperado.difference(existente)
print("Combinações UF, ano e mês sem registro de desaparecida:", len(faltando))
print(list(faltando[:20]))
print()

tabela = df.pivot_table(index="ano", columns="situacao", values="pessoas", aggfunc="sum")
tabela["localizada_%"] = (tabela["Localizada"] / tabela["Desaparecida"] * 100).round(1)
print(tabela)
print()

print("Desaparecidas por mês em 2025:")
print(desap[desap["ano"] == 2025].groupby("mes")["pessoas"].sum())
print()

print("Desaparecidas por região (2015 a 2025):")
print(desap.groupby("regiao")["pessoas"].sum().sort_values(ascending=False))