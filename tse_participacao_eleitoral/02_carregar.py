from getpass import getpass
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine, text

PASTA = Path(__file__).resolve().parent
ARQUIVO = PASTA / "02_dados_limpos" / "presidente_munzona.csv"

df = pd.read_csv(ARQUIVO, sep=";", decimal=",", encoding="utf-8-sig")
print("Linhas no CSV:", len(df))

usuario = input("Usuário do MySQL (Enter para root): ").strip() or "root"
senha = getpass("Senha do MySQL (não aparece na tela): ")

url = f"mysql+pymysql://{usuario}:{quote_plus(senha)}@localhost:3306/tse_participacao?charset=utf8mb4"
engine = create_engine(url)

with engine.begin() as conexao:
    conexao.execute(text("TRUNCATE TABLE presidente_munzona"))

df.to_sql("presidente_munzona", engine, if_exists="append",
          index=False, chunksize=1000)

with engine.connect() as conexao:
    total = conexao.execute(text("SELECT COUNT(*) FROM presidente_munzona")).scalar()
print("Linhas no MySQL:", total)
print("Conferência:", "OK" if total == len(df) else "NÚMEROS DIFERENTES")