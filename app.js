const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const PORT = 3000;

// Habilitar CORS
app.use(cors());

let BEARER_TOKEN = ''; // Variable para almacenar el token Bearer

// Función para obtener el token Bearer
async function obtenerToken() {
    try {
        const response = await axios.post('https://api.invertironline.com/token', {
            username: 'sdkniko',
            password: 'Niko2137!',
            grant_type: 'password'
        });

        // Almacenar el token Bearer
        BEARER_TOKEN = response.data.access_token;
        console.log('Token obtenido:', BEARER_TOKEN);
    } catch (error) {
        console.error('Error al obtener el token:', error.message);
    }
}

// Llamar a la función para obtener el token cuando se inicie el servidor
obtenerToken();

app.get('/api/cotizacion/:mercado/:simbolo', async (req, res) => {
    const { mercado, simbolo } = req.params;
    const { modelMercado, modelSimbolo, modelPlazo } = req.query;

    try {
        const response = await axios.get(`https://api.invertironline.com/api/v2/${mercado}/Titulos/${simbolo}/Cotizacion`, {
            headers: {
                'Authorization': `Bearer ${BEARER_TOKEN}`
            },
            params: {
                mercado: modelMercado,
                simbolo: modelSimbolo,
                plazo: modelPlazo
            }
        });

        console.log('Cotización:', response.data); // Para depuración
        res.json(response.data);
    } catch (error) {
        console.error('Error al hacer la solicitud a la API de cotización:', error.message);
        res.status(500).json({ error: 'Error al obtener los datos de cotización' });
    }
});

// Endpoint para obtener opciones tipo "Call" o "Put" según lo especificado
app.get('/api/opciones/:mercado/:simbolo/:tipoOpcion', async (req, res) => {
  const { mercado, simbolo, tipoOpcion } = req.params;

  try {
    const response = await axios.get(`https://api.invertironline.com/api/v2/${mercado}/Titulos/${simbolo}/Opciones`, {
      headers: {
        'Authorization': `Bearer ${BEARER_TOKEN}`
      },
      params: {
        mercado: 'bcba',
        simbolo: simbolo
      }
    });

    // Filtrar los resultados por el tipo de opción (Call o Put)
    const opciones = response.data.filter(opcion => opcion.tipoOpcion === tipoOpcion);

    // Limitar los resultados a los primeros 10
    const primeros10Opciones = opciones.slice(0, 100);

    console.log(`Primeros 10 Opciones tipo ${tipoOpcion}:`, primeros10Opciones);
    res.json(primeros10Opciones);
  } catch (error) {
    console.error('Error al hacer la solicitud a la API:', error.message);
    res.status(500).json({ error: 'Error al obtener los datos de la API' });
  }
});

app.listen(PORT, () => {
  console.log(`Servidor ejecutándose en http://localhost:${PORT}`);
});
