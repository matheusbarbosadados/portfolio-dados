# pdf_para_pdf_pesquisavel.py - transforma um PDF de imagem em um PDF pesquisável


import io
from pathlib import Path
from tkinter import Tk, filedialog

import pymupdf as fitz  # PyMuPDF
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def escolher_arquivos():
    janela = Tk()
    janela.withdraw()
    janela.attributes("-topmost", True)
    pdf = filedialog.askopenfilename(
        title="Escolha o PDF",
        filetypes=[("PDF", "*.pdf")],
    )
    if not pdf:
        janela.destroy()
        raise SystemExit("Nenhum PDF escolhido.")
    saida = filedialog.asksaveasfilename(
        title="Salvar o PDF pesquisável como",
        defaultextension=".pdf",
        initialfile=Path(pdf).stem + "_pesquisavel.pdf",
        filetypes=[("PDF", "*.pdf")],
    )
    janela.destroy()
    if not saida:
        raise SystemExit("Nenhum local escolhido.")
    return pdf, saida


PDF, SAIDA = escolher_arquivos()

doc = fitz.open(PDF)
novo = fitz.open()

for numero, pagina in enumerate(doc, start=1):
    print(f"Lendo página {numero} de {len(doc)}...")
    pix = pagina.get_pixmap(dpi=300)
    imagem = Image.open(io.BytesIO(pix.tobytes("png")))
    pdf_bytes = pytesseract.image_to_pdf_or_hocr(imagem, lang="por", extension="pdf")
    novo.insert_pdf(fitz.open("pdf", pdf_bytes))

novo.save(SAIDA)
print("Pronto! PDF salvo em:", SAIDA)