# pdf_para_txt_lotes.py - converte vários PDFs de uma pasta em arquivos TXT

import io
from pathlib import Path
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Altere para as suas pastas
PASTA_PDFS = Path("pdfs")
PASTA_SAIDA = Path("textos")
PASTA_SAIDA.mkdir(exist_ok=True)


def pdf_para_txt(caminho_pdf, caminho_txt):
    doc = fitz.open(caminho_pdf)
    textos = []

    for numero, pagina in enumerate(doc, start=1):
        print(f"  Página {numero} de {len(doc)}...")
        pix = pagina.get_pixmap(dpi=300)
        imagem = Image.open(io.BytesIO(pix.tobytes("png")))
        texto = pytesseract.image_to_string(imagem, lang="por")
        textos.append(f"--- Página {numero} ---\n{texto}")

    caminho_txt.write_text("\n\n".join(textos), encoding="utf-8")


arquivos = sorted(PASTA_PDFS.glob("*.pdf"))
print(f"{len(arquivos)} PDF(s) encontrado(s).")

for i, pdf in enumerate(arquivos, start=1):
    saida = PASTA_SAIDA / (pdf.stem + ".txt")

    if saida.exists():
        print(f"[{i}/{len(arquivos)}] {pdf.name}: já existe, pulando.")
        continue

    print(f"[{i}/{len(arquivos)}] {pdf.name}")
    try:
        pdf_para_txt(pdf, saida)
    except Exception as erro:
        print(f"  Erro em {pdf.name}: {erro}")

print("Pronto! Textos salvos em:", PASTA_SAIDA)