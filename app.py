import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração da Página
st.set_page_config(
    page_title="Water Quality & Compliance Dashboard",
    page_icon="💧",
    layout="wide"
)

# Título do Dashboard
st.title("💧 Water Quality & Compliance Dashboard")
st.markdown("""
Interactive dashboard designed to monitor water quality parameters (pH, Turbidity, and Bacteriological Contamination) 
in compliance with **Good Laboratory Practices (GLP)** and standard regulatory limits. Developed for environmental data analysis.
""")

# Simulando dados de monitoramento (baseados em rotinas laboratoriais reais)
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", end="2026-10-01", freq="D")
    data = pd.DataFrame({
        'Date': dates,
        'Station': np.choice(['Station A - Intake', 'Station B - Treatment Plant', 'Station C - Distribution'], size=len(dates)),
        'pH': np.random.normal(7.2, 0.4, len(dates)),
        'Turbidity_NTU': np.random.exponential(1.5, len(dates)),
        'Bacteriological_Status': np.random.choice(['Safe / Absent', 'Alert / Present'], size=len(dates), p=[0.92, 0.08])
    })
    return data

df = load_data()

# Filtros na Barra Lateral (Sidebar)
st.sidebar.header("Filter Options")
selected_station = st.sidebar.selectbox("Select Monitoring Station", df['Station'].unique())

filtered_df = df[df['Station'] == selected_station]

# Métricas principais no topo
col1, col2, col3 = st.columns(3)
col1.metric("Total Samples Analyzed", len(filtered_df))
col2.metric("Average pH", round(filtered_df['pH'].mean(), 2))
col3.metric("Average Turbidity (NTU)", round(filtered_df['Turbidity_NTU'].mean(), 2))

st.markdown("---")

# Gráficos interativos
st.subheader(f"Parameter Trends for {selected_station}")

col_g1, col_g2 = st.columns(2)

with col_g1:
    fig_ph = px.line(filtered_df, x='Date', y='pH', title="pH Levels Over Time", markers=True)
    fig_ph.add_hline(y=6.5, line_dash="dash", line_color="red", annotation_text="Min pH Limit")
    fig_ph.add_hline(y=8.5, line_dash="dash", line_color="red", annotation_text="Max pH Limit")
    st.plotly_chart(fig_ph, use_container_width=True)

with col_g2:
    fig_turb = px.bar(filtered_df, x='Date', y='Turbidity_NTU', title="Turbidity Levels (NTU)")
    fig_turb.add_hline(y=4.0, line_dash="dash", line_color="orange", annotation_text="Max Limit")
    st.plotly_chart(fig_turb, use_container_width=True)

# Tabela de dados brutos
st.subheader("Raw Data & Traceability Table")
st.dataframe(filtered_df.tail(10))
