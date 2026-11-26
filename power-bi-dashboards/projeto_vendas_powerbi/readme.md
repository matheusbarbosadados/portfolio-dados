[readme.md](https://github.com/user-attachments/files/35483397/readme.md)
# 📊 Dashboard de Vendas e Performance Comercial — Power BI

Este projeto apresenta um relatório interativo de **Business Intelligence e Análise de Dados** desenvolvido no **Power BI Desktop** a partir de bases de vendas de informática (2024–2026).

O objetivo é consolidar indicadores financeiros e comerciais — como faturamento, lucro, margem, desempenho por vendedor, categorias, formas de pagamento, evolução mensal/anual e distribuição geográfica — em um painel visual com tema escuro (`tema_tecnologico.json`).

---

## 📁 Arquivos do Projeto

- **Relatório Power BI (`.pbix`):** `Projeto_Vendas - Concluido.pbix`
- **Tema Personalizado:** `tema_tecnologico.json`
- **Bases de Dados (`.xlsx`):**
  - `Base_Vendas_Informatica_2024_2025.xlsx`
  - `Base_Vendas_Informatica_2026.xlsx`
- **Capturas das Páginas:** `Dashboard 1.png`, `Dashboard 2.png`, `Dashboard 3.png` e `Dashboard 4.png`

---

## 🗂️ Estrutura das Páginas do Dashboard

O relatório está dividido em **4 páginas**, com modelagem relacional estruturada em tabela fato (`F_Vendas_Total`), tabelas dimensão (`D_Produtos`, `D_Vendedores`, `D_Clientes`) e tabela dedicada às medidas (`Medidas`):

1. **Dashboard de Vendas (`Dashboard 1.png`):** Visão geral do painel de vendas e principais indicadores.
2. **Resumo de Vendas e Rentabilidade (`Dashboard 2.png`):** Cartões de **Faturamento Total** (`R$ 714.495,00`), **Lucro Total** (`R$ 287.941,00`), **Margem de Lucro** (`40,30%`) e **Total de Vendas** (`1.950`), segmentações de dados, medidor de meta/receita anterior, gráficos de rosca, barras empilhadas e gráfico combinado de colunas e linhas.
3. **Desempenho Comercial e Categorias (`Dashboard 3.png`):** Tabela de vendedores com vendas concluídas, faturamento e lucro, indicadores de periféricos e média de itens por venda, gráfico de área empilhada, pizza por categoria e matriz de análise.
4. **Análise por Produto e Evolução Anual (`Dashboard 4.png`):** Ranking de faturamento por produto, participação por grupo de produto ao longo dos anos, comparativo de lucro e faturamento por categoria e visão geográfica por estado.

---

## 🖼️ Prévia das Páginas

### Página 1 — Dashboard de Vendas
---

![Dashboard 1](./Dashboard%201.png)

### Página 2 — Resumo de Vendas e Rentabilidade
---

![Dashboard 2](./Dashboard%202.png)

---

### Página 3 — Desempenho Comercial e Categorias
![Dashboard 3](./Dashboard%203.png)

---

### Página 4 — Análise por Produto e Evolução Anual
![Dashboard 4](./Dashboard%204.png)

---

## 🛠️ Ferramentas e Boas Práticas Aplicadas

- **Power BI Desktop:** Construção dos visuais, formatação, filtros, segmentações de dados, matrizes, tabelas e mapa preenchido.
- **DAX:** Criação de medidas de negócio (faturamento, lucro, margem, volume de vendas, comparativos temporais e participação percentual) e coluna de localização (`Local`) para o mapa.
- **Organização Visual:** Aplicação de tema escuro personalizado (`tema_tecnologico.json`), títulos nos visuais e divisão do relatório em páginas temáticas.

---

## ▶️ Como Visualizar

1. Baixe o arquivo `Projeto_Vendas - Concluido.pbix` (junto com as planilhas `.xlsx` e `tema_tecnologico.json`, caso queira atualizar ou inspecionar as fontes).
2. Abra o arquivo `.pbix` no **Power BI Desktop**.
3. Navegue entre as páginas **Dashboard de Vendas**, **Resumo de Vendas e Rentabilidade**, **Desempenho Comercial e Categorias** e **Análise por Produto e Evolução Anual**.

## ⚠️ Este projeto foi desenvolvido com base em um roteiro próprio de estudos em Power BI, utilizando bases de vendas estruturadas para praticar modelagem relacional, medidas em DAX e construção de painéis visuais.
