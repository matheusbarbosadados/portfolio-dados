from pathlib import Path
from tkinter import Tk, filedialog
import pandas as pd

pasta_script = Path(__file__).resolve().parent
root = Tk()
root.withdraw()
arquivo = filedialog.askopenfilename(
    title="Selecione o CSV leve do ISP (EstatisticaMensalPorMunicipio.csv)",
    initialdir=str(pasta_script),
    filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
)
root.destroy()

if not arquivo:
    raise SystemExit("Nenhum arquivo selecionado.")

separador = ";"
for enc in ("latin1", "utf-8-sig", "cp1252"):
    try:
        primeira_linha = Path(arquivo).open(encoding=enc).readline()
        if "\t" in primeira_linha and primeira_linha.count("\t") > primeira_linha.count(";"):
            separador = "\t"
        elif "," in primeira_linha and primeira_linha.count(",") > primeira_linha.count(";"):
            separador = ","
        df = pd.read_csv(arquivo, sep=separador, encoding=enc, low_memory=False)
        break
    except UnicodeDecodeError:
        continue

df.columns = [c.strip().lower() for c in df.columns]

col_munic = "munic" if "munic" in df.columns else "municipio"
if col_munic in df.columns:
    df_rio = df[df[col_munic].astype(str).str.lower().str.contains("rio de janeiro")].copy()
else:
    df_rio = df.copy()

if "ano" in df.columns:
    df_rio["ano"] = pd.to_numeric(df_rio["ano"], errors="coerce")
    df_rio = df_rio[(df_rio["ano"] >= 2015) & (df_rio["ano"] <= 2025)]

linhas_txt = [
    f"Arquivo analisado: {Path(arquivo).name}",
    f"Município: Rio de Janeiro",
    f"Período: 2015 a 2025",
    f"Total de meses analisados: {len(df_rio)}",
    "\n--- EVOLUÇÃO ANUAL DE ROUBOS E FURTOS (2015-2025) ---",
]

if "ano" in df.columns:
    colunas_soma = [c for c in df_rio.columns if c not in ["ano", "mes", col_munic, "fosp", "fase", "regiao"]]
    resumo_ano = df_rio.groupby("ano")[colunas_soma].sum(numeric_only=True)
    
    for ano, linha in resumo_ano.iterrows():
        furtos = linha.get("total_furtos", 0)
        roubos = linha.get("total_roubos", 0)
        linhas_txt.append(f"Ano {int(ano)} -> Total Furtos: {int(furtos):,} | Total Roubos: {int(roubos):,}".replace(",", "."))

linhas_txt.append("\n--- TOTAIS ACUMULADOS NO PERÍODO (2015-2025) ---")
colunas_num = df_rio.select_dtypes(include=["number"]).columns
for col in colunas_num:
    if col not in ["ano", "mes"]:
        total_val = df_rio[col].sum()
        linhas_txt.append(f"{col}: {int(total_val):,}".replace(",", "."))

saida = pasta_script / "resumo_isp_10anos.txt"
saida.write_text("\n".join(linhas_txt), encoding="utf-8")
print(f"Resumo de 10 anos salvo com sucesso em: {saida}")