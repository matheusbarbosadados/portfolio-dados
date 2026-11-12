###### **GUIA DE USO - PROJETO PLANILHA A E B**



Passo 1: Abra a pasta “Projeto Planilha A e B” no VS Code.

Passo 2: Só na primeira vez, abra o terminal do VS Code e digite **pip install openpyxl**. Essa é a única biblioteca que precisa instalar.

Passo 3: Feche as duas planilhas no Excel.

Passo 4: Abra **planilha\_A\_e\_B.py** e clique no ícone de executar. O script copia da planilha B para a A as vendas que ainda não existem na A, comparando pelo ID da primeira coluna.

Passo 5: Na primeira janela, escolha a planilha A (a que recebe as vendas). Na segunda janela, escolha a planilha B (de onde vêm as vendas novas).

Passo 6: Aguarde. O terminal mostra "X vendas adicionadas".

Passo 7: Quando terminar, o resultado fica em **planilha\_a\_atualizada.xlsx**, na mesma pasta da planilha A.









##### ATENÇÃO:





* Escolha a A primeiro e a B depois. Na ordem errada, as vendas vão no sentido contrário.
* As planilhas originais não são alteradas. O arquivo novo é substituído a cada execução, e dá erro se estiver aberto no Excel.
* O **planilha\_a\_atualizada.xlsx** que está na pasta é de 02/10, anterior às duas planilhas. Execute de novo para ele refletir os dados atuais.
* A comparação é só pelo ID da primeira coluna. Se uma venda existe nas duas com dados diferentes, a A não é atualizada. Vendas que estão só na A continuam lá.
* As duas planilhas precisam ter o cabeçalho na linha 1 e as colunas na mesma ordem.
* O script usa só a aba ativa de cada arquivo (a que estava aberta quando foi salvo).
* Se o ID for número em uma planilha e texto na outra, o script os trata como diferentes e a venda entra repetida.
* Linhas vazias no fim da B podem entrar como linhas em branco na A. Fórmulas da B são copiadas como estão. Se houver fórmulas, confira o resultado.

