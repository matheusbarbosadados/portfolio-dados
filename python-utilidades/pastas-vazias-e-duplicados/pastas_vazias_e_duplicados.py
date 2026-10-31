import os
import stat
import hashlib
import tkinter as tk
from tkinter import filedialog

# ====== CONFIGURAÇÃO ======
ARQUIVO_VAZIAS = "pastas_vazias.txt"
ARQUIVO_DUPLICADOS = "arquivos_duplicados.txt"

# Pastas do sistema que serão ignoradas
PASTAS_SISTEMA = {
    "windows",
    "$recycle.bin",
    "system volume information",
    "program files",
    "program files (x86)",
    "programdata",
}
# ==========================


def escolher_pasta():
    """Abre a janela do Windows para escolher uma pasta."""
    janela = tk.Tk()
    janela.withdraw()
    janela.attributes("-topmost", True)
    caminho = filedialog.askdirectory(title="Escolha a pasta para analisar")
    janela.destroy()
    return os.path.normpath(caminho) if caminho else ""


def e_ignorada(entrada):
    """Retorna True se a pasta ou arquivo for do sistema ou oculto."""
    if entrada.name.lower() in PASTAS_SISTEMA:
        return True
    try:
        atributos = entrada.stat(follow_symlinks=False).st_file_attributes
        return bool(atributos & stat.FILE_ATTRIBUTE_HIDDEN)
    except OSError:
        return True


# ---------- PASTAS VAZIAS ----------

def encontrar_pastas_vazias(raiz):
    vazias = []
    avisos = []
    total_analisadas = 0

    def analisar(pasta):
        """Retorna True se a pasta estiver vazia."""
        nonlocal total_analisadas
        total_analisadas += 1

        try:
            with os.scandir(pasta) as itens:
                itens = list(itens)
        except OSError:
            avisos.append(f"Aviso: sem permissão ou erro ao ler: {pasta}")
            return False

        esta_vazia = True
        for item in itens:
            if item.is_dir(follow_symlinks=False):
                if e_ignorada(item):
                    esta_vazia = False
                elif analisar(item.path):
                    vazias.append(item.path)
                else:
                    esta_vazia = False
            else:
                esta_vazia = False
        return esta_vazia

    analisar(raiz)
    return sorted(vazias), total_analisadas, avisos


def listar_vazias(pasta):
    vazias, total, avisos = encontrar_pastas_vazias(pasta)

    print("\n--- PASTAS VAZIAS ---")
    for p in vazias:
        print(p)

    for aviso in avisos:
        print(aviso)

    with open(ARQUIVO_VAZIAS, "w", encoding="utf-8") as f:
        for p in vazias:
            f.write(p + "\n")

    print("\n--- RESUMO ---")
    print(f"Pastas analisadas: {total}")
    print(f"Pastas vazias: {len(vazias)}")
    print(f"Lista salva em: {ARQUIVO_VAZIAS}")


# ---------- ARQUIVOS DUPLICADOS ----------

def coletar_arquivos(raiz, avisos):
    """Retorna um dicionário: tamanho -> lista de arquivos."""
    por_tamanho = {}
    total = 0
    pendentes = [raiz]

    while pendentes:
        pasta = pendentes.pop()
        try:
            with os.scandir(pasta) as itens:
                itens = list(itens)
        except OSError:
            avisos.append(f"Aviso: sem permissão ou erro ao ler: {pasta}")
            continue

        for item in itens:
            if e_ignorada(item):
                continue
            if item.is_dir(follow_symlinks=False):
                pendentes.append(item.path)
            elif item.is_file(follow_symlinks=False):
                try:
                    tamanho = item.stat().st_size
                except OSError:
                    avisos.append(f"Aviso: não foi possível ler: {item.path}")
                    continue
                total += 1
                if tamanho > 0:  # ignora arquivos vazios
                    por_tamanho.setdefault(tamanho, []).append(item.path)

    return por_tamanho, total


def calcular_hash(caminho):
    """Retorna a 'impressão digital' do conteúdo do arquivo."""
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        while True:
            bloco = f.read(1024 * 1024)
            if not bloco:
                break
            h.update(bloco)
    return h.hexdigest()


def encontrar_duplicados(raiz):
    avisos = []
    por_tamanho, total = coletar_arquivos(raiz, avisos)

    grupos = []  # cada grupo: (tamanho, [caminhos])
    for tamanho, caminhos in por_tamanho.items():
        if len(caminhos) < 2:
            continue  # tamanho único: não pode ter cópia

        por_hash = {}
        for caminho in caminhos:
            try:
                por_hash.setdefault(calcular_hash(caminho), []).append(caminho)
            except OSError:
                avisos.append(f"Aviso: não foi possível ler: {caminho}")

        for lista in por_hash.values():
            if len(lista) > 1:
                grupos.append((tamanho, sorted(lista)))

    grupos.sort(key=lambda g: g[0] * (len(g[1]) - 1), reverse=True)
    return grupos, total, avisos


def listar_duplicados(pasta):
    print("\nAnalisando arquivos... pode levar um tempo em pastas grandes.")
    grupos, total, avisos = encontrar_duplicados(pasta)

    linhas = []
    espaco_extra = 0
    copias = 0
    for numero, (tamanho, caminhos) in enumerate(grupos, start=1):
        linhas.append(f"Grupo {numero} ({tamanho / 1024 / 1024:.2f} MB cada):")
        for c in caminhos:
            linhas.append(f"  {c}")
        linhas.append("")
        espaco_extra += tamanho * (len(caminhos) - 1)
        copias += len(caminhos) - 1

    print("\n--- ARQUIVOS DUPLICADOS ---")
    for linha in linhas:
        print(linha)

    for aviso in avisos:
        print(aviso)

    with open(ARQUIVO_DUPLICADOS, "w", encoding="utf-8") as f:
        for linha in linhas:
            f.write(linha + "\n")

    print("--- RESUMO ---")
    print(f"Arquivos analisados: {total}")
    print(f"Grupos de duplicados: {len(grupos)}")
    print(f"Cópias extras: {copias}")
    print(f"Espaço ocupado pelas cópias: {espaco_extra / 1024 / 1024:.2f} MB")
    print(f"Lista salva em: {ARQUIVO_DUPLICADOS}")


# ---------- MENU ----------

def menu():
    while True:
        print("\n===== MENU =====")
        print("1 - Listar pastas vazias")
        print("2 - Procurar arquivos duplicados")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("Encerrando.")
            break

        if opcao not in ("1", "2"):
            print("Opção inválida.")
            continue

        pasta = escolher_pasta()
        if not pasta:
            print("Nenhuma pasta escolhida. Voltando ao menu.")
            continue

        print(f"Pasta escolhida: {pasta}")
        if opcao == "1":
            listar_vazias(pasta)
        else:
            listar_duplicados(pasta)


menu()