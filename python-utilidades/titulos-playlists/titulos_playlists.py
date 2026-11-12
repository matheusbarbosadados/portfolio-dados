import re
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import yt_dlp

# ---------------------------------------------------------
# CONFIGURAÇÃO
# ---------------------------------------------------------
# Os resultados são salvos na pasta Resultados,
# ao lado deste script.

PASTA = Path(__file__).parent
PASTA_RESULTADOS = PASTA / "Resultados"
PREFIXO = "Titulos - "

# ---------------------------------------------------------
# FUNÇÕES
# ---------------------------------------------------------


def extrair_links(texto):
    """Pega os links do texto (um por linha). Linhas com # são ignoradas."""
    links = []
    for linha in texto.splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#"):
            links.append(linha)
    return links


def escolher_arquivo():
    """Abre a janelinha para escolher um .txt com links. Devolve o caminho ou vazio."""
    janela = tk.Tk()
    janela.withdraw()
    janela.attributes("-topmost", True)
    caminho = filedialog.askopenfilename(
        title="Escolha o .txt com os links (ou cancele para colar no terminal)",
        initialdir=str(PASTA),
        filetypes=[("Arquivos de texto", "*.txt")],
    )
    janela.destroy()
    return caminho


def pedir_links_no_terminal():
    """Pede os links no terminal. Linha vazia termina."""
    print("Cole os links das playlists, um por linha.")
    print("Quando terminar, aperte Enter em uma linha vazia.")
    linhas = []
    while True:
        linha = input("> ").strip()
        if not linha:
            break
        linhas.append(linha)
    return extrair_links("\n".join(linhas))


def obter_links():
    """Escolhe o .txt, ou, se cancelar, pede os links no terminal."""
    caminho = escolher_arquivo()
    if caminho:
        texto = Path(caminho).read_text(encoding="utf-8-sig")
        return extrair_links(texto)
    return pedir_links_no_terminal()


def ler_titulos(link):
    """Lê a playlist sem baixar nada. Devolve o nome da playlist e os títulos."""
    opcoes = {
        "extract_flat": "in_playlist",
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
        "http_headers": {"Accept-Language": "pt-BR,pt;q=0.9"},
        "extractor_args": {"youtube": {"lang": ["pt"]}},
    }
    with yt_dlp.YoutubeDL(opcoes) as ydl:
        info = ydl.extract_info(link, download=False)

    nome_playlist = info.get("title") or ""
    titulos = []
    for entrada in info.get("entries") or []:
        if entrada:
            titulos.append(entrada.get("title") or "(sem título)")
    return nome_playlist, titulos


def limpar_nome(nome):
    """Tira caracteres que o Windows não aceita em nomes de arquivo."""
    nome = re.sub(r'[\\/:*?"<>|]', "", nome)
    return nome.strip().rstrip(".")


def salvar_txt(caminho, titulos):
    """Salva um título por linha: número e título."""
    with open(caminho, "w", encoding="utf-8") as arquivo:
        for numero, titulo in enumerate(titulos, start=1):
            arquivo.write(f"{numero:02d} - {titulo}\n")


def main():
    links = obter_links()
    if not links:
        raise SystemExit("Nenhum link informado.")

    PASTA_RESULTADOS.mkdir(exist_ok=True)

    nomes_usados = set()
    resumo = []

    for posicao, link in enumerate(links, start=1):
        print(f"Lendo playlist {posicao} de {len(links)}...")

        try:
            nome_playlist, titulos = ler_titulos(link)
            if not titulos:
                print("  ERRO: nenhum vídeo encontrado.")
                resumo.append((link, "falhou"))
                continue

            nome = limpar_nome(nome_playlist) or f"playlist_{posicao:02d}"
            base = PREFIXO + nome
            nome_final = base
            contador = 2
            while nome_final in nomes_usados:
                nome_final = f"{base}_{contador}"
                contador += 1
            nomes_usados.add(nome_final)

            caminho = PASTA_RESULTADOS / f"{nome_final}.txt"
            salvar_txt(caminho, titulos)
            print(f"  OK: {len(titulos)} vídeos salvos em {caminho.name}")
            resumo.append((nome_final, len(titulos)))

        except Exception as erro:
            print(f"  ERRO: {erro}")
            resumo.append((link, "falhou"))

    print("\n--- RESUMO ---")
    for nome, resultado in resumo:
        if resultado == "falhou":
            print(f"{nome}: falhou")
        else:
            print(f"{nome}: {resultado} vídeos")


main()