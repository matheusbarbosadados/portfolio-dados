import sys
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from pathlib import Path


def selecionar_arquivo():
    """Abre caixa de diálogo para seleção do arquivo CSV do DATASUS."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo CSV do DATASUS",
        initialdir=Path(__file__).resolve().parent,
        filetypes=[("Arquivos CSV", "*.csv"), ("Arquivos de Texto", "*.txt")],
    )

    return caminho_arquivo


def processar_dados_datasus(caminho_arquivo):
    """Executa a limpeza, estruturação e unpivot dos dados de mortalidade."""
    if not caminho_arquivo:
        print("Nenhum arquivo selecionado. Processamento cancelado.")
        return

    print(f"Lendo arquivo: {caminho_arquivo}")

    # Tenta ler primeiramente em UTF-8 (padrão VS Code) e depois em Latin-1
    encodings_para_testar = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
    linhas = None
    encoding_correto = "utf-8"

    for enc in encodings_para_testar:
        try:
            with open(caminho_arquivo, "r", encoding=enc) as f:
                linhas = f.readlines()
            encoding_correto = enc
            break
        except UnicodeDecodeError:
            continue

    if not linhas:
        print("Não foi possível ler o arquivo com as codificações padrão.")
        return

    # Procura a linha do cabeçalho principal contendo a coluna de Região/UF
    inicio_dados = 0
    for i, linha in enumerate(linhas):
        if "Regi" in linha and "Unidade da Federa" in linha:
            inicio_dados = i
            break

    # Carrega a tabela via Pandas
    df = pd.read_csv(
        caminho_arquivo,
        skiprows=inicio_dados,
        sep=";",
        encoding=encoding_correto,
        dtype=str,
    )

    # Identifica dinamicamente a primeira coluna (Região / UF)
    coluna_regiao_uf = df.columns[0]

    # Limpeza de linhas nulas e rodapés de notas do DATASUS
    df = df.dropna(subset=[coluna_regiao_uf])
    df = df[
        ~df[coluna_regiao_uf].str.contains(
            r"Fonte:|Notas:|Total|&|-", na=False
        )
    ]

    # Separação entre Região e Estado (UF)
    regiao_atual = None
    regioes = []
    ufs = []

    for item in df[coluna_regiao_uf]:
        item_limpo = str(item).replace('"', "").strip()
        if not item_limpo.startswith(".."):
            regiao_atual = item_limpo
            regioes.append(regiao_atual)
            ufs.append(None)
        else:
            regioes.append(regiao_atual)
            ufs.append(item_limpo.replace(".. ", ""))

    df["regiao"] = regioes
    df["uf"] = ufs

    # Mantém apenas as linhas com estados válidos
    df_uf = df.dropna(subset=["uf"]).copy()

    # Identificação das colunas de anos (2014 a 2026)
    colunas_anos = [str(ano) for ano in range(2014, 2027)]
    colunas_anos_presentes = [
        col for col in colunas_anos if col in df_uf.columns
    ]

    # Aplicação do Melt (Unpivot das colunas de ano para linhas)
    df_melted = pd.melt(
        df_uf,
        id_vars=["regiao", "uf"],
        value_vars=colunas_anos_presentes,
        var_name="ano",
        value_name="obitos",
    )

    # Tratamento numérico de valores
    df_melted["obitos"] = (
        pd.to_numeric(df_melted["obitos"], errors="coerce")
        .fillna(0)
        .astype(int)
    )
    df_melted["ano"] = df_melted["ano"].astype(int)

    # Ordenação dos registros
    df_melted = df_melted.sort_values(by=["regiao", "uf", "ano"]).reset_index(
        drop=True
    )

    # Salvando a base limpa final
    nome_saida = "mortalidade_causas_externas_x60_x84_tratado.csv"
    df_melted.to_csv(nome_saida, index=False, encoding="utf-8-sig")

    print("\nTratamento concluído com sucesso!")
    print(f"Arquivo gerado: {nome_saida}")
    print("\nPrimeiras 10 linhas da base tratada:")
    print(df_melted.head(10))


if __name__ == "__main__":
    arquivo_selecionado = selecionar_arquivo()
    processar_dados_datasus(arquivo_selecionado)