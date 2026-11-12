##### **PDF para Excel**



Script em Python que lê um PDF e salva o conteúdo em uma planilha Excel, com uma aba por página.

#### 

#### **O que ele faz**



* Encontra tabelas no PDF, mesmo sem linhas desenhadas. Mantém o texto que está fora das tabelas.
* Converte números, moeda (R$) e porcentagem para o formato do Excel. Mantém códigos com zeros à esquerda (exemplo: 00123).
* Preserva negrito, bordas e células mescladas das tabelas.
* Ignora o número da página e o rodapé.
* Mostra um resumo de cada página no terminal.



**Arquivos:**



**1\_pdf\_para\_excel.py** é o script principal.



##### **Como usar**



1. Só na primeira vez, instale as bibliotecas no terminal do VS Code com o comando pip install pdfplumber openpyxl.
2. Depois, abra o 1\_pdf\_para\_excel.py no VS Code e clique no ícone de executar.
3. Na janela que abrir, escolha o PDF.
4. A planilha é salva na mesma pasta do PDF, com o mesmo nome e final .xlsx.



##### **Bibliotecas usadas**



pdfplumber, openpyxl, tkinter e re (as duas últimas já vêm com o Python).



##### **Limitações**



* PDFs digitalizados (imagens) não funcionam, pois não têm texto.
* Imagens dentro do PDF não são copiadas para o Excel.
* Em PDFs com layout complicado, confira o resultado, pois uma tabela pode sair dividida.













