###### **PDFS (OCR)**



Três scripts que convertem PDFs em texto ou em PDF pesquisável, usando o texto do próprio PDF ou OCR nas páginas de imagem.



###### **ARQUIVOS**



**pdf\_para\_pdf\_pesquisavel.py** - transforma um PDF de imagem em um PDF pesquisável

**pdf\_para\_txt\_lotes.py** - converte vários PDFs de uma pasta em arquivos TXT

**pdf\_para\_txt.py** - converte um PDF em um arquivo TXT



###### **ANTES DE USAR**



1. Instale o Tesseract OCR no Windows, com o idioma português.
2. Instale as bibliotecas: pip install pymupdf pytesseract pillow
3. Confira o caminho do Tesseract no começo de cada script:
C:/Program Files/Tesseract-OCR/tesseract.exe



###### **COMO USAR**



1. Abra o script e clique no ícone de executar.
2. Escolha o PDF, a pasta ou o local de saída nas janelas que abrem.
3. Acompanhe o progresso no terminal.
4. Abra o arquivo gerado.



###### **COMO FUNCIONA**



**pdf\_para\_pdf\_pesquisavel.py**

1. Abre uma janela para escolher o PDF e outra para escolher onde salvar.
2. Transforma cada página em imagem.
3. O Tesseract lê o texto da imagem.
4. Cria um novo PDF com a imagem e o texto invisível por cima.



**pdf\_para\_txt\_lotes.py**

1. Abre uma janela para escolher a pasta dos PDFs e outra para a pasta de saída.
2. Lista todos os PDFs da pasta de entrada.
3. Em cada página, usa o texto do próprio PDF. Se a página tiver pouco texto, faz OCR.
4. Ignora cabeçalho e rodapé, refaz palavras cortadas com hífen e junta frases quebradas em várias linhas.
5. Salva um TXT para cada PDF na pasta de saída.
6. Pula os PDFs que já foram convertidos.
7. Se um PDF der erro ou tiver senha, mostra a mensagem e segue para o próximo.
8. No final, mostra o resumo no terminal.



**pdf\_para\_txt.py**

1. Abre uma janela para escolher o PDF.
2. Em cada página, usa o texto do próprio PDF. Se a página tiver pouco texto, faz OCR.
3. Ignora cabeçalho e rodapé, refaz palavras cortadas com hífen e junta frases quebradas em várias linhas.
4. Junta tudo em um único TXT, salvo na mesma pasta do PDF, com o mesmo nome.
5. Marca o início de cada página com "--- Página N ---".
6. No final, mostra o resumo no terminal.



###### **BIBLIOTECAS**



pymupdf (fitz), pytesseract, pillow, tkinter, io, pathlib, unicodedata





###### **LIMITAÇÕES**



* Precisa do Tesseract instalado.
* O pdf\_para\_pdf\_pesquisavel.py faz OCR em todas as páginas e é o mais lento.
* PDFs grandes demoram no OCR, pois cada página é lida em alta resolução (300 dpi).
* A qualidade depende da imagem. Páginas borradas ou inclinadas podem ter erros, e palavras de baixa confiança são descartadas.
* Cabeçalho e rodapé só são ignorados nas páginas com texto próprio. Nas páginas lidas por OCR, eles entram no TXT.
* PDFs com senha não funcionam.
* Tabelas e colunas podem sair fora de ordem no TXT.







