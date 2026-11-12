# pdf_para_txt_lotes.py - converte vários PDFs de uma pasta em arquivos TXT

import io
import unicodedata
from pathlib import Path
from tkinter import Tk, filedialog

import pymupdf as fitz 
import pytesseract
from PIL import Image

# Caminho do Tesseract (local padrão da instalação)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Páginas com menos caracteres que isso são tratadas como imagem e passam por OCR
MIN_CARACTERES = 50

# Parte da altura da página (0.08 = 8%) onde ficam cabeçalho e rodapé, que são ignorados
MARGEM_TOPO = 0.08
MARGEM_BASE = 0.06

# No OCR, palavras com confiança abaixo disso (0 a 100) são descartadas
CONFIANCA_MINIMA = 60

# Se a página inteira tiver menos letras que isso depois da limpeza, é tratada como vazia
MIN_LETRAS_PAGINA = 15

FIM_DE_FRASE = (".", ":", ";", "!", "?", "”", '"')


def escolher_pasta(titulo):
    janela = Tk()
    janela.withdraw()
    janela.attributes("-topmost", True)
    pasta = filedialog.askdirectory(title=titulo)
    janela.destroy()
    if not pasta:
        raise SystemExit("Nenhuma pasta escolhida.")
    return Path(pasta)


def limpar_caracteres(texto):
    """Troca ligaduras (ﬁ vira fi) e hífen invisível por hífen comum."""
    texto = unicodedata.normalize("NFKC", texto)
    return texto.replace("\u00ad", "-")


def e_marcador(caractere):
    """Marcador de lista: caractere especial do PDF ou bolinha comum."""
    return unicodedata.category(caractere) in ("Co", "Cc") or caractere in "•▪■●◦"


def url_aberta(texto):
    """True se o texto termina no meio de um endereço de internet (continua na linha seguinte)."""
    palavras = texto.split()
    if not palavras:
        return False
    ultima = palavras[-1]
    comeca_url = ultima.lower().lstrip("<(").startswith(("http", "www"))
    return comeca_url and ">" not in ultima and ultima.endswith(("/", ".", "-"))


def juntar_linhas(linhas):
    """Junta várias linhas em um texto corrido, refazendo palavras cortadas com hífen."""
    texto = ""
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
        if not texto:
            texto = linha
        elif url_aberta(texto):
            texto += linha
        elif texto.endswith("-") and linha[0].islower():
            texto = texto[:-1] + linha
        else:
            texto += " " + linha
    return texto


def continua(anterior, texto):
    """True se 'texto' é a continuação da frase que ficou aberta em 'anterior'."""
    if not anterior:
        return False
    if anterior.isupper() and texto.isupper() and len(anterior) < 60:
        return True  # título em maiúsculas dividido em duas linhas
    return texto[:1].islower() and not anterior.endswith(FIM_DE_FRASE)


def adicionar(paragrafos, linhas, item, colar=False):
    """Fecha um trecho de linhas e coloca na lista, colando na frase anterior se for continuação."""
    texto = juntar_linhas(linhas)
    if not texto:
        return
    if paragrafos and not item and (colar or continua(paragrafos[-1], texto)):
        paragrafos[-1] = juntar_linhas([paragrafos[-1], texto])
    else:
        paragrafos.append(texto)


def paragrafos_do_pdf(pagina):
    """Lê o texto do próprio PDF, bloco por bloco, ignorando cabeçalho e rodapé."""
    altura = pagina.rect.height
    paragrafos = []
    x_item = None  # posição horizontal do último item de lista
    for bloco in pagina.get_text("blocks", sort=True):
        x0, y0, y1, texto, tipo = bloco[0], bloco[1], bloco[3], bloco[4], bloco[6]
        if tipo != 0:
            continue
        if y1 < altura * MARGEM_TOPO or y0 > altura * (1 - MARGEM_BASE):
            continue
        # Texto recuado logo depois de um item da lista continua o mesmo item
        colar = (
            bool(paragrafos)
            and paragrafos[-1].startswith("- ")
            and x_item is not None
            and x0 >= x_item - 1
        )
        atual, item = [], False
        for linha in limpar_caracteres(texto).split("\n"):
            linha = linha.strip()
            if len(linha) == 1 and e_marcador(linha):
                continue
            if linha and e_marcador(linha[0]):
                adicionar(paragrafos, atual, item, colar)
                colar = False
                atual, item = ["- " + linha[1:].strip()], True
                x_item = x0
            else:
                atual.append(linha)
        adicionar(paragrafos, atual, item, colar)
    return paragrafos


