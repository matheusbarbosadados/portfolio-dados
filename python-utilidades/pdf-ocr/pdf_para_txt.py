# pdf_para_txt.py - converte um PDF em um arquivo TXT

import io
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

# Caminho do Tesseract (local padrão da instalação)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Altere para o caminho do seu PDF e do arquivo de saída
PDF = r"C:\Users\MatheusWIN11\Downloads\index.pdf"
SAIDA = r"C:\Users\MatheusWIN11\Downloads\apostila.txt"

doc = fitz.open(PDF)
textos = []

for numero, pagina in enumerate(doc, start=1):
    print(f"Lendo página {numero} de {len(doc)}...")
    pix = pagina.get_pixmap(dpi=300)
    imagem = Image.open(io.BytesIO(pix.tobytes("png")))
    texto = pytesseract.image_to_string(imagem, lang="por")
    textos.append(f"--- Página {numero} ---\n{texto}")

with open(SAIDA, "w", encoding="utf-8") as arquivo:
    arquivo.write("\n\n".join(textos))

print("Pronto! Texto salvo em:", SAIDA)