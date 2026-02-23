import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

st.set_page_config(page_title="Simulador d'aeronaus", layout="wide")

avions_df = pd.DataFrame({
    "nom": ["Cessna172", "Boeing747", "AirbusA320", "Stuka", "B29", "F16"],
    "categoria": ["Civil", "Civil", "Civil", "Militar", "Militar", "Militar"],
    "densitat_aire": [1.225]*6,
    "area_ala": [16.2, 511, 122.6, 30, 160, 27],
    "longitud": [8, 70, 37, 9, 30, 15],
    "velocitat_max": [70, 250, 230, 200, 220, 300],
    "massa": [1150, 183500, 73500, 3500, 29000, 9000],
    "coef_sustentacio": [1.2, 1.5, 1.4, 1.3, 1.4, 1.3]
})

st.title("Simulador d'aeronaus")

col1, col2 = st.columns([1,2])

with col1:
    avion_seleccionat = st.selectbox("Selecciona un avion", avions_df["nom"])
    velocitat = st.slider("Velocitat (m/s)", 0, int(avions_df[avions_df["nom"]==avion_seleccionat]["velocitat_max"].values[0]),
                          int(avions_df[avions_df["nom"]==avion_seleccionat]["velocitat_max"].values[0]/2))

def calcular_vectors(avion, v):
    dades = avions_df[avions_df["nom"]==avion].iloc[0]
    rho, S, CL, m, tam = dades["densitat_aire"], dades["area_ala"], dades["coef_sustentacio"], dades["massa"], dades["longitud"]/20
    L = 0.5 * rho * v**2 * S * CL
    W = m * 9.81
    T = 0.5 * v * 2000
    D = 50000
    inclinacio = 0.2 if L >= W else -0.2
    return L, W, T, D, tam, inclinacio

L, W, T, D, tam, inclinacio = calcular_vectors(avion_seleccionat, velocitat)

fig = go.Figure()


fuselatge_x = [-2*tam, 2*tam]
fuselatge_y = [0,0]
fuselatge_z = [0,0]
fig.add_trace(go.Scatter3d(x=fuselatge_x, y=fuselatge_y, z=fuselatge_z, mode="lines",
                           line=dict(color="gray", width=6), name="Fuselatge"))

alas_x = [0,0]
alas_y = [-3*tam,3*tam]
alas_z = [0,0]
fig.add_trace(go.Scatter3d(x=alas_x, y=alas_y, z=alas_z, mode="lines",
                           line=dict(color="gray", width=6), name="Ales"))


escala = tam / max(L, W, T, D) * 5
fig.add_trace(go.Cone(x=[0], y=[0], z=[0], u=[0], v=[0], w=[L*escala], sizemode="absolute",
                      anchor="tail", colorscale=[[0,"blue"],[1,"blue"]], showscale=False, name="Sustentació"))
fig.add_trace(go.Cone(x=[0], y=[0], z=[0], u=[0], v=[0], w=[-W*escala], sizemode="absolute",
                      anchor="tail", colorscale=[[0,"red"],[1,"red"]], showscale=False, name="Pes"))
fig.add_trace(go.Cone(x=[0], y=[0], z=[0], u=[T*escala], v=[0], w=[0], sizemode="absolute",
                      anchor="tail", colorscale=[[0,"purple"],[1,"purple"]], showscale=False, name="Empuje"))
fig.add_trace(go.Cone(x=[0], y=[0], z=[0], u=[-D*escala], v=[0], w=[0], sizemode="absolute",
                      anchor="tail", colorscale=[[0,"green"],[1,"green"]], showscale=False, name="Drag"))

fig.update_layout(scene=dict(
    xaxis=dict(range=[-5*tam,5*tam], visible=False),
    yaxis=dict(range=[-5*tam,5*tam], visible=False),
    zaxis=dict(range=[-5*tam,5*tam], visible=False)
),
                  margin=dict(l=0,r=0,b=0,t=0),
                  showlegend=True)

with col2:
    st.plotly_chart(fig, use_container_width=True)
    st.write(f"Sustentació: {L:.0f} N, Pes: {W:.0f} N, Empuje: {T:.0f} N, Drag: {D:.0f} N")
