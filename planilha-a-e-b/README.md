PROJETO PLANILHA A E B

Compara duas planilhas Excel e copia para a menor as linhas que estão faltando nela.

Exemplo: a planilha B tem 45 vendas e a A tem 30. O script traz as 15 que faltam para a A.

ARQUIVOS

planilha_A_e_B.py - script principal
Vendas de Informática 30.xlsx - planilha menor (A), que será completada
Vendas de Informática 45.xlsx - planilha maior e mais atualizada (B)
planilha_a_atualizada.xlsx - resultado, criado pelo script

COMO USAR

1. Instale a biblioteca: pip install openpyxl
2. Coloque as duas planilhas na mesma pasta do script.
3. Execute: python planilha_A_e_B.py
4. Abra planilha_a_atualizada.xlsx.

COMO FUNCIONA

1. Abre as duas planilhas.
2. Lê os IDs da coluna A da planilha menor.
3. Procura na maior os IDs que não existem na menor.
4. Copia essas linhas, com a formatação.
5. Salva tudo em um arquivo novo.
6. Mostra quantas vendas foram adicionadas.

LIMITAÇÕES

- O ID precisa estar na primeira coluna.
- A primeira linha precisa ser o cabeçalho.
- Só adiciona linhas novas. Não atualiza linhas que já existem.
- A planilha original não é alterada.
