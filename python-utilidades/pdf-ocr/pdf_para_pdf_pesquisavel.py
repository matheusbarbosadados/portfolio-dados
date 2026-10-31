# pdf_para_pdf_pesquisavel.py - transforma um PDF de imagem em um PDF pesquisável


import io
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Altere para o caminho do seu PDF e do arquivo de saída
PDF = r"entrada.pdf"
SAIDA = r"pdf_pesquisavel.pdf"

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