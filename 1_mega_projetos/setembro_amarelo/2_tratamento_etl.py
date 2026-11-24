import os
import sys
import tkinter as tk
from tkinter import filedialog
import pandas as pd


def selecionar_arquivos():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    arquivos = filedialog.askopenfilenames(
        title="Selecione os arquivos CSV limpos (formato matriz)",
        filetypes=[("Arquivos CSV", "*.csv")],
    )
    return arquivos


def unpivot_datasus_limpo(caminho_arquivo):
    nome_base = os.path.basename(caminho_arquivo)
    print(f"Processando: {nome_base}")

    # Ignora arquivos que já são o resultado tratado
    if nome_base.startswith("tratado_"):
        print(f"  -> Ignorado: {nome_base} já é um arquivo tratado final.\n")
        return

    df = pd.read_csv(caminho_arquivo)

    # Verifica se o arquivo já possui a coluna 'obitos' (já está unpivoted)
    if "obitos" in df.columns and "ano" in df.columns:
        print(
            f"  -> AVISO: {nome_base} já está no formato relacional (unpivoted). Nenhuma ação necessária.\n"
        )
        return

    # Identifica a coluna dimensional (a segunda coluna do arquivo)
    coluna_dimensao = df.columns[1]

    # Remove totais e linhas de rodapé do DATASUS
    df_filtrado = df[
        ~df[coluna_dimensao].isin(["Total", "&"])
        & ~df[coluna_dimensao].str.contains("&", na=False)
    ].copy()

    # Tratamento específico para a tabela de Estados/Regiões (mortalidade_causas_externas_x60_x84_limpo.csv)
    if (
        "Região/Unidade" in coluna_dimensao
        or "UF" in coluna_dimensao
        or "Federação" in coluna_dimensao
    ):
        df_filtrado = df_filtrado[
            df_filtrado[coluna_dimensao].str.startswith("..", na=False)
        ]
        df_filtrado[coluna_dimensao] = df_filtrado[
            coluna_dimensao
        ].str.replace(".. ", "", regex=False)

    # Identifica colunas de anos (2014 a 2024 para análise segura)
    colunas_anos = [str(ano) for ano in range(2014, 2025)]
    colunas_presentes = [
        col for col in colunas_anos if col in df_filtrado.columns
    ]

    if not colunas_presentes:
        print(
            f"  -> AVISO: Nenhuma coluna de ano (2014-2024) foi encontrada em {nome_base}.\n"
        )
        return

    # Limpeza numérica das colunas de anos
    for col in colunas_presentes:
        df_filtrado[col] = (
            df_filtrado[col]
            .astype(str)
            .str.replace("-", "0")
            .str.replace(" ", "")
        )
        df_filtrado[col] = (
            pd.to_numeric(df_filtrado[col], errors="coerce")
            .fillna(0)
            .astype(int)
        )

    # Transformação Melt / Unpivot
    df_melted = pd.melt(
        df_filtrado,
        id_vars=[coluna_dimensao],
        value_vars=colunas_presentes,
        var_name="ano",
        value_name="obitos",
    )

    df_melted["ano"] = df_melted["ano"].astype(int)

    # Exportação
    nome_saida = f"tratado_{nome_base}"
    df_melted.to_csv(nome_saida, index=False, encoding="utf-8-sig")
    print(
        f"  -> Concluído com sucesso! Salvo como: {nome_saida} (Linhas: {len(df_melted)})\n"
    )


if __name__ == "__main__":
    lista_arquivos = selecionar_arquivos()
    for arq in lista_arquivos:
        unpivot_datasus_limpo(arq)