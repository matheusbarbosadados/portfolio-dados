import os
import shutil
import subprocess
import time
from tkinter import Tk, filedialog

# ---------------- CONFIGURAÇÕES ----------------
SUFIXO_SAIDA = "_corte"  # Nome que vai no final do arquivo novo
MODO_PADRAO = "1"  # 1 = rápido (sem perder qualidade), 2 = preciso (corte exato)

# Formatos de tempo: nome -> (descrição, exemplo, partes separadas por ":")
FORMATO_MINUTOS = ("Minutos e segundos", "5:01", 2)
FORMATO_SEGUNDOS = ("Só segundos", "301", 1)
FORMATO_HORAS = ("Horas, minutos e segundos", "1:01:00", 3)

# ---------------- SOM FINAL (OPCIONAL) ----------------
try:
    import sons
except ImportError:
    sons = None


class SairDoPrograma(Exception):
    """Usada quando o usuário escolhe sair em algum menu."""


def avisar_fim():
    """Toca o aviso sonoro, se o sons.py estiver na mesma pasta."""
    if sons is not None and hasattr(sons, "avisar"):
        try:
            sons.avisar()
        except Exception:
            pass


# ---------------- FUNÇÕES ----------------
def achar_ffmpeg():
    """Procura o FFmpeg instalado ou o do imageio-ffmpeg."""
    caminho = shutil.which("ffmpeg")
    if caminho:
        return caminho
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return None


def escolher_video():
    """Abre a janela do Windows para escolher o vídeo."""
    janela = Tk()
    janela.withdraw()
    janela.attributes("-topmost", True)
    caminho = filedialog.askopenfilename(
        title="Escolha o vídeo",
        filetypes=[
            ("Vídeos", "*.mp4 *.mkv *.avi *.mov *.webm *.flv *.wmv"),
            ("Todos os arquivos", "*.*"),
        ],
    )
    janela.destroy()
    return caminho


def ler_tempo(texto):
    """Converte 301, 5:01 ou 1:05:01 em segundos."""
    segundos = 0
    for parte in texto.split(":"):
        segundos = segundos * 60 + float(parte)
    return segundos


def escolher_outro_formato():
    """Submenu: segundos ou horas. Devolve o formato ou None para voltar."""
    print("\nOutros formatos:")
    print(f"1 - {FORMATO_SEGUNDOS[0]} (exemplo: {FORMATO_SEGUNDOS[1]})")
    print(f"2 - {FORMATO_HORAS[0]} (exemplo: {FORMATO_HORAS[1]})")
    print("0 - Voltar")
    while True:
        escolha = input("Escolha: ").strip()
        if escolha == "1":
            return FORMATO_SEGUNDOS
        if escolha == "2":
            return FORMATO_HORAS
        if escolha == "0":
            return None
        print("Opção inválida.")


def digitar_tempo(nome, formato):
    """Pede o tempo no formato escolhido e devolve em segundos."""
    _, exemplo, partes = formato
    while True:
        texto = input(f"{nome} (exemplo: {exemplo}): ").strip()
        if len(texto.split(":")) != partes:
            print(f"ERRO: use o formato escolhido (exemplo: {exemplo}).")
            continue
        try:
            return ler_tempo(texto)
        except ValueError:
            print(f"ERRO: tempo inválido (exemplo: {exemplo}).")


def pedir_ponto(nome, texto_enter):
    """Mostra o menu e devolve o tempo em segundos, ou None se apertar Enter."""
    while True:
        print(f"\n{nome} do corte:")
        print(f"1 - {FORMATO_MINUTOS[0]} (exemplo: {FORMATO_MINUTOS[1]})")
        print("2 - Outros formatos (segundos ou horas)")
        print("3 - Sair")
        print(f"Enter (sem escolher nada) - {texto_enter}")
        escolha = input("Escolha: ").strip()

        if escolha == "":
            return None
        if escolha == "1":
            return digitar_tempo(nome, FORMATO_MINUTOS)
        if escolha == "2":
            formato = escolher_outro_formato()
            if formato is not None:
                return digitar_tempo(nome, formato)
            continue
        if escolha == "3":
            raise SairDoPrograma
        print("Opção inválida.")


def formatar_tempo(segundos):
    """Mostra o tempo no formato 'X min Y s'."""
    minutos = int(segundos // 60)
    return f"{minutos} min {int(segundos % 60)} s"


def nome_de_saida(video):
    """Cria um nome novo que não existe ainda, para nunca sobrescrever."""
    pasta, nome = os.path.split(video)
    base, extensao = os.path.splitext(nome)
    saida = os.path.join(pasta, f"{base}{SUFIXO_SAIDA}{extensao}")
    contador = 2
    while os.path.exists(saida):
        saida = os.path.join(pasta, f"{base}{SUFIXO_SAIDA}{contador}{extensao}")
        contador += 1
    return saida


def montar_comando(ffmpeg, video, saida, inicio, fim, modo):
    """Monta o comando do FFmpeg conforme o modo escolhido."""
    comando = [ffmpeg, "-y"]
    if modo == "1":
        if inicio is not None:
            comando += ["-ss", str(inicio)]
        comando += ["-i", video]
        if fim is not None:
            comando += ["-t", str(fim - (inicio or 0))]
        comando += ["-c", "copy"]
    else:
        comando += ["-i", video]
        if inicio is not None:
            comando += ["-ss", str(inicio)]
        if fim is not None:
            comando += ["-to", str(fim)]
        comando += ["-c:v", "libx264", "-c:a", "aac"]
    comando.append(saida)
    return comando


# ---------------- FLUXO PRINCIPAL ----------------
def main():
    inicio_execucao = time.perf_counter()
    try:
        ffmpeg = achar_ffmpeg()
        if not ffmpeg:
            print("Falta instalar o FFmpeg. No terminal, digite: pip install imageio-ffmpeg")
            return

        # Etapa 0: escolher o vídeo
        print("Escolha o vídeo na janela que vai abrir...")
        video = escolher_video()
        if not video:
            print("Nenhum vídeo escolhido. Encerrando.")
            return
        print(f"Vídeo: {video}")

        # Etapa 1: pedir início e fim
        inicio = pedir_ponto("Início", "Começar do início do vídeo")
        fim = pedir_ponto("Fim", "Ir até o final do vídeo")

        if inicio is None and fim is None:
            print("Nada para cortar: informe pelo menos o início ou o fim.")
            return
        if inicio is not None and fim is not None and fim <= inicio:
            print("ERRO: o fim precisa ser maior que o início.")
            return

        # Etapa 2: escolher o modo
        print("\n1 - Rápido (sem perder qualidade, o corte pode variar alguns segundos)")
        print("2 - Preciso (corte exato, demora mais)")
        modo = input(f"Escolha 1 ou 2 (vazio = {MODO_PADRAO}): ").strip() or MODO_PADRAO
        if modo not in ("1", "2"):
            print("Opção inválida.")
            return

        # Etapa 3: cortar
        saida = nome_de_saida(video)
        comando = montar_comando(ffmpeg, video, saida, inicio, fim, modo)
        print("\nCortando...")
        resultado = subprocess.run(comando, capture_output=True, text=True)

        if resultado.returncode == 0:
            print(f"OK: arquivo criado: {saida}")
        else:
            print("ERRO: o FFmpeg não conseguiu cortar.")
            print(resultado.stderr[-500:])
    except SairDoPrograma:
        print("Programa encerrado.")
    finally:
        total = time.perf_counter() - inicio_execucao
        print(f"\nTempo total de execução: {formatar_tempo(total)}")
        avisar_fim()


if __name__ == "__main__":
    main()