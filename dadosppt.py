import streamlit as st
import random
from collections import Counter
import pandas as pd

st.title("simulador: piedra, papel o tijera (dos dados)")

default_text = "Piedra\nPiedra\nPapel\nPapel\nTijera\nTijera"
opciones_validas = {"piedra", "papel", "tijera"}

col1, col2 = st.columns(2)

with col1:
    texto_dado1 = st.text_area("Dado 1", value=default_text, height=170)

with col2:
    texto_dado2 = st.text_area("Dado 2", value=default_text, height=170)

def procesar(texto):
    return [line.strip() for line in texto.split("\n") if line.strip() != ""]

caras1 = procesar(texto_dado1)
caras2 = procesar(texto_dado2)

def validar(caras):
    return (
        len(caras) == 6 and
        all(c.lower() in opciones_validas for c in caras)
    )

valido = validar(caras1) and validar(caras2)

if not valido:
    st.info("Cada dado debe tener 6 líneas y solo usar: Piedra, Papel o Tijera.")

n = st.number_input("Cantidad de tiradas", min_value=1, value=10, step=1)

def gana(a, b):
    a = a.lower()
    b = b.lower()
    if a == b:
        return 0
    if (a == "piedra" and b == "tijera") or \
       (a == "tijera" and b == "papel") or \
       (a == "papel" and b == "piedra"):
        return 1
    return -1

if st.button("Tirar", disabled=not valido):
    resultados1 = []
    resultados2 = []
    
    g1 = g2 = emp = 0

    for _ in range(n):
        r1 = random.choice(caras1)
        r2 = random.choice(caras2)
        
        resultados1.append(r1)
        resultados2.append(r2)

        res = gana(r1, r2)
        if res == 1:
            g1 += 1
        elif res == -1:
            g2 += 1
        else:
            emp += 1

    # Conteos por dado
    c1 = Counter(resultados1)
    c2 = Counter(resultados2)

    df = pd.DataFrame({
        "Resultado": ["Piedra", "Papel", "Tijera"],
        "Dado 1": [c1.get("Piedra", 0), c1.get("Papel", 0), c1.get("Tijera", 0)],
        "Dado 2": [c2.get("Piedra", 0), c2.get("Papel", 0), c2.get("Tijera", 0)],
    })

    st.write("Frecuencias:")
    st.dataframe(df, hide_index=True)

    st.write("Victorias:")
    st.write(f"Dado 1: {g1}")
    st.write(f"Dado 2: {g2}")
    st.write(f"Empates: {emp}")
