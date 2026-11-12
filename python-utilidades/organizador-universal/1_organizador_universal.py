
from pathlib import Path
import shutil
import re
import os
import unicodedata
from tkinter import Tk, filedialog


# ==========================================
# CONFIGURAÇÕES
# ==========================================

EXTENSOES = {
    "Documentos": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"],
    "Planilhas": [".xls", ".xlsx", ".csv", ".ods"],
    "Apresentações": [".ppt", ".pptx", ".odp"],
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Vídeos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "Áudios": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Arquivos Compactados": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programas": [".exe", ".msi", ".bat", ".cmd", ".ps1"],
    "Ícones": [".ico"],
    "Power BI": [".pbix"],
    "Códigos": [".py", ".sql", ".html", ".css", ".js", ".json"]
}

PALAVRAS_CHAVE = {
    "Currículos": ["curriculo", "cv"],
    "Contratos": ["contrato", "acordo"],
    "Backups": ["backup", "copia_seguranca"],
    "Estudos": ["estudo", "estudos", "apostila", "curso", "cursos", "gabarito", "teste", "testes"],
    "Vagas": ["vaga", "vagas", "linkedin", "emprego"],
    "Projetos": ["projeto", "projetos"],
    "Financeiro": ["financeiro", "fatura", "boleto", "nf", "nota fiscal"]
}

PASTAS_DESTINO = (
    set(EXTENSOES.keys())
    | set(PALAVRAS_CHAVE.keys())
    | {"Não classificados"}
)


