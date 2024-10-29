from flask import Flask, jsonify, request, render_template
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app = Flask(__name__)

PORT = 3000
BEARER_TOKEN = ''  # Variable para almacenar el token Bearer

# Función para obtener el token Bearer
def obtener_token():
    global BEARER_TOKEN
    try:
        response = requests.post('https://api.invertironline.com/token', data={
            'username': 'sdkniko',
            'password': 'Niko2137!',
            'grant_type': 'password'
        })
        response.raise_for_status()
        BEARER_TOKEN = response.json()['access_token']
        print('Token obtenido:', BEARER_TOKEN)
    except requests.exceptions.RequestException as error:
        print(f'Error al obtener el token: {error}')

# Llamar a la función para obtener el token cuando se inicie el servidor
obtener_token()

# Nuevo endpoint que llama a la API de InvertirOnline
@app.route('/api/cotizacion/<mercado>/<simbolo>', methods=['GET'])
def obtener_cotizacion(mercado, simbolo):
    # Asegúrate de que no haya espacios en blanco adicionales
    mercado = mercado.strip()
    simbolo = simbolo.strip()

    # Construir la URL de la API
    url = f'https://api.invertironline.com/api/v2/{mercado}/Titulos/{simbolo}/Cotizacion'
    
    # Establecer los parámetros de la solicitud
    params = {
        'mercado': mercado,
        'simbolo': simbolo,
        'model.simbolo': simbolo,
        'model.mercado': mercado.lower(),
        'model.plazo': 't0'
    }

    try:
        # Realizar la solicitud a la API remota de InvertirOnline
        response = requests.get(url, headers={'Authorization': f'Bearer {BEARER_TOKEN}'}, params=params)
        
        # Si la respuesta es exitosa (código 200), procesar el JSON
        response.raise_for_status()
        cotizacion = response.json()

        # Extraer los valores de "cierreanterior" y "ultimoPrecio" de la respuesta
        cierre_anterior = cotizacion.get('cierreanterior', 'N/A')
        ultimo_precio = cotizacion.get('ultimoPrecio', 'N/A')

        # Devolver solo el cierre anterior y el último precio
        return jsonify({
            'cierreanterior': cierre_anterior,
            'ultimoPrecio': ultimo_precio
        })

    except requests.exceptions.RequestException as error:
        print(f'Error al hacer la solicitud a la API de cotización: {error}')
        if error.response:
            print(f'Response: {error.response.text}')  # Mostrar la respuesta del servidor
        return jsonify({'error': 'Error al obtener los datos de cotización'}), 500
# Endpoint para obtener opciones tipo "Call" o "Put"
@app.route('/api/opciones/<mercado>/<simbolo>/<tipoOpcion>', methods=['GET'])
def obtener_opciones(mercado, simbolo, tipoOpcion):
    try:
        response = requests.get(f'https://api.invertironline.com/api/v2/{mercado}/Titulos/{simbolo}/Opciones', 
                                headers={'Authorization': f'Bearer {BEARER_TOKEN}'})
        response.raise_for_status()
        
        opciones = response.json()  # Obtener la respuesta en formato JSON

        # Verificar si la respuesta contiene una lista de opciones
        if isinstance(opciones, list):
            # Filtrar por tipo de opción (Call o Put)
            opciones_filtradas = [opcion for opcion in opciones if opcion.get('tipoOpcion') == tipoOpcion]

            # Limitar los resultados a los primeros 10 (puedes ajustar el número si es necesario)
            primeros10_opciones = opciones_filtradas[:100]

            print(f'Primeros 10 Opciones tipo {tipoOpcion}:', primeros10_opciones)
            return jsonify(primeros10_opciones)
        else:
            return jsonify({'error': 'Estructura de respuesta inesperada de la API'}), 500

    except requests.exceptions.RequestException as error:
        print(f'Error al hacer la solicitud a la API: {error}')
        return jsonify({'error': 'Error al obtener los datos de la API'}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=PORT)
