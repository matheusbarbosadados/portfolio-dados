##### **PROJETO TSE - PARTICIPAÇÃO ELEITORAL 2026**

Estudo técnico e neutro da participação nas eleições presidenciais de 2026 (1º e 2º turno), com dados públicos do TSE: abstenção, votos brancos e votos nulos por estado.

##### **ARQUIVOS**

01_dados_brutos/Link TSE.txt - links de onde os dados foram baixados

01_dados_brutos/detalhe_votacao_munzona_2026_BRASIL.csv - detalhe da apuração por município e zona, como veio do TSE

01_limpar.py - lê o CSV, filtra o cargo de Presidente, confere as contas e salva os CSVs limpos

02_dados_limpos/presidente_munzona.csv - dados de Presidente por município e zona, já limpos

02_dados_limpos/resumo_por_uf.csv - resumo por estado

03_sql/01_criar_banco.sql - cria o banco tse_participacao e a tabela

03_sql/02_views.sql - cria a view vw_resumo_uf

02_carregar.py - carrega os dados limpos no MySQL

04_powerbi/dashboard_participacao.pbix - dashboard no Power BI

04_powerbi/dashboard_tse.png - imagem do dashboard

##### **COMO USAR**

1. Baixe o CSV pelo link do arquivo Link TSE.txt e coloque na pasta 01_dados_brutos.
2. Abra o 01_limpar.py no VS Code e execute. Os CSVs limpos serão salvos na pasta 02_dados_limpos.
3. No MySQL, execute o arquivo 01_criar_banco.sql.
4. Abra o 02_carregar.py no VS Code e execute. A senha do MySQL é pedida na hora e não fica no código.
5. No MySQL, execute o arquivo 02_views.sql.
6. Abra o dashboard_participacao.pbix no Power BI Desktop.

##### **COMO FUNCIONA**

O script 01_limpar.py lê o CSV do TSE, mantém só o cargo de Presidente (1º e 2º turno), confere se as somas batem e salva os arquivos limpos.

O script 02_carregar.py envia esses dados para o banco tse_participacao no MySQL.

A view vw_resumo_uf soma os dados por estado (UF) e alimenta o dashboard no Power BI, que mostra abstenção, votos brancos e votos nulos.

##### **LIMITAÇÕES**

- Só o cargo de Presidente, no 1º e no 2º turno.
- O exterior (ZZ) fica fora do dashboard.
- Só dados públicos e agregados, sem análise de candidatos ou partidos.
- Precisa de um MySQL instalado no computador.
- Projeto de estudo: não substitui os resultados oficiais do TSE.
