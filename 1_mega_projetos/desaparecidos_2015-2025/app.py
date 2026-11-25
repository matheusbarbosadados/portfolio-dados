from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Pessoas desaparecidas no Brasil", layout="wide")

pasta = Path(__file__).resolve().parent
arquivos = sorted(pasta.glob("sinesp_desaparecidos*.csv"))
if not arquivos:
    st.error("CSV não encontrado na pasta do app.")
    st.stop()


@st.cache_data
def carregar(caminho):
    return pd.read_csv(caminho, encoding="utf-8-sig")


def fmt(n):
    return f"{int(n):,}".replace(",", ".")


def rotular(fig, eixo):
    fig.update_traces(
        texttemplate="%{" + eixo + ":,.0f}", textposition="outside", cliponaxis=False
    )
    fig.update_layout(separators=",.")
    return fig


df = carregar(str(arquivos[0]))
anos = sorted(df["ano"].unique())

st.title("Pessoas desaparecidas no Brasil (2015 a 2025)")

st.sidebar.header("Filtros")
ano_ini, ano_fim = st.sidebar.select_slider(
    "Período", options=anos, value=(anos[0], anos[-1])
)

periodo = df[
    (df["ano"] >= ano_ini)
    & (df["ano"] <= ano_fim)
    & (df["situacao"] == "Desaparecida")
]

todas_regioes = sorted(df["regiao"].unique())
tot_regiao = periodo.groupby("regiao")["pessoas"].sum()
regioes = st.sidebar.multiselect(
    "Região",
    todas_regioes,
    default=todas_regioes,
    format_func=lambda r: f"{r} ({fmt(tot_regiao.get(r, 0))})",
)

tot_estado = periodo.groupby("estado")["pessoas"].sum()
estados_disp = sorted(df[df["regiao"].isin(regioes)]["estado"].unique())
estados = st.sidebar.multiselect(
    "Estado (vazio = todos)",
    estados_disp,
    format_func=lambda e: f"{e} ({fmt(tot_estado.get(e, 0))})",
)

base = df[df["regiao"].isin(regioes)]
if estados:
    base = base[base["estado"].isin(estados)]
f = base[(base["ano"] >= ano_ini) & (base["ano"] <= ano_fim)]

if f.empty:
    st.info("Nenhum dado para os filtros escolhidos.")
    st.stop()

desap = f[f["situacao"] == "Desaparecida"]
loc = f[f["situacao"] == "Localizada"]

meses = (
    df[df["situacao"] == "Desaparecida"]
    .groupby(["uf", "ano"])["mes"]
    .nunique()
    .unstack(fill_value=0)
)
avisos = []
for uf in sorted(base["uf"].unique()):
    ruins = [a for a in anos if ano_ini <= a <= ano_fim and meses.loc[uf, a] < 12]
    if ruins:
        avisos.append(f"{uf}: {', '.join(str(a) for a in ruins)}")
if avisos:
    lista = "\n".join(f"- {a}" for a in avisos)
    st.warning(
        "Estados com meses sem registro (os totais desses anos são parciais):\n\n"
        + lista
    )
    

total_desap = desap["pessoas"].sum()
total_loc = loc["pessoas"].sum()
dias = (ano_fim - ano_ini + 1) * 365

c1, c2, c3, c4 = st.columns(4)
c1.metric("Pessoas desaparecidas", fmt(total_desap))
c2.metric("Pessoas localizadas", fmt(total_loc))
c3.metric("Média por dia (aproximada)", fmt(total_desap / dias))
c4.metric("Estados no filtro", base["uf"].nunique())

por_ano = f.groupby(["ano", "situacao"], as_index=False)["pessoas"].sum()
fig = px.line(
    por_ano,
    x="ano",
    y="pessoas",
    color="situacao",
    markers=True,
    title="Evolução por ano",
    labels={"ano": "Ano", "pessoas": "Pessoas", "situacao": "Situação"},
)
fig.update_traces(
    mode="lines+markers+text", texttemplate="%{y:,.0f}", textposition="top center"
)
fig.update_layout(separators=",.")
fig.update_xaxes(dtick=1)
st.plotly_chart(fig, width="stretch")

col1, col2 = st.columns(2)
por_estado = (
    desap.groupby("estado", as_index=False)["pessoas"].sum().sort_values("pessoas")
)
fig = px.bar(
    por_estado,
    x="pessoas",
    y="estado",
    orientation="h",
    title="Desaparecidas por estado",
    labels={"pessoas": "Pessoas", "estado": "Estado"},
)
fig = rotular(fig, "x")
fig.update_layout(height=max(300, 22 * len(por_estado) + 130), margin=dict(t=80))
fig.update_xaxes(range=[0, por_estado["pessoas"].max() * 1.15])
col1.plotly_chart(fig, width="stretch")

por_regiao = (
    desap.groupby("regiao", as_index=False)["pessoas"]
    .sum()
    .sort_values("pessoas", ascending=False)
)
fig = px.bar(
    por_regiao,
    x="regiao",
    y="pessoas",
    title="Desaparecidas por região",
    labels={"pessoas": "Pessoas", "regiao": "Região"},
)
col2.plotly_chart(rotular(fig, "y"), width="stretch")

col3, col4 = st.columns(2)
por_sexo = desap.groupby("sexo", as_index=False)["pessoas"].sum()
fig = px.bar(
    por_sexo,
    x="sexo",
    y="pessoas",
    title="Desaparecidas por sexo",
    labels={"pessoas": "Pessoas", "sexo": "Sexo"},
)
col3.plotly_chart(rotular(fig, "y"), width="stretch")

nomes_faixa = {
    "0 a 17 anos": "Crianças e adolescentes (0 a 17)",
    "18 anos ou mais": "Adultos (18 ou mais)",
    "Não informada": "Idade não informada",
}
por_faixa = desap.groupby("faixa_etaria", as_index=False)["pessoas"].sum()
por_faixa["faixa"] = por_faixa["faixa_etaria"].map(nomes_faixa).fillna(
    por_faixa["faixa_etaria"]
)
total_faixa = por_faixa["pessoas"].sum()


def rotulo_faixa(linha):
    pct = f"{linha['pessoas'] / total_faixa * 100:.1f}".replace(".", ",")
    return f"{fmt(linha['pessoas'])} ({pct}%)"


por_faixa["rotulo"] = por_faixa.apply(rotulo_faixa, axis=1)
fig = px.bar(
    por_faixa,
    x="faixa",
    y="pessoas",
    text="rotulo",
    title="Desaparecidas por faixa etária",
    labels={"pessoas": "Pessoas", "faixa": "Faixa etária"},
)
fig.update_traces(textposition="outside", cliponaxis=False)
fig.update_layout(separators=",.", margin=dict(t=80))
col4.plotly_chart(fig, width="stretch")

st.caption(
    "Fonte: arquivo CSV do Sinesp obtido em sumidospb.com.br. "
    "Pessoas localizadas em um ano não são necessariamente as que desapareceram no mesmo ano."
)

# Para rodar no terminal:
#python -m streamlit run app.py