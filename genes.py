import streamlit as st
import pandas as pd
import itertools
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador Genético", layout="wide")

# --------------------------
# Funções básicas
# --------------------------

def gerar_gametas(genotipo):
    return list(genotipo)

def cruzar(pai1, pai2):
    gametas1 = gerar_gametas(pai1)
    gametas2 = gerar_gametas(pai2)

    combinacoes = []
    for g1 in gametas1:
        for g2 in gametas2:
            filho = "".join(sorted(g1 + g2))
            combinacoes.append(filho)

    df = pd.DataFrame(combinacoes, columns=["Genótipo"])

    # Probabilidade em percentual (%)
    prob = df["Genótipo"].value_counts(normalize=True).reset_index()
    prob.columns = ["Genótipo", "Probabilidade"]
    prob["Percentual"] = prob["Probabilidade"] * 100

    return prob

def cruzamento_encadeado(resultados1, resultados2):
    final_probs = {}

    for g1, p1 in resultados1.items():
        for g2, p2 in resultados2.items():
            inter = cruzar(g1, g2)
            for _, row in inter.iterrows():
                final_probs[row["Genótipo"]] = final_probs.get(row["Genótipo"], 0) + row["Probabilidade"] * p1 * p2

    df = pd.DataFrame(final_probs.items(), columns=["Genótipo", "Probabilidade"])
    df["Percentual"] = df["Probabilidade"] * 100
    df = df.sort_values("Genótipo")
    return df

# --------------------------
# Interface Streamlit
# --------------------------

st.title("🧬 Simulador de Cruzamentos Genéticos - By Marcinho")

st.header("1️⃣ Cruzamento Simples")

opcoes = {
    "AA × aa": ("AA", "aa"),
    "Aa × aa": ("Aa", "aa"),
    "Aa × Aa": ("Aa", "Aa"),
}

escolha = st.selectbox("Selecione o cruzamento:", list(opcoes.keys()))

p1, p2 = opcoes[escolha]
resultados = cruzar(p1, p2)

st.subheader(f"Resultado: {p1} × {p2}")
st.dataframe(resultados)

# --------------------------
# Gráfico de Percentuais
# --------------------------
st.subheader("Distribuição Percentual (%)")

fig, ax = plt.subplots()
ax.bar(resultados["Genótipo"], resultados["Percentual"])

# Rótulos de porcentagem acima de cada barra
for i, v in enumerate(resultados["Percentual"]):
    ax.text(i, v + 1, f"{v:.1f}%", ha="center", fontweight="bold")

ax.set_xlabel("Genótipo")
ax.set_ylabel("Percentual (%)")
st.pyplot(fig)

# --------------------------
# Cruzamento Encadeado
# --------------------------

st.header("2️⃣ Cruzamento Encadeado (Cruzar resultados entre si)")

escolha2 = st.selectbox("Selecione um segundo cruzamento:", list(opcoes.keys()), key="segunda")

p3, p4 = opcoes[escolha2]
resultados2 = cruzar(p3, p4)

st.subheader(f"Resultado do segundo: {p3} × {p4}")
st.dataframe(resultados2)

if st.button("🔁 Cruzar Resultado 1 com Resultado 2"):
    r1 = dict(zip(resultados["Genótipo"], resultados["Probabilidade"]))
    r2 = dict(zip(resultados2["Genótipo"], resultados2["Probabilidade"]))

    final = cruzamento_encadeado(r1, r2)

    st.subheader("Resultado Final do Cruzamento Encadeado (%)")
    st.dataframe(final)

    fig2, ax2 = plt.subplots()
    ax2.bar(final["Genótipo"], final["Percentual"])

    # Rótulos
    for i, v in enumerate(final["Percentual"]):
        ax2.text(i, v + 1, f"{v:.1f}%", ha="center", fontweight="bold")

    ax2.set_xlabel("Genótipo")
    ax2.set_ylabel("Percentual (%)")
    st.pyplot(fig2)