# ==========================================
# NORMALIZAÇÃO E CLASSIFICAÇÃO
# ==========================================

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)

    texto = "".join(
        caractere for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    texto = re.sub(r"[_\-.]+", " ", texto)
    texto = re.sub(r"[^\w\s]", " ", texto)

    return texto


def classificar_por_nome(nome_arquivo):
    nome = normalizar_texto(Path(nome_arquivo).stem)
    palavras_nome = set(nome.split())

    for categoria, palavras in PALAVRAS_CHAVE.items():
        for palavra in palavras:
            termos = normalizar_texto(palavra).split()

            if all(termo in palavras_nome for termo in termos):
                return categoria

    return None


def classificar_arquivo(arquivo):
    nome = normalizar_texto(arquivo.stem)
    extensao = arquivo.suffix.lower()

    # Regras específicas
    if "backup" in nome and extensao in [".sql", ".db", ".sqlite"]:
        return "Backups"

    if "financeiro" in nome and extensao in [".xlsx", ".xls", ".csv", ".pdf"]:
        return "Financeiro"

    if "curriculo" in nome and extensao in [".pdf", ".docx", ".doc"]:
        return "Currículos"

    # O nome tem prioridade sobre a extensão
    categoria = classificar_por_nome(arquivo.name)

    if categoria:
        return categoria

    # Classificação por extensão
    for categoria, extensoes in EXTENSOES.items():
        if extensao in extensoes:
            return categoria

    return "Não classificados"


# ==========================================
# SELEÇÃO DA PASTA
# ==========================================

print("ORGANIZADOR UNIVERSAL")

print(f"Categorias disponíveis: {len(PASTAS_DESTINO)}")

janela = Tk()
janela.withdraw()
janela.attributes("-topmost", True)

pasta_selecionada = filedialog.askdirectory(
    title="Selecione a pasta que deseja organizar"
)

janela.destroy()

if not pasta_selecionada:
    print("\nNenhuma pasta selecionada.")
    raise SystemExit

pasta_origem = Path(pasta_selecionada)

print(f"\nPasta selecionada: {pasta_origem}")


# ==========================================
# BUSCAR ARQUIVOS, INCLUSIVE EM SUBPASTAS
# ==========================================

arquivos_encontrados = []

for arquivo in pasta_origem.rglob("*"):
    if not arquivo.is_file():
        continue

    caminho_relativo = arquivo.relative_to(pasta_origem)

    # Não reprocessar arquivos já organizados
    if caminho_relativo.parts[0] in PASTAS_DESTINO:
        continue

    arquivos_encontrados.append(arquivo)


# ==========================================
# ANÁLISE DAS EXTENSÕES
# ==========================================

contagem = {}

for arquivo in arquivos_encontrados:
    extensao = arquivo.suffix.lower() or "Sem extensão"
    contagem[extensao] = contagem.get(extensao, 0) + 1

print("\n===== ANÁLISE DOS ARQUIVOS =====")

for extensao, quantidade in sorted(contagem.items()):
    print(f"{extensao}: {quantidade}")

print(f"\nTotal de arquivos: {len(arquivos_encontrados)}")


# ==========================================
# CLASSIFICAR ARQUIVOS
# ==========================================

arquivos_por_categoria = {}

for arquivo in arquivos_encontrados:
    categoria = classificar_arquivo(arquivo)

    if categoria not in arquivos_por_categoria:
        arquivos_por_categoria[categoria] = []

    caminho_relativo = arquivo.relative_to(pasta_origem)
    arquivos_por_categoria[categoria].append(caminho_relativo)


# ==========================================
# PRÉVIA DA ORGANIZAÇÃO
# ==========================================

print("\n===== PRÉVIA DA ORGANIZAÇÃO =====")

for categoria, arquivos in sorted(arquivos_por_categoria.items()):
    print(f"\n📁 {categoria}/")

    for caminho in sorted(arquivos):
        print(f"   {caminho} → {categoria}/{caminho.name}")


total_arquivos = sum(
    len(arquivos) for arquivos in arquivos_por_categoria.values()
)

print("\n===== RESUMO =====")
print(f"Pastas que seriam utilizadas: {len(arquivos_por_categoria)}")
print(f"Arquivos que seriam organizados: {total_arquivos}")


# ==========================================
# VERIFICAR CONFLITOS
# ==========================================

print("\n===== VERIFICAÇÃO DE CONFLITOS =====")

conflitos = []
destinos_planejados = set()

for categoria, arquivos in arquivos_por_categoria.items():
    pasta_destino = pasta_origem / categoria

    # Verificar se já existe um arquivo com o nome da pasta
    if pasta_destino.exists() and not pasta_destino.is_dir():
        conflitos.append(str(pasta_destino))
        continue

    for caminho in arquivos:
        destino = pasta_destino / caminho.name
        chave_destino = os.path.normcase(str(destino))

        if destino.exists():
            conflitos.append(str(destino))

        if chave_destino in destinos_planejados:
            conflitos.append(str(destino))

        destinos_planejados.add(chave_destino)


if conflitos:
    print(f"Conflitos encontrados: {len(set(conflitos))}")

    for conflito in sorted(set(conflitos)):
        print(f"Já existe ou está duplicado: {conflito}")

else:
    print("Nenhum conflito encontrado!")


# ==========================================
# CONFIRMAR E MOVIMENTAR
# ==========================================

if not arquivos_encontrados:
    print("\nNenhum arquivo novo encontrado para organizar.")

elif conflitos:
    print("\nMovimentação cancelada devido a conflitos.")

else:
    resposta = input(
        "\nDeseja organizar os arquivos agora? (S/N): "
    ).strip().upper()

    if resposta in ("S", "SIM"):
        total_movidos = 0

        try:
            for categoria, arquivos in arquivos_por_categoria.items():
                pasta_destino = pasta_origem / categoria
                pasta_destino.mkdir(parents=True, exist_ok=True)

                for caminho in arquivos:
                    origem = pasta_origem / caminho
                    destino = pasta_destino / caminho.name

                    shutil.move(str(origem), str(destino))
                    total_movidos += 1

            print("\n===== RESULTADO FINAL =====")
            print("Organização concluída!")
            print(f"Arquivos movidos: {total_movidos}")
            print(
                f"Arquivos não classificados: "
                f"{len(arquivos_por_categoria.get('Não classificados', []))}"
            )

        except OSError as erro:
            print("\nERRO DURANTE A MOVIMENTAÇÃO!")
            print(f"Arquivos movidos antes do erro: {total_movidos}")
            print(f"Detalhes: {erro}")

    else:
        print("\nOrganização cancelada. Nenhum arquivo foi movido.")
