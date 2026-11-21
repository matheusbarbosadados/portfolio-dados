import glob
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def carregar_dados_tratados():
    """Localiza e carrega todos os CSVs da pasta 3_dados_tratados e a base de UF."""
    dados = {}

    caminho_busca = os.path.join("3_dados_tratados", "tratado_*.csv")
    arquivos = glob.glob(caminho_busca)

    if not arquivos:
        arquivos = glob.glob("tratado_*.csv")

    for arq in arquivos:
        nome_arq = os.path.basename(arq).lower()
        df = pd.read_csv(arq)

        if "sexo" in nome_arq:
            dados["sexo"] = df
        elif "faixa" in nome_arq:
            dados["faixa_etaria"] = df
        elif "escolaridade" in nome_arq:
            dados["escolaridade"] = df
        elif "estado civil" in nome_arq:
            dados["estado_civil"] = df
        elif "cor e raca" in nome_arq or "raca" in nome_arq:
            dados["cor_raca"] = df

    arq_uf = os.path.join(
        "3_dados_tratados", "mortalidade_causas_externas_x60_x84_tratado.csv"
    )
    if not os.path.exists(arq_uf):
        arq_uf = "mortalidade_causas_externas_x60_x84_tratado.csv"

    if os.path.exists(arq_uf):
        dados["uf"] = pd.read_csv(arq_uf)

    return dados


def gerar_html_dashboard(dados):
    """Gera o arquivo index.html contendo KPIs, gráficos ordenados e suporte dinamico ao Dark Mode."""
    print("Gerando visualizações interativas atualizadas com Plotly...")

    # 1. Gráfico de Evolução Temporal (Sexo)
    df_sexo = dados.get("sexo")
    fig_evolucao = go.Figure()

    if df_sexo is not None:
        df_sexo_fil = df_sexo[~df_sexo["Sexo"].isin(["Total", "Ign"])].copy()
        df_sexo_fil["ano"] = df_sexo_fil["ano"].astype(str)

        for sexo in df_sexo_fil["Sexo"].unique():
            df_sub = df_sexo_fil[df_sexo_fil["Sexo"] == sexo]
            fig_evolucao.add_trace(
                go.Scatter(
                    x=df_sub["ano"],
                    y=df_sub["obitos"],
                    mode="lines+markers",
                    name="Masculino" if sexo == "Masc" else "Feminino",
                    line=dict(width=3),
                )
            )

        fig_evolucao.update_layout(
            title="<b>Evolução Anual por Gênero (2014-2024)</b>",
            xaxis_title="Ano",
            yaxis_title="Número de Óbitos",
            template="plotly_white",
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#333333"),
        )

    # 2. Gráfico de Faixa Etária (Ajuste de Fonte e Espaçamento Lateral)
    df_fe = dados.get("faixa_etaria")
    fig_fe = go.Figure()

    if df_fe is not None:
        df_fe_grouped = (
            df_fe.groupby("Faixa Etária")["obitos"]
            .sum()
            .reset_index()
            .sort_values(by="obitos", ascending=True)
        )
        fig_fe = px.bar(
            df_fe_grouped,
            x="obitos",
            y="Faixa Etária",
            orientation="h",
            title="<b>Distribuição Acumulada por Faixa Etária</b>",
            text="obitos",
            labels={"obitos": "Total de Óbitos", "Faixa Etária": ""},
            template="plotly_white",
            color="obitos",
            color_continuous_scale="Reds",
        )
        fig_fe.update_traces(
            texttemplate="%{text:,}",
            textposition="outside",
            textfont_size=11,
            cliponaxis=False,
        )
        fig_fe.update_layout(
            margin=dict(l=20, r=70, t=50, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#333333"),
        )

    # 3. Gráfico de Escolaridade (Retorno ao Formato Rosca/Pizza com Legenda Ordenada)
    df_esc = dados.get("escolaridade")
    fig_esc = go.Figure()

    if df_esc is not None:
        ordem_escolaridade = [
            "Nenhuma",
            "1 A 3 Anos",
            "4 A 7 Anos",
            "8 A 11 Anos",
            "12 Anos E Mais",
            "Ignorado",
        ]

        df_esc_grouped = (
            df_esc.groupby("Escolaridade")["obitos"].sum().reset_index()
        )

        fig_esc = px.pie(
            df_esc_grouped,
            values="obitos",
            names="Escolaridade",
            title="<b>Distribuição por Nível de Escolaridade</b>",
            hole=0.4,
            template="plotly_white",
            category_orders={"Escolaridade": ordem_escolaridade},
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_esc.update_traces(
            textinfo="percent+label",
            textposition="inside",
            insidetextorientation="radial",
        )
        fig_esc.update_layout(
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#333333"),
        )

    # 4. Gráfico por Estado (Top 10 UFs)
    df_uf = dados.get("uf")
    fig_uf = go.Figure()

    if df_uf is not None:
        df_uf_grouped = (
            df_uf.groupby("uf")["obitos"]
            .sum()
            .reset_index()
            .sort_values(by="obitos", ascending=False)
            .head(10)
        )
        fig_uf = px.bar(
            df_uf_grouped,
            x="uf",
            y="obitos",
            title="<b>Top 10 Estados com Maior Volume de Registros (2014-2024)</b>",
            text="obitos",
            labels={"obitos": "Total de Óbitos", "uf": "Estado"},
            template="plotly_white",
            color="obitos",
            color_continuous_scale="Blues",
        )
        fig_uf.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig_uf.update_layout(
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#333333"),
        )

    # Converter os gráficos para HTML
    html_evolucao = fig_evolucao.to_html(
        full_html=False, include_plotlyjs="cdn"
    )
    html_fe = fig_fe.to_html(full_html=False, include_plotlyjs=False)
    html_esc = fig_esc.to_html(full_html=False, include_plotlyjs=False)
    html_uf = fig_uf.to_html(full_html=False, include_plotlyjs=False)

    # Estrutura do Site HTML com Suporte Avançado a Tema Escuro Dinâmico
    html_completo = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard de Mortalidade - DATASUS CID-10 X60-X84</title>
    <style>
        :root {{
            --bg-color: #f4f7f6;
            --card-bg: #ffffff;
            --text-color: #222222;
            --subtext-color: #555555;
            --header-bg: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            --header-text: #ffffff;
            --card-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}

        [data-theme="dark"] {{
            --bg-color: #121212;
            --card-bg: #1e1e1e;
            --text-color: #ffffff;
            --subtext-color: #b0b0b0;
            --header-bg: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
            --header-text: #ffffff;
            --card-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        .header {{
            background: var(--header-bg);
            color: var(--header-text);
            padding: 25px 30px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .header-content h1 {{
            margin: 0 0 10px 0;
            font-size: 24px;
        }}

        .header-content p {{
            margin: 0;
            opacity: 0.9;
            font-size: 14px;
        }}

        .theme-toggle {{
            background-color: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.4);
            color: white;
            padding: 10px 18px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
            font-size: 13px;
            transition: all 0.3s ease;
        }}

        .theme-toggle:hover {{
            background-color: rgba(255, 255, 255, 0.3);
        }}

        .kpi-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }}

        .kpi-card {{
            background: var(--card-bg);
            padding: 20px;
            border-radius: 10px;
            box-shadow: var(--card-shadow);
            border-left: 5px solid #2a5298;
            transition: background-color 0.3s ease;
        }}

        .kpi-card .title {{
            font-size: 12px;
            color: var(--subtext-color);
            text-transform: uppercase;
            font-weight: bold;
        }}

        .kpi-card .value {{
            font-size: 28px;
            font-weight: bold;
            color: var(--text-color);
            margin-top: 5px;
        }}

        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 25px;
        }}

        .chart-card {{
            background: var(--card-bg);
            padding: 15px;
            border-radius: 12px;
            box-shadow: var(--card-shadow);
            transition: background-color 0.3s ease;
        }}

        .full-width {{
            grid-column: 1 / -1;
        }}

        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            font-size: 13px;
            color: var(--subtext-color);
        }}
    </style>
