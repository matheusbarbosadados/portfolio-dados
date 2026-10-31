from pathlib import Path

import yt_dlp

# ---------------------------------------------------------
# CONFIGURAÇÃO (altere apenas esta parte)
# ---------------------------------------------------------

# Pasta onde os arquivos .txt serão salvos (será criada se não existir)
PASTA_SAIDA = r"playlists_txt"

# Lista de playlists: (nome do arquivo, link da playlist)
PLAYLISTS = [
    # ("mundo_1", "https://www.youtube.com/watch?v=S9uPNppGsGo&list=PLHz_AreHm4dlKP6QQCekuIPky1CiwmdI6"),
    ("mundo_2", "https://www.youtube.com/watch?v=nJkVHusJp6E&list=PLHz_AreHm4dk_nZHmxxf_J0WRAqy5Czye"),
    ("mundo_3", "https://www.youtube.com/watch?v=0LB3FSfjvao&list=PLHz_AreHm4dksnH2jVTIVNviIMBVYyFnH"),
    ("mundo_4", "https://www.youtube.com/watch?v=Mim6nnkdOto&list=PLHz_AreHm4dn_RXXoa3Ameh77f95Hgwv3"),
]

# ---------------------------------------------------------
# FUNÇÕES
# ---------------------------------------------------------


def ler_titulos(link):
    """Lê a playlist sem baixar nada e devolve a lista de títulos."""
    opcoes = {
        "extract_flat": "in_playlist",  # apenas lê a lista
        "skip_download": True,          # garante que nada será baixado
        "quiet": True,
        "no_warnings": True,
        # Pede os títulos em português do Brasil
        "http_headers": {"Accept-Language": "pt-BR,pt;q=0.9"},
        "extractor_args": {"youtube": {"lang": ["pt"]}},
    }
    with yt_dlp.YoutubeDL(opcoes) as ydl:
        info = ydl.extract_info(link, download=False)

    entradas = info.get("entries") or []
    titulos = []
    for entrada in entradas:
        if entrada:
            titulos.append(entrada.get("title") or "(sem título)")
    return titulos


def salvar_txt(caminho, titulos):
    """Salva um título por linha: número e título, sem alterar o texto."""
    with open(caminho, "w", encoding="utf-8") as arquivo:
        for numero, titulo in enumerate(titulos, start=1):
            arquivo.write(f"{numero:02d} - {titulo}\n")


def main():
    pasta = Path(PASTA_SAIDA)
    pasta.mkdir(parents=True, exist_ok=True)

    resumo = []

    for nome, link in PLAYLISTS:
        print(f"Lendo {nome}...")

        if link.startswith("COLE_AQUI"):
            print(f"  ERRO: coloque o link de {nome} na lista PLAYLISTS.")
            resumo.append((nome, "falhou"))
            continue

        try:
            titulos = ler_titulos(link)
            if not titulos:
                print(f"  ERRO: nenhum vídeo encontrado em {nome}.")
                resumo.append((nome, "falhou"))
                continue

            caminho = pasta / f"{nome}.txt"
            salvar_txt(caminho, titulos)
            print(f"  OK: {len(titulos)} vídeos salvos em {caminho}")
            resumo.append((nome, len(titulos)))

        except Exception as erro:
            print(f"  ERRO em {nome}: {erro}")
            resumo.append((nome, "falhou"))

    print("\n--- RESUMO ---")
    for nome, resultado in resumo:
        if resultado == "falhou":
            print(f"{nome}: falhou")
        else:
            print(f"{nome}: {resultado} vídeos")


main()