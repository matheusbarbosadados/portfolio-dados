##### **PROJETO PLANILHA A E B**



Compara duas planilhas Excel e copia para a planilha A as linhas que existem na B e ainda não existem nela. A comparação é feita pelo identificador (ID) da primeira coluna.



Exemplo: a planilha B tem 45 vendas e a A tem 30. Se as 30 da A também estão na B, o script traz as 15 que faltam para a A, com a formatação original.



##### **ARQUIVOS**



planilha_A_e_B.py - script principal

Vendas de Informática 30.xlsx - planilha A (a menor), que será completada

Vendas de Informática 45.xlsx - planilha B (a maior e mais atualizada)

planilha_a_atualizada.xlsx - resultado, criado pelo script na mesma pasta da planilha A



##### **REQUISITOS**



- Python 3
- Biblioteca openpyxl
- Biblioteca tkinter, que já vem com o Python e abre as janelas de escolha dos arquivos



##### **COMO USAR**



1. Instale a biblioteca (só na primeira vez): pip install openpyxl
2. Feche as duas planilhas no Excel.
3. Abra planilha_A_e_B.py no VS Code e clique no ícone de executar.
4. Na primeira janela, escolha a planilha A (a que recebe as linhas).
5. Na segunda janela, escolha a planilha B (de onde vêm as linhas novas).
6. Abra planilha_a_atualizada.xlsx.



##### **COMO FUNCIONA**



1. Abre a aba ativa de cada planilha.
2. Lê os IDs da primeira coluna da planilha A, a partir da linha 2.
3. Percorre a planilha B e identifica as linhas cujo ID não existe na A.
4. Copia essas linhas para o final da A, com valores, formato de número, fonte, preenchimento, borda e alinhamento.
5. Salva o resultado em um arquivo novo, sem alterar as planilhas originais.
6. Mostra no terminal quantas vendas foram adicionadas.



##### **LIMITAÇÕES**



- O ID precisa estar na primeira coluna.
- A primeira linha precisa ser o cabeçalho, e as colunas precisam estar na mesma ordem nas duas planilhas.
- Só adiciona linhas novas. Não atualiza linhas que já existem e não remove linhas que estão apenas na A.
- Usa apenas a aba ativa de cada arquivo.
- IDs iguais em formatos diferentes (número em uma planilha e texto na outra) são tratados como diferentes.
- Fórmulas são copiadas como estão, sem ajuste de referências.
- Larguras de coluna e células mescladas não são copiadas.
- Se o arquivo de resultado já existir, é substituído. Se estiver aberto no Excel, ocorre erro ao salvar.