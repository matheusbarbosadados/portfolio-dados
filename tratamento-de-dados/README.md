##### **LIMPEZA AUTOMÁTICA DE PLANILHAS**

Script em Python que recebe uma planilha (CSV ou Excel), corrige os problemas mais comuns e gera um relatório do que foi feito. Funciona com qualquer arquivo, pois identifica sozinho o tipo de cada coluna.



##### **ARQUIVOS**



teste.py - script de limpeza

dados\_baguncados.csv - planilha de teste com 200 linhas e erros colocados de propósito

gabarito.csv - lista dos erros colocados e dos valores corretos, usada para conferir o resultado

dados\_baguncados\_limpo.csv - resultado da limpeza em CSV

dados\_baguncados\_limpo.xlsx - resultado da limpeza em Excel



##### **REQUISITOS**



1. Python 3
2. Biblioteca pandas
3. Biblioteca openpyxl (só para gerar o arquivo Excel)



##### **COMO USAR**



1. Abra o teste.py no VS Code.
2. Clique no ícone de executar.
3. Escolha a planilha na janela que abrir.
4. Leia o relatório no terminal.
5. Abra o arquivo \_limpo.xlsx ou \_limpo.csv e filtre a coluna alerta.



##### **COMO FUNCIONA**



1. Lê o arquivo e remove espaços sobrando e letras quebradas por problema de acentuação.
2. Identifica pelo conteúdo se cada coluna é data, número, categoria ou texto.
3. Converte as datas para o padrão AAAA-MM-DD e os números para ponto decimal, aceitando formatos como 1.925,67, 5,749.61 e R$ 492,64.
4. Padroniza categorias escritas de formas diferentes (maiúsculas, minúsculas, espaços e hífen).
5. Remove linhas repetidas, quando todas as colunas são iguais, exceto o identificador que nunca se repete.
6. Cria a coluna alerta, que marca o que não foi possível corrigir: datas inválidas, células vazias, valores muito acima do normal e nomes parecidos.



##### **LIMITAÇÕES**



* Datas impossíveis (como 31/02/2026) e células vazias são apenas marcadas, não corrigidas.
* Erros de digitação e diferenças de acento nos nomes não são alterados, apenas avisados.
* Regras específicas do negócio, como comissão maior que o valor, não são verificadas.
* Duas linhas totalmente iguais podem ser registros verdadeiros, por isso o terminal lista as linhas removidas para conferência.
* Números ambíguos, como 5,749, não são convertidos e ficam marcados.