def paragrafos_do_ocr(pagina):
    """Faz OCR da página e descarta palavras que o Tesseract não leu com confiança."""
    pix = pagina.get_pixmap(dpi=300)
    imagem = Image.open(io.BytesIO(pix.tobytes("png")))
    dados = pytesseract.image_to_data(
        imagem, lang="por", output_type=pytesseract.Output.DICT
    )

    blocos = {}
    for i, palavra in enumerate(dados["text"]):
        if not palavra.strip() or float(dados["conf"][i]) < CONFIANCA_MINIMA:
            continue
        chave = (dados["block_num"][i], dados["par_num"][i])
        linhas = blocos.setdefault(chave, {})
        linhas.setdefault(dados["line_num"][i], []).append(palavra)

    paragrafos = []
    for linhas in blocos.values():
        textos = [limpar_caracteres(" ".join(p)) for p in linhas.values()]
        adicionar(paragrafos, textos, False)
    return paragrafos


def pagina_vazia(paragrafos):
    letras = sum(c.isalpha() for p in paragrafos for c in p)
    return letras < MIN_LETRAS_PAGINA


def montar_txt(paginas):
    """Monta o texto final. Frases cortadas na virada de página são unidas."""
    validas = []
    for numero, paragrafos in paginas:
        if pagina_vazia(paragrafos):
            continue
        if validas and continua(validas[-1][1][-1], paragrafos[0]):
            validas[-1][1][-1] = juntar_linhas([validas[-1][1][-1], paragrafos[0]])
            paragrafos = paragrafos[1:]
        if paragrafos:
            validas.append((numero, paragrafos))
    return "\n\n".join(
        f"--- Página {numero} ---\n\n" + "\n\n".join(paragrafos)
        for numero, paragrafos in validas
    )


def pdf_para_txt(caminho_pdf, caminho_txt):
    """Converte um PDF. Devolve False se o PDF tem senha, True se deu certo."""
    doc = fitz.open(caminho_pdf)
    if doc.needs_pass:
        doc.close()
        return False

    total = len(doc)
    paginas = []

    for numero, pagina in enumerate(doc, start=1):
        if len(pagina.get_text().strip()) >= MIN_CARACTERES:
            print(f"  Página {numero} de {total}: texto do próprio PDF")
            paginas.append((numero, paragrafos_do_pdf(pagina)))
        else:
            print(f"  Página {numero} de {total}: OCR...")
            try:
                paginas.append((numero, paragrafos_do_ocr(pagina)))
            except pytesseract.TesseractNotFoundError:
                raise SystemExit(
                    "Tesseract não encontrado em C:\\Program Files\\Tesseract-OCR. "
                    "Instale o programa ou corrija o caminho no começo do script."
                )
            except Exception as erro:
                print(f"    Erro no OCR: {erro}")
                paginas.append((numero, ["[ERRO NO OCR DESTA PÁGINA]"]))

    doc.close()
    caminho_txt.write_text(montar_txt(paginas), encoding="utf-8")
    return True


PASTA_PDFS = escolher_pasta("Escolha a pasta com os PDFs")
PASTA_SAIDA = escolher_pasta("Escolha a pasta para salvar os TXTs")

arquivos = sorted(PASTA_PDFS.glob("*.pdf"))
print(f"{len(arquivos)} PDF(s) encontrado(s).")

convertidos = 0
pulados = 0
com_erro = 0

for i, pdf in enumerate(arquivos, start=1):
    saida = PASTA_SAIDA / (pdf.stem + ".txt")

    if saida.exists():
        print(f"[{i}/{len(arquivos)}] {pdf.name}: já existe, pulando.")
        pulados += 1
        continue

    print(f"[{i}/{len(arquivos)}] {pdf.name}")
    try:
        if pdf_para_txt(pdf, saida):
            convertidos += 1
        else:
            print("  O PDF tem senha. Remova a senha e tente de novo.")
            com_erro += 1
    except Exception as erro:
        print(f"  Erro em {pdf.name}: {erro}")
        com_erro += 1

print("\n--- RESUMO ---")
print(f"PDFs convertidos: {convertidos}")
print(f"PDFs pulados (TXT já existia): {pulados}")
if com_erro:
    print(f"PDFs com erro: {com_erro}")
print("Pronto! Textos salvos em:", PASTA_SAIDA)