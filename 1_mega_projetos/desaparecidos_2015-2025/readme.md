# 🔎 Painel de Pessoas Desaparecidas no Brasil (2015 a 2025)

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

Projeto de Análise de Dados e visualização interativa dos registros de pessoas desaparecidas e localizadas no Brasil entre 2015 e 2025, com filtros por período, região e estado, feito em Python com Streamlit e Plotly.

---

## 📸 Visual do Painel

![Painel de Pessoas Desaparecidas](./imagens/painel.png)

---

## 🔗 Fonte dos Dados

O arquivo CSV foi obtido no portal abaixo. O nome do arquivo indica origem no Sinesp (Sistema Nacional de Informações de Segurança Pública), mas o portal é de terceiros e não é um site oficial do governo.

* **Portal:** [Sumidos PB - Dashboard](https://sumidospb.com.br/portaldashboard.php?ano=2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025)

Para conferência dos totais, foram usados como referência os números do [Anuário Brasileiro de Segurança Pública](https://forumseguranca.org.br/publicacoes/anuario-brasileiro-de-seguranca-publica/), do Fórum Brasileiro de Segurança Pública.

---

## 🧩 O que o Painel Mostra

* Cartões com total de desaparecidas, total de localizadas, média por dia (aproximada) e quantidade de estados no filtro
* Evolução por ano (desaparecidas e localizadas)
* Desaparecidas por estado, por região, por sexo e por faixa etária
* Filtros de período, região e estado, com o total de cada opção ao lado do nome
* Aviso automático dos estados e anos com meses sem registro
* Tema claro ou escuro, escolhido pelo menu do Streamlit (canto superior direito)

---

## 📂 Estrutura do Repositório

```text
.
├── sinesp_desaparecidos_ano-2015-...-2025.csv   # Base de dados baixada do portal
├── 01_explorar.py          # Primeira exploração: colunas, anos e valores
├── 02_conferir.py          # Conferência de qualidade: repetidas, valores inválidos e meses sem registro
├── 03_faltas.py            # Estados e anos com dados faltando
├── app.py                  # Painel em Streamlit
└── README.md               # Documentação do projeto
```

---

## ▶️ Como Executar

1. Instale as bibliotecas:

```text
python -m pip install streamlit plotly pandas
```

2. Deixe o arquivo CSV na mesma pasta do app.py
3. No terminal, dentro da pasta do projeto, rode:

```text
python -m streamlit run app.py
```

4. O painel abre no navegador. Para trocar o tema, use o menu no canto superior direito, em Settings, Theme

---

## ⚠️ Limitações

* Meses sem registro: Acre, Espírito Santo e Tocantins (2015 a 2017), Paraíba (2015 a 2018), Goiás (2015 e parte de 2016) e um mês do Amazonas em 2019. Esses meses aparecem como sem dados, e não como zero, então os totais desses anos são parciais
* O total do Brasil só é totalmente comparável entre os anos a partir de 2019
* Pessoas localizadas em um ano não são necessariamente as que desapareceram no mesmo ano
* Os totais podem diferir um pouco dos divulgados em outras fontes, como o Anuário Brasileiro de Segurança Pública
* Os registros dependem do que cada estado envia, e há subnotificação
* A base só tem duas faixas etárias (0 a 17 e 18 ou mais), por isso o gráfico não detalha mais

---

## 🚀 Possíveis Melhorias

* Complementar os anos faltantes com outras fontes, mostrando-as separadas dos dados principais
* Detalhar as faixas etárias, caso apareçam dados mais finos (por exemplo 0 a 11, 12 a 17, 18 a 29, 30 a 59 e 60 ou mais)
