import streamlit as st
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt

# Definir los endpoints
BASE_URL = "http://127.0.0.1:3000/api"




# Funciones para calcular ganancias y pérdidas
def long_call(ST, X, c0):
    return np.maximum(0, ST - X) - c0

def short_call(ST, X, c0):
    return -np.maximum(0, ST - X) + c0

def long_put(ST, X, p0):
    return np.maximum(0, X - ST) - p0

def short_put(ST, X, p0):
    return -np.maximum(0, X - ST) + p0

# Función para obtener las opciones (Call o Put)
def obtener_opciones(mercado, simbolo, tipo_opcion):
    url = f"{BASE_URL}/opciones/{mercado}/{simbolo}/{tipo_opcion}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener opciones: {response.json().get('error')}")
            return []
    except Exception as e:
        st.error(f"Error al conectar con el servidor: {e}")
        return []

# Función para obtener la cotización
def obtener_cotizacion(mercado, simbolo):
    url = f"{BASE_URL}/cotizacion/{mercado}/{simbolo}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            cotizacion = response.json()
            ultimo_precio = cotizacion.get("ultimoPrecio", "No disponible")
            return {"ultimo_precio": ultimo_precio}
        else:
            st.error(f"Error al obtener cotización: {response.json().get('error')}")
            return None
    except Exception as e:
        st.error(f"Error al conectar con el servidor: {e}")
        return None

# Título de la app
st.title("Opciones: Call & Put")

# Input del usuario para elegir el mercado y el símbolo
mercado = st.text_input("Mercado", value="bcba")
simbolo = st.text_input("Símbolo", value="GGAL")

# Seleccionar el tipo de opción (Call o Put)
tipo_opcion = st.selectbox("Selecciona el tipo de opción", ["Call", "Put"])

# Botón para obtener las opciones
if st.button("Mostrar Opciones"):
    opciones = obtener_opciones(mercado, simbolo, tipo_opcion)

    if opciones:
        df = pd.DataFrame(opciones)

        if 'cotizacion' in df.columns:
            df['cierreAnterior'] = df['cotizacion'].apply(lambda x: x.get('cierreAnterior') if isinstance(x, dict) else None)
            df['ultimoPrecio'] = df['cotizacion'].apply(lambda x: x.get('ultimoPrecio') if isinstance(x, dict) else None)

        columnas_a_mostrar = ['cierreAnterior', 'simbolo', 'tipoOpcion', 'ultimoPrecio']
        columnas_disponibles = [col for col in columnas_a_mostrar if col in df.columns]

        if columnas_disponibles:
            df_filtrado = df[columnas_disponibles]
            st.write(f"Mostrando todas las opciones de tipo {tipo_opcion}")
            st.dataframe(df_filtrado)
        else:
            st.error("No se encontraron las columnas esperadas en la respuesta de la API.")

# Botón para obtener la cotización
if st.button("Mostrar Cotización"):
    cotizacion = obtener_cotizacion(mercado, simbolo)

    if cotizacion:
        ultimo_precio = cotizacion.get("ultimo_precio", "No disponible")
        st.write(f"Último Precio: {ultimo_precio}")

# Parte de la calculadora de opciones
st.header("Calculadora de Opciones")

# Selector para elegir el tipo de opción para el cálculo
option_type = st.selectbox("Selecciona el tipo de opción para cálculo", ("Long Call", "Short Call", "Long Put", "Short Put"))

# Entradas para los parámetros de la opción
X = st.number_input("Precio de ejercicio (X)", min_value=0.0, value=100.0)
premium = st.number_input("Prima de la opción", min_value=0.0, value=10.0)
ST = np.arange(0, 200, 1)  # Precio del activo subyacente (S_T)

# Calcular ganancias/pérdidas según el tipo de opción seleccionada
if option_type == "Long Call":
    profits = long_call(ST, X, premium)
    label = "Long Call"
elif option_type == "Short Call":
    profits = short_call(ST, X, premium)
    label = "Short Call"
elif option_type == "Long Put":
    profits = long_put(ST, X, premium)
    label = "Long Put"
else:  # Short Put
    profits = short_put(ST, X, premium)
    label = "Short Put"

# Graficar resultados
plt.figure(figsize=(10, 6))
plt.plot(ST, profits, label=label, color='blue')
plt.axhline(0, color='black', lw=1, ls='--')
plt.axvline(X, color='red', lw=1, ls='--', label='Strike Price (X)')
plt.title(f'Ganancias/Pérdidas para {label}')
plt.xlabel('Precio del activo subyacente (S_T)')
plt.ylabel('Ganancia/Pérdida')
plt.legend()
plt.grid()

# Ajustar límites dinámicamente
plt.xlim(0, max(ST))
plt.ylim(min(profits) - 10, max(profits) + 10)

st.pyplot(plt)
