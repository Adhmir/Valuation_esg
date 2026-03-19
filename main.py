import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Valuation ESG (FCFE)", layout="centered")

# =========================
# PARÂMETROS PADRÃO
# =========================
DEFAULTS = {
    "beta": 1.1,
    "rf": 0.05,
    "market_premium": 0.06,
    "g_base": 0.03,
    "g_esg_coef": 0.02,
    "g_terminal": 0.025
}

# =========================
# FUNÇÕES
# =========================
def cost_of_equity(rf, beta, market_premium):
    return rf + beta * market_premium

def estimate_growth(esg, g_base, g_esg_coef):
    g_esg = g_esg_coef * (esg / 100)
    g_total = g_base + g_esg
    return g_total, g_esg

def project_fcfe(fcfe_0, g, n=5):
    return [fcfe_0 * (1 + g)**t for t in range(1, n+1)]

def fcfe_valuation(fcfe, ke, g_terminal):
    value = 0
    for t, f in enumerate(fcfe, start=1):
        value += f / ((1 + ke)**t)
    
    terminal = fcfe[-1] * (1 + g_terminal) / (ke - g_terminal)
    terminal /= (1 + ke)**len(fcfe)
    
    return value + terminal

# =========================
# TÍTULO
# =========================
st.title("Valuation com ESG baseado em FCFE")

# =========================
# INPUTS PRINCIPAIS
# =========================
st.subheader("Entradas")

fcfe = st.number_input("Fluxo de Caixa Livre ao Acionista (FCFE₀)", value=1000.0)
esg = st.slider("Score ESG", 0, 100, 50)

# =========================
# PARÂMETROS (OCULTO)
# =========================
with st.expander("Parâmetros do Modelo"):

    beta = st.number_input("Beta", value=DEFAULTS["beta"])
    rf = st.number_input("Taxa livre de risco", value=DEFAULTS["rf"])
    market_premium = st.number_input("Prêmio de mercado", value=DEFAULTS["market_premium"])

    g_base = st.number_input("Crescimento base", value=DEFAULTS["g_base"])
    g_esg_coef = st.number_input("Coeficiente ESG", value=DEFAULTS["g_esg_coef"])

    g_terminal = st.number_input("Crescimento terminal", value=DEFAULTS["g_terminal"])

# =========================
# CÁLCULOS
# =========================
ke = cost_of_equity(rf, beta, market_premium)
g_total, g_esg = estimate_growth(esg, g_base, g_esg_coef)

# Validação
if ke <= g_terminal:
    st.error("Ke deve ser maior que o crescimento terminal")
    st.stop()

fcfe_proj = project_fcfe(fcfe, g_total)
value = fcfe_valuation(fcfe_proj, ke, g_terminal)

# =========================
# RESULTADO PRINCIPAL
# =========================
st.markdown("## Valor da Empresa")
st.metric(label="Valor estimado", value=f"{value:,.2f}")

# =========================
# DETALHES
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Crescimento")
    st.write(f"Total: {g_total:.2%}")
    st.write(f"Base: {g_base:.2%}")
    st.write(f"ESG: {g_esg:.2%}")

with col2:
    st.subheader("Custo de Capital")
    st.write(f"Ke: {ke:.2%}")

# =========================
# PROJEÇÃO
# =========================
st.subheader("Projeção do FCFE")
st.line_chart(fcfe_proj)

# =========================
# EQUAÇÕES
# =========================
st.markdown("---")
st.subheader("Equações do Modelo")

st.markdown("### Custo de Capital (CAPM)")
:contentReference[oaicite:0]{index=0}

st.markdown("### Crescimento com ESG")
:contentReference[oaicite:1]{index=1}

st.markdown("### Projeção do FCFE")
:contentReference[oaicite:2]{index=2}

st.markdown("### Valuation")
:contentReference[oaicite:3]{index=3}
