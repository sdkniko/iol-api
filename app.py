import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Función para calcular el payoff de la opción Call
def call_option_payoff(underlying_price, strike_price, option_price, num_contracts, contract_multiplier):
    payoff = (np.maximum(underlying_price - strike_price, 0) - option_price) * num_contracts * contract_multiplier
    return payoff

# Función para calcular el payoff de la opción Put
def put_option_payoff(underlying_price, strike_price, option_price, num_contracts, contract_multiplier):
    payoff = (np.maximum(strike_price - underlying_price, 0) - option_price) * num_contracts * contract_multiplier
    return payoff

# Configuración de la página de la aplicación web
st.title("Diagrama de Payoff de Opciones Call y Put")
st.write("Ingrese los valores para las opciones Call y Put para ver el gráfico interactivo.")

# Entradas del usuario para la opción Call
st.header("Parámetros de la opción Call")
strike_price_call = st.number_input("Precio de Ejercicio (Strike Price) de la opción Call:", min_value=0.0, value=45.0)
option_price_call = st.number_input("Precio de la opción Call:", min_value=0.0, value=2.88)
num_contracts_call = st.number_input("Número de contratos de la opción Call:", min_value=1, value=1)

# Entradas del usuario para la opción Put
st.header("Parámetros de la opción Put")
strike_price_put = st.number_input("Precio de Ejercicio (Strike Price) de la opción Put:", min_value=0.0, value=40.0)
option_price_put = st.number_input("Precio de la opción Put:", min_value=0.0, value=2.45)
num_contracts_put = st.number_input("Número de contratos de la opción Put:", min_value=1, value=1)

contract_multiplier = 100  # Usualmente es 100 para opciones estándar

# Generar un rango de precios subyacentes en función de los precios de ejercicio
lower_bound = max(0, min(strike_price_call, strike_price_put) - 20)  # Límite inferior basado en el strike más bajo
upper_bound = max(strike_price_call, strike_price_put) + 20  # Límite superior basado en el strike más alto
underlying_prices = np.arange(lower_bound, upper_bound, 0.1)

# Calcular los payoffs correspondientes
call_payoffs = call_option_payoff(underlying_prices, strike_price_call, option_price_call, num_contracts_call, contract_multiplier)
put_payoffs = put_option_payoff(underlying_prices, strike_price_put, option_price_put, num_contracts_put, contract_multiplier)

# Crear el gráfico con Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(underlying_prices, call_payoffs, label="Payoff Opción Call", color="blue")
ax.plot(underlying_prices, put_payoffs, label="Payoff Opción Put", color="green")
ax.axhline(0, color='black', linewidth=1)
ax.axvline(x=strike_price_call, color='red', linestyle='--', label=f"Strike Call = {strike_price_call}")
ax.axvline(x=strike_price_put, color='orange', linestyle='--', label=f"Strike Put = {strike_price_put}")

# Ajustar los límites del gráfico
ax.set_xlim(lower_bound, upper_bound)
ax.set_ylim(min(min(call_payoffs), min(put_payoffs)) - 50, max(max(call_payoffs), max(put_payoffs)) + 50)

# Etiquetas y leyenda
ax.set_title("Diagrama de Payoff de Opciones Call y Put")
ax.set_xlabel("Precio del Subyacente")
ax.set_ylabel("Ganancia / Pérdida")
ax.legend()
ax.grid(True)

# Mostrar el gráfico en la aplicación web
st.pyplot(fig)
