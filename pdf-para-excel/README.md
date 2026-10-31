PDF para Excel

Script em Python que lê um PDF e salva o conteúdo em uma planilha Excel, com uma aba por página.

O que ele faz

- Encontra tabelas no PDF, mesmo sem linhas desenhadas.
- Mantém o texto que está fora das tabelas.
- Converte números, moeda (R$) e porcentagem para o formato do Excel.
- Preserva códigos com zeros à esquerda (ex.: 00123).
- Ignora o número da página e o rodapé.
- Mostra um resumo de cada página e avisa sobre imagens.

Arquivos

Arquivo | Descrição
pdf_para_excel.py | Script principal

Como usar

1. Instale as bibliotecas:
   pip install pdfplumber openpyxl
2. Coloque o PDF na mesma pasta do script.
3. Execute:
   python pdf_para_excel.py nome_do_arquivo.pdf
4. A planilha é salva com o mesmo nome do PDF, com final .xlsx.

Bibliotecas usadas

pdfplumber, openpyxl

Limitações

- PDFs digitalizados (imagens) não funcionam, pois não têm texto.
- Imagens dentro do PDF não são copiadas para o Excel.
