import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

st.title("Simulador D'aeronaus")

avio_seleccionat = st.selectbox("Tria l'avió:", avions_df["nom"])
velocitat_max = int(avions_df[avions_df["nom"]==avio_seleccionat]["velocitat_max"])
velocitat = st.slider("Velocitat (m/s)", 0, velocitat_max, velocitat_max)

dades = avions_df[avions_df["nom"]==avio_seleccionat].iloc[0]
rho, S, CL, m, mida = 1.225, dades["area_ala"], dades["coef_sustentacio"], dades["massa"], dades["longitud"]/20

L = 0.5 * rho * velocitat**2 * S * CL
W = m * 9.81
T = 200 * velocitat
D = 0.5 * rho * velocitat**2 * S * 0.02

angle = -0.3 if L < W else max(min((T - D) * 0.00000002, 0.4), -0.4)

fig = plt.figure(figsize=(6,5))
ax = fig.add_subplot(111, projection="3d")
ax.set_box_aspect([1,1,1])

rot = np.array([
    [np.cos(angle),0,np.sin(angle)],
    [0,1,0],
    [-np.sin(angle),0,np.cos(angle)]
])

fuselatge = np.array([[-2*mida,0,0],[2*mida,0,0]]) @ rot.T
ax.plot(fuselatge[:,0], fuselatge[:,1], fuselatge[:,2], color="gray", linewidth=6)

alas = np.array([[0,-3*mida,0],[0,3*mida,0]]) @ rot.T
ax.plot(alas[:,0], alas[:,1], alas[:,2], color="gray", linewidth=6)

cola = np.array([[-1.5*mida,0,0],[-2.2*mida,0,1*mida]]) @ rot.T
ax.plot(cola[:,0], cola[:,1], cola[:,2], color="gray", linewidth=4)

vec_L = np.array([0,0,L]) @ rot.T
vec_W = np.array([0,0,-W]) @ rot.T
vec_T = np.array([T,0,0]) @ rot.T if T-D>=0 else np.array([-T,0,0]) @ rot.T
vec_D = np.array([-D,0,0]) @ rot.T if T-D>=0 else np.array([D,0,0]) @ rot.T

escala = mida / max(L, W, abs(T), D, 1) * 5

ax.quiver(0,0,0, vec_L[0]*escala, vec_L[1]*escala, vec_L[2]*escala, color="blue", linewidth=3)
ax.quiver(0,0,0, vec_W[0]*escala, vec_W[1]*escala, vec_W[2]*escala, color="red", linewidth=3)
ax.quiver(0,0,0, vec_T[0]*escala, vec_T[1]*escala, vec_T[2]*escala, color="purple", linewidth=3)
ax.quiver(0,0,0, vec_D[0]*escala, vec_D[1]*escala, vec_D[2]*escala, color="green", linewidth=3)

ax.set_xlim(-6*mida,6*mida)
ax.set_ylim(-6*mida,6*mida)
ax.set_zlim(-6*mida,6*mida)

estat_vertical = "Vola" if L >= W else "No vola"
ax.set_title(f"{avio_seleccionat}\n{estat_vertical}\nL={L:.0f}N  W={W:.0f}N  T={T:.0f}N  D={D:.0f}N", fontsize=12)

st.pyplot(fig)