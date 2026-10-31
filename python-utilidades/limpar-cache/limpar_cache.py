import os
import subprocess

os.system("cls")

LOCAL = os.environ["LOCALAPPDATA"]
ROAMING = os.environ["APPDATA"]
CHROME = os.path.join(LOCAL, "Google", "Chrome", "User Data", "Default")
CODE = os.path.join(ROAMING, "Code")

# (nome, pasta, prefixo do arquivo ou None para todos)
ALVOS = [
    ("Temp do usuário", os.environ["TEMP"], None),
    ("Temp do Windows", r"C:\Windows\Temp", None),
    ("pip - cache", os.path.join(LOCAL, "pip", "cache"), None),
    ("Chrome - Cache", os.path.join(CHROME, "Cache"), None),
    ("Chrome - Code Cache", os.path.join(CHROME, "Code Cache"), None),
    ("Chrome - GPUCache", os.path.join(CHROME, "GPUCache"), None),
    ("VS Code - Cache", os.path.join(CODE, "Cache"), None),
    ("VS Code - CachedData", os.path.join(CODE, "CachedData"), None),
    ("VS Code - VSIX baixados", os.path.join(CODE, "CachedExtensionVSIXs"), None),
    ("VS Code - Code Cache", os.path.join(CODE, "Code Cache"), None),
    ("VS Code - GPUCache", os.path.join(CODE, "GPUCache"), None),
    ("VS Code - Crashpad", os.path.join(CODE, "Crashpad"), None),
    ("Notion - Cache", os.path.join(ROAMING, "Notion", "Partitions", "notion", "Cache"), None),
    ("Relatórios de falhas", os.path.join(LOCAL, "CrashDumps"), None),
    ("Miniaturas do Explorer", os.path.join(LOCAL, "Microsoft", "Windows", "Explorer"), "thumbcache_"),
]

PROGRAMAS = ["chrome.exe", "Code.exe", "Notion.exe"]


def mb(bytes_):
    return round(bytes_ / 1024 / 1024, 1)


def coletar(pasta, prefixo):
    arquivos = []
    for raiz, _, nomes in os.walk(pasta):
        for nome in nomes:
            if prefixo and not (nome.startswith(prefixo) and nome.endswith(".db")):
                continue
            caminho = os.path.join(raiz, nome)
            if os.path.islink(caminho):
                continue
            try:
                arquivos.append((caminho, os.path.getsize(caminho)))
            except OSError:
                pass
    return arquivos


def programas_abertos():
    saida = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
    return [p for p in PROGRAMAS if p.lower() in saida]


def fazer_backup():
    destino = os.path.join(os.environ["USERPROFILE"], "OneDrive", "Backup_C")
    pastas = [r"C:\Projetos"]  # Altere para as pastas que você quer copiar
    print("Fazendo backup para o OneDrive...\n")
    for pasta in pastas:
        if not os.path.isdir(pasta):
            print(f"Pasta não encontrada, pulando: {pasta}")
            continue
        nome = os.path.basename(pasta)
        resultado = subprocess.run(
            ["robocopy", pasta, os.path.join(destino, nome), "/E",
             "/XD", ".venv", "venv", "__pycache__", "/NFL", "/NDL", "/NJH", "/NJS", "/NP"]
        )
        # Códigos de 0 a 7 são sucesso; a partir de 8 houve erro
        if resultado.returncode >= 8:
            print(f"ERRO ao copiar {pasta}")
    print("\nBackup concluído.\n")


# 0. Backup
fazer_backup()


# 1. Simulação
print("SIMULAÇÃO (nada foi apagado ainda)\n")


plano = []
total = 0
for nome, pasta, prefixo in ALVOS:
    if not os.path.isdir(pasta):
        print(f"{nome:28} não encontrada")
        continue
    arquivos = coletar(pasta, prefixo)
    tamanho = sum(t for _, t in arquivos)
    total += tamanho
    plano.append((nome, pasta, prefixo, arquivos))
    print(f"{nome:28} {mb(tamanho):>8} MB")

print(f"\nTotal que pode ser liberado: {mb(total)} MB")

abertos = programas_abertos()
if abertos:
    print("\nATENÇÃO: feche antes de apagar:", ", ".join(abertos))

# 2. Confirmação
resposta = input("\nDigite SIM para apagar (qualquer outra coisa cancela): ")
if resposta.strip() != "SIM":
    print("Cancelado. Nada foi apagado.")
    raise SystemExit

# 3. Limpeza
liberado = 0
pulados = 0
for nome, pasta, prefixo, arquivos in plano:
    for caminho, tamanho in arquivos:
        try:
            os.remove(caminho)
            liberado += tamanho
        except OSError:
            pulados += 1
    if prefixo is None:
        for raiz, pastas, _ in os.walk(pasta, topdown=False):
            for p in pastas:
                try:
                    os.rmdir(os.path.join(raiz, p))
                except OSError:
                    pass

print(f"\nLiberado: {mb(liberado)} MB")
print(f"Arquivos pulados (em uso ou sem permissão): {pulados}")