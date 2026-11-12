###### **GUIA DE USO - PDF PARA EXCEL**



Passo 1: Abra a pasta “PDF para Excel” no VS Code.

Passo 2: Só na primeira vez, abra o terminal do VS Code e digite **pip install pdfplumber openpyxl**. O tkinter, que abre a janela, já vem com o Python.

Passo 3: Abra **1\_pdf\_para\_excel.py** e clique no ícone de executar. O script converte um PDF em planilha do Excel, mantendo tabelas, bordas, negrito e textos soltos.

Passo 4: Na janela que abrir, escolha o PDF.

Passo 5: Aguarde. O terminal mostra uma linha por página e, no final, o caminho do arquivo salvo.

Passo 6: Quando terminar, o resultado fica na mesma pasta do PDF escolhido, com o mesmo nome e a extensão .xlsx (exemplo: **contrato.pdf** gera **contrato.xlsx**). Cada página vira uma aba (Página\_1, Página\_2 e assim por diante).





##### ATENÇÃO:



* Se já existir um **.xlsx** com o **mesmo nome na pasta** do PDF, ele é substituído sem aviso.
Se estiver aberto no Excel, o script dá erro ao salvar. Feche o arquivo antes de executar.



* Só funciona com PDF que tenha texto de verdade. PDF escaneado vira uma aba com o aviso "Página sem texto detectado." O script não faz OCR.



* Imagens do PDF não vão para o Excel, e o terminal não avisa mais sobre isso.
* O negrito segue o do PDF. Se o PDF não tiver negrito e a tabela tiver 3 linhas ou mais...
A primeira linha vira cabeçalho cinza mesmo que não seja um cabeçalho. O texto fora das tabelas sai em itálico cinza.



* Valores como R$ 1.234,50 e 25% viram números. Números com ponto são lidos como milhar (1.234 vira 1234).
Números com mais de 15 dígitos, como chave de nota fiscal, ficam com dígitos errados.



* Em PDF com layout complicado, a tabela pode sair dividida ou misturada com texto. Confira o resultado.

