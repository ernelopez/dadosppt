import streamlit as st
import random
from collections import Counter
import pandas as pd

st.title("Simulador de tiradas de dados: piedra, papel o tijera")

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

    if (
        (a == "piedra" and b == "tijera") or
        (a == "tijera" and b == "papel") or
        (a == "papel" and b == "piedra")
    ):
        return 1

    return -1


if st.button("Tirar", disabled=not valido):

    resultados1 = []
    resultados2 = []

    g1 = 0
    g2 = 0
    emp = 0

    partidas = []

    for i in range(1, n + 1):

        r1 = random.choice(caras1)
        r2 = random.choice(caras2)

        resultados1.append(r1)
        resultados2.append(r2)

        res = gana(r1, r2)

        if res == 1:
            g1 += 1
            resultado = "Dado 1"

        elif res == -1:
            g2 += 1
            resultado = "Dado 2"

        else:
            emp += 1
            resultado = "Empate"

        prop_g1 = g1 / i
        prop_g2 = g2 / i
        prop_emp = emp / i

        if g1 + g2 > 0:
            prop_g1_sin_emp = g1 / (g1 + g2)
        else:
            prop_g1_sin_emp = 0

        partidas.append({
            "Partida": i,
            "Ganador": resultado,
            "Ganadas dado 1": g1,
            "Ganadas dado 2": g2,
            "Empates": emp,
            "Prop. dado 1": prop_g1,
            "Prop. dado 2": prop_g2,
            "Prop. empates": prop_emp,
            "Prop. G1 sin emp.": prop_g1_sin_emp
        })

    # Conteos por dado
    c1 = Counter(resultados1)
    c2 = Counter(resultados2)

    df = pd.DataFrame({
        "Resultado": ["Piedra", "Papel", "Tijera"],
        "Dado 1": [
            c1.get("Piedra", 0),
            c1.get("Papel", 0),
            c1.get("Tijera", 0)
        ],
        "Dado 2": [
            c2.get("Piedra", 0),
            c2.get("Papel", 0),
            c2.get("Tijera", 0)
        ],
    })

    st.write("Frecuencias:")
    st.dataframe(df, hide_index=True)

    st.write(f"Victorias Dado 1: {g1}")
    st.write(f"Victorias Dado 2: {g2}")
    st.write(f"Empates: {emp}")

    st.write("Detalle de tiradas:")

    df_partidas = pd.DataFrame(partidas)

    st.dataframe(
        df_partidas,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Partida": st.column_config.NumberColumn(width="small"),
            "Ganador": st.column_config.TextColumn(width="small"),
            "Gan. dado 1": st.column_config.NumberColumn(width="small"),
            "Gan. dado 2": st.column_config.NumberColumn(width="small"),
            "Empates": st.column_config.NumberColumn(width="small"),
            "Prop. dado 1": st.column_config.NumberColumn(
                "Prop. dado 1",
                format="%.3f",
                width="small",
            ),
            "Prop. dado 2": st.column_config.NumberColumn(
                "Prop. dado 2",
                format="%.3f",
                width="small",
            ),
            "Prop. empates": st.column_config.NumberColumn(
                "Prop. emp.",
                format="%.3f",
                width="small",
            ),
            "Prop. G1 sin emp.": st.column_config.NumberColumn(
                "Prop. G1\nsin emp.",
                format="%.3f",
                width="small",
            ),
        },
    )
