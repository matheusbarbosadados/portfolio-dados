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

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 50)
pd.set_option("display.max_rows", 200)

df = pd.read_csv(caminho, encoding="utf-8-sig")
desap = df[df["situacao"] == "Desaparecida"]

esperado = pd.MultiIndex.from_product(
    [sorted(df["uf"].unique()), sorted(df["ano"].unique()), range(1, 13)],
    names=["uf", "ano", "mes"],
)
existente = pd.MultiIndex.from_frame(desap[["uf", "ano", "mes"]].drop_duplicates())
faltando = esperado.difference(existente).to_frame(index=False)

print("Meses sem registro por UF e ano:")
print(faltando.groupby(["uf", "ano"]).size().rename("meses_sem_registro"))
print()

print("Desaparecidas por UF e ano:")
print(
    desap.pivot_table(
        index="uf", columns="ano", values="pessoas", aggfunc="sum", fill_value=0
    )
)