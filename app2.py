import streamlit as st
import pandas as pd
import requests

# Definir los endpoints
BASE_URL = "http://127.0.0.1:3000/api"

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
            # Asegúrate de que 'ultimoPrecio' esté presente en la respuesta
            ultimo_precio = cotizacion.get("ultimoPrecio", "No disponible")  # Cambiado aquí
            return {"ultimo_precio": ultimo_precio}  # Devolver en un dict para consistencia
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
        # Convertir las opciones en un DataFrame
        df = pd.DataFrame(opciones)

        # Extraer 'cierreAnterior' y 'ultimoPrecio' desde la columna 'cotizacion'
        if 'cotizacion' in df.columns:
            df['cierreAnterior'] = df['cotizacion'].apply(lambda x: x.get('cierreAnterior') if isinstance(x, dict) else None)
            df['ultimoPrecio'] = df['cotizacion'].apply(lambda x: x.get('ultimoPrecio') if isinstance(x, dict) else None)

        # Filtrar las columnas que queremos mostrar: cierreAnterior, simbolo, tipoOpcion, ultimoPrecio
        columnas_a_mostrar = ['cierreAnterior', 'simbolo', 'tipoOpcion', 'ultimoPrecio']

        # Verificar si las columnas existen antes de mostrar
        columnas_disponibles = [col for col in columnas_a_mostrar if col in df.columns]

        if columnas_disponibles:
            df_filtrado = df[columnas_disponibles]
            st.write(f"Mostrando todas las opciones de tipo {tipo_opcion}")
            st.dataframe(df_filtrado)  # Mostrar todas las filas sin limitación
        else:
            st.error("No se encontraron las columnas esperadas en la respuesta de la API.")

# Botón para obtener la cotización
if st.button("Mostrar Cotización"):
    cotizacion = obtener_cotizacion(mercado, simbolo)

    if cotizacion:
        # Extraer y mostrar el valor "ultimoPrecio" dentro de la cotización
        ultimo_precio = cotizacion.get("ultimo_precio", "No disponible")  # Cambiado aquí
        st.write(f"Último Precio: {ultimo_precio}")  # Cambiado aquí
