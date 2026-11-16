import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import time
from rembg import remove, new_session
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np

PASTA = Path(__file__).parent
SAIDA = PASTA / "resultado"
SAIDA.mkdir(exist_ok=True)
SESSAO = new_session("u2net_human_seg")

# Ajustes simples (pode mudar depois)
LUZ_ESQUERDA = 1.15    # luz no lado esquerdo da pessoa (acima de 1 clareia)
LUZ_DIREITA = 0.55     # luz no lado direito (abaixo de 1 escurece)
BRILHO_GERAL = 0.95    # brilho total da pessoa (1.0 = igual)
CONTRASTE = 1.15       # contraste da pessoa (1.0 = igual)
BRILHO_FUNDO = 45      # força do brilho no fundo (0 = fundo todo preto)
SUAVIZAR_BORDA = 2     # suaviza o recorte (0 = sem suavizar)


def escolher_fotos():
    """Abre a janela para escolher as fotos com o mouse."""
    raiz = tk.Tk()
    raiz.withdraw()
    raiz.attributes("-topmost", True)
    arquivos = filedialog.askopenfilenames(
        title="Escolha as fotos",
        filetypes=[("Imagens", "*.jpg *.jpeg *.png")],
    )
    raiz.destroy()
    return [Path(a) for a in arquivos]


def criar_fundo(largura, altura):
    """Fundo preto com um brilho suave, do lado oposto à luz."""
    y, x = np.ogrid[:altura, :largura]
    cx, cy = largura * 0.62, altura * 0.40
    dist = np.sqrt(((x - cx) / largura) ** 2 + ((y - cy) / altura) ** 2)
    brilho = np.clip(1 - dist * 1.8, 0, 1) ** 2
    cinza = (brilho * BRILHO_FUNDO).astype(np.uint8)
    fundo = np.stack([cinza] * 3, axis=-1)
    return Image.fromarray(fundo, "RGB").convert("RGBA")


def ajustar_pessoa(pessoa):
    """Simula luz vinda da esquerda e suaviza a borda do recorte."""
    alfa = pessoa.split()[3]
    x0, _, x1, _ = alfa.getbbox()

    rgb = np.array(pessoa.convert("RGB"), dtype=np.float32)
    largura = rgb.shape[1]
    posicao = np.clip((np.arange(largura) - x0) / max(x1 - x0, 1), 0, 1)
    gradiente = LUZ_ESQUERDA + (LUZ_DIREITA - LUZ_ESQUERDA) * posicao
    rgb = rgb * gradiente[None, :, None] * BRILHO_GERAL
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)

    img = ImageEnhance.Contrast(Image.fromarray(rgb)).enhance(CONTRASTE)

    # Tira o contorno do fundo antigo e suaviza a borda
    alfa = alfa.filter(ImageFilter.MinFilter(3))
    if SUAVIZAR_BORDA > 0:
        alfa = alfa.filter(ImageFilter.GaussianBlur(SUAVIZAR_BORDA / 2))

    return Image.merge("RGBA", (*img.split(), alfa))


def processar(caminho):
    foto = Image.open(caminho)
    inicio = time.time()
    foto = ImageOps.exif_transpose(foto).convert("RGB")
    foto.thumbnail((1600, 1600))

    pessoa = ajustar_pessoa(remove(foto, session=SESSAO))

    resultado = criar_fundo(*pessoa.size)
    resultado.alpha_composite(pessoa)

    destino = SAIDA / (caminho.stem + "_estudio_v2.png")
    resultado.convert("RGB").save(destino)
    print("Pronto:", destino.name, "-", round(time.time() - inicio), "segundos")


arquivos = escolher_fotos()

if not arquivos:
    print("Nenhuma foto escolhida.")

for arquivo in arquivos:
    processar(arquivo)

print("Finalizado.")