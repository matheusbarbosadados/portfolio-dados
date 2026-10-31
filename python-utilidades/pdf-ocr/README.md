# PDF - OCR

Três scripts em Python que leem PDFs digitalizados (só imagem) usando OCR e extraem o texto. OCR é a tecnologia que "lê" o texto que está dentro de uma imagem.

## Arquivos

| Arquivo | Descrição |
|---|---|
| pdf_para_pdf_pesquisavel.py | Transforma um PDF de imagem em um PDF pesquisável |
| pdf_para_txt.py | Converte um PDF em um arquivo TXT |
| pdf_para_txt_lotes.py | Converte vários PDFs de uma pasta em arquivos TXT |

## Antes de usar

1. Instale o Tesseract OCR no Windows, com o idioma português.
2. Instale as bibliotecas:

       pip install pymupdf pytesseract pillow

3. Confira o caminho do Tesseract no script:

       C:\Program Files\Tesseract-OCR\tesseract.exe

## Como usar

**pdf_para_pdf_pesquisavel.py e pdf_para_txt.py**

1. Coloque o PDF na mesma pasta do script, com o nome `entrada.pdf`.
2. Execute o script (por exemplo: `python pdf_para_txt.py`).
3. Acompanhe o progresso no terminal.
4. Abra o arquivo gerado: `pdf_pesquisavel.pdf` ou `saida.txt`.

**pdf_para_txt_lotes.py**

1. Crie uma pasta chamada `pdfs` ao lado do script e coloque nela os PDFs.
2. Execute: `python pdf_para_txt_lotes.py`
3. Os textos são salvos na pasta `textos`.

Para usar outros nomes ou pastas, altere as linhas no começo do script.

## Como funciona

**pdf_para_pdf_pesquisavel.py**

1. Abre o PDF e transforma cada página em imagem.
2. O Tesseract lê o texto da imagem.
3. Cria um novo PDF com a imagem e o texto invisível por cima.

**pdf_para_txt.py**

1. Faz o OCR de cada página de um PDF.
2. Junta tudo em um único TXT.
3. Marca o início de cada página com "--- Página N ---".

**pdf_para_txt_lotes.py**

1. Lista todos os PDFs da pasta de entrada.
2. Faz o OCR de cada página.
3. Salva um TXT para cada PDF na pasta de saída.
4. Pula os PDFs que já foram convertidos.
5. Se um PDF der erro, mostra a mensagem e segue para o próximo.

## Bibliotecas usadas

pymupdf (fitz), pytesseract, pillow

## Limitações

- Precisa do Tesseract instalado.
- Os nomes dos arquivos e das pastas estão fixos no código.
- PDFs grandes demoram, pois cada página é lida em alta resolução (300 dpi).
- A qualidade depende da imagem. Páginas borradas ou inclinadas podem ter erros.
- Tabelas e colunas podem sair fora de ordem no TXT.
