import numpy as np
import matplotlib.pyplot as plt

# Función para calcular el payoff de la opción Call
def call_option_payoff(underlying_price, strike_price, option_price, num_contracts, contract_multiplier):
    payoff = (np.maximum(underlying_price - strike_price, 0) - option_price) * num_contracts * contract_multiplier
    return payoff

# Función para calcular el payoff de la opción Put
def put_option_payoff(underlying_price, strike_price, option_price, num_contracts, contract_multiplier):
    payoff = (np.maximum(strike_price - underlying_price, 0) - option_price) * num_contracts * contract_multiplier
    return payoff

# Ingreso de variables por el usuario para la opción Call
strike_price_call = float(input("Ingrese el precio de ejercicio (strike price) de la opción Call: "))
option_price_call = float(input("Ingrese el precio de la opción Call: "))
num_contracts_call = int(input("Ingrese el número de contratos de la opción Call: "))

# Ingreso de variables por el usuario para la opción Put
strike_price_put = float(input("Ingrese el precio de ejercicio (strike price) de la opción Put: "))
option_price_put = float(input("Ingrese el precio de la opción Put: "))
num_contracts_put = int(input("Ingrese el número de contratos de la opción Put: "))

contract_multiplier = 100  # Usualmente es 100 para opciones estándar

# Ajustar el rango de precios subyacentes de forma dinámica
lower_bound = max(0, min(strike_price_call, strike_price_put) - 20)  # Límite inferior basado en el strike más bajo
upper_bound = max(strike_price_call, strike_price_put) + 20  # Límite superior basado en el strike más alto

# Generar un rango de precios subyacentes en función de los precios de ejercicio
underlying_prices = np.arange(lower_bound, upper_bound, 0.1)

# Calcular los payoffs correspondientes
call_payoffs = call_option_payoff(underlying_prices, strike_price_call, option_price_call, num_contracts_call, contract_multiplier)
put_payoffs = put_option_payoff(underlying_prices, strike_price_put, option_price_put, num_contracts_put, contract_multiplier)

# Graficar el diagrama de payoff para Call y Put
plt.figure(figsize=(10, 6))
plt.plot(underlying_prices, call_payoffs, label="Payoff Opción Call", color="blue")
plt.plot(underlying_prices, put_payoffs, label="Payoff Opción Put", color="green")
plt.axhline(0, color='black', linewidth=1)
plt.axvline(x=strike_price_call, color='red', linestyle='--', label=f"Strike Call = {strike_price_call}")
plt.axvline(x=strike_price_put, color='orange', linestyle='--', label=f"Strike Put = {strike_price_put}")

# Ajustar los límites del gráfico
plt.xlim(lower_bound, upper_bound)
plt.ylim(min(min(call_payoffs), min(put_payoffs)) - 50, max(max(call_payoffs), max(put_payoffs)) + 50)

# Etiquetas y leyenda
plt.title("Diagrama de Payoff de Opciones Call y Put")
plt.xlabel("Precio del Subyacente")
plt.ylabel("Ganancia / Pérdida")
plt.legend()
plt.grid(True)
plt.show()
