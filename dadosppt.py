
import streamlit as st
import random
from collections import Counter
import pandas as pd

st.set_page_config(page_title="Simulador P-P-T", page_icon="🎲", layout="wide")

st.title("🎲 Simulador de tiradas de dados: Piedra, Papel o Tijera")
st.markdown("Elegí las seis caras de cada dado y simulá tantas partidas como quieras.")

opciones = ["🪨 Piedra","📄 Papel","✂️ Tijera"]
mapa = {"🪨 Piedra":"Piedra","📄 Papel":"Papel","✂️ Tijera":"Tijera"}

default=["🪨 Piedra","🪨 Piedra","📄 Papel","📄 Papel","✂️ Tijera","✂️ Tijera"]

c1,c2=st.columns(2)
caras1=[];caras2=[]
with c1:
    st.subheader("🔷 Dado 1")
    for i,d in enumerate(default):
        caras1.append(mapa[st.selectbox(f"Cara {i+1}",opciones,index=opciones.index(d),key=f"a{i}")])
with c2:
    st.subheader("🔶 Dado 2")
    for i,d in enumerate(default):
        caras2.append(mapa[st.selectbox(f"Cara {i+1}",opciones,index=opciones.index(d),key=f"b{i}")])

n=st.number_input("Cantidad de tiradas",1,1000000,100,1)

def gana(a,b):
    if a==b:return 0
    if (a,b) in [("Piedra","Tijera"),("Tijera","Papel"),("Papel","Piedra")]:
        return 1
    return -1

if st.button("🎲 Tirar"):
    g1=g2=emp=0
    res1=[];res2=[];partidas=[]
    prog=st.progress(0)
    for i in range(1,n+1):
        a=random.choice(caras1);b=random.choice(caras2)
        res1.append(a);res2.append(b)
        r=gana(a,b)
        if r==1:
            g1+=1;gan="🔷 Dado 1"
        elif r==-1:
            g2+=1;gan="🔶 Dado 2"
        else:
            emp+=1;gan="🤝 Empate"
        p1=g1/i;p2=g2/i;pe=emp/i
        ps=g1/(g1+g2) if g1+g2 else 0
        partidas.append({"Partida":i,"Ganador":gan,
        "Ganadas dado 1":g1,"Ganadas dado 2":g2,"Empates":emp,
        "Proporción 🔷":p1,"Proporción 🔶":p2,
        "Proporción empates":pe,"Proporción 🔷 sin empates":ps})
        if n<=1000 or i%(max(1,n//200))==0:
            prog.progress(i/n)
    prog.empty()
    cc1,cc2,cc3=st.columns(3)
    cc1.metric("🔷 Victorias dado 1", g1)
    cc2.metric("🔶 Victorias dado 2", g2)
    cc3.metric("🤝 Empates",emp)
    c1=Counter(res1);c2=Counter(res2)
    st.subheader("Frecuencias")
    st.dataframe(pd.DataFrame({
        "Resultado":["Piedra","Papel","Tijera"],
        "Dado 1":[c1["Piedra"],c1["Papel"],c1["Tijera"]],
        "Dado 2":[c2["Piedra"],c2["Papel"],c2["Tijera"]]
    }),hide_index=True,use_container_width=True)
    df=pd.DataFrame(partidas)
    st.subheader("Evolución de las proporciones")
    #st.line_chart(df.set_index("Partida")[["Proporción 🔷","Proporción 🔶","Proporción empates"]])
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=df["Partida"],
            y=df["Proporción 🔷"],
            mode="lines",
            name="🔷 Dado 1",
            line=dict(color="royalblue", width=3),
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=df["Partida"],
            y=df["Proporción 🔶"],
            mode="lines",
            name="🔶 Dado 2",
            line=dict(color="darkorange", width=3),
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=df["Partida"],
            y=df["Proporción empates"],
            mode="lines",
            name="🤝 Empates",
            line=dict(color="forestgreen", width=3),
        )
    )
    
    fig.update_layout(
        xaxis_title="Partida",
        yaxis_title="Proporción",
        yaxis=dict(range=[0, 1]),
        legend_title="",
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Detalle de tiradas")
    st.dataframe(df,hide_index=True,use_container_width=True,
        column_config={
            "Proporción dado 1":st.column_config.NumberColumn(format="%.3f"),
            "Proporción dado 2":st.column_config.NumberColumn(format="%.3f"),
            "Proporción empates":st.column_config.NumberColumn(format="%.3f"),
            "Proporción G1 sin empates":st.column_config.NumberColumn(format="%.3f"),
        })