</head>
<body>

    <div class="header">
        <div class="header-content">
            <h1>📊 Painel de Análise Epidemiológica: Lesões Autoprovocadas (CID-10 X60-X84)</h1>
            <p>Dados Oficiais do SIM / DATASUS — Período de Análise: 2014 a 2024 | Projeto de Engenharia de Dados</p>
        </div>
        <button class="theme-toggle" onclick="toggleTheme()">🌙 Alternar Tema</button>
    </div>

    <div class="kpi-container">
        <div class="kpi-card">
            <div class="title">Total de Registros (2014-2024)</div>
            <div class="value">151.561</div>
        </div>
        <div class="kpi-card" style="border-left-color: #d9534f;">
            <div class="title">Proporção Masculina</div>
            <div class="value">78,39%</div>
        </div>
        <div class="kpi-card" style="border-left-color: #f0ad4e;">
            <div class="title">Crescimento no Período</div>
            <div class="value">+57,2%</div>
        </div>
        <div class="kpi-card" style="border-left-color: #5bc0de;">
            <div class="title">Faixa Etária Principal</div>
            <div class="value">20 a 39 anos</div>
        </div>
    </div>

    <div class="chart-grid">
        <div class="chart-card full-width">
            {html_evolucao}
        </div>
        <div class="chart-card">
            {html_fe}
        </div>
        <div class="chart-card">
            {html_esc}
        </div>
        <div class="chart-card full-width">
            {html_uf}
        </div>
    </div>

    <div class="footer">
        <p>Desenvolvido como projeto de portfólio em Python & DATASUS | Fonte: Ministério da Saúde (SVSA/CGIAE)</p>
    </div>

    <script>
        function toggleTheme() {{
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            
            const isDark = newTheme === 'dark';
            const textColor = isDark ? '#ffffff' : '#333333';
            
            const btn = document.querySelector('.theme-toggle');
            btn.textContent = isDark ? '☀️ Modo Claro' : '🌙 Modo Escuro';

            // Atualiza dinamicamente a cor de todas as fontes dos gráficos Plotly
            const graphDivs = document.querySelectorAll('.plotly-graph-div');
            graphDivs.forEach(div => {{
                Plotly.relayout(div, {{
                    'font.color': textColor,
                    'title.font.color': textColor,
                    'xaxis.title.font.color': textColor,
                    'xaxis.tickfont.color': textColor,
                    'yaxis.title.font.color': textColor,
                    'yaxis.tickfont.color': textColor,
                    'legend.font.color': textColor
                }});
            }});
        }}
    </script>

</body>
</html>"""

    caminho_saida = "index.html"
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(html_completo)

    print(f"\n✅ Dashboard atualizado com sucesso!")
    print(f"📄 Arquivo gerado: {os.path.abspath(caminho_saida)}")


if __name__ == "__main__":
    dados_carregados = carregar_dados_tratados()
    gerar_html_dashboard(dados_carregados)