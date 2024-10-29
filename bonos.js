const axios = require('axios');

// URL de la API
const url = 'https://api.invertironline.com/api/v2/Cotizaciones/titulosPublicos/argentina/Todos?cotizacionInstrumentoModel.instrumento=titulosPublicos&cotizacionInstrumentoModel.pais=argentina';

// Tu Bearer Token
const bearerToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCJ9.eyJzdWIiOiI1NzI4MTkiLCJJRCI6IjU3MjgxOSIsImp0aSI6ImRhNWUzM2Y1LWQ5YWItNDY2OS05YzE4LWZjNDlkYTkyZGY3MiIsImNvbnN1bWVyX3R5cGUiOiIxIiwidGllbmVfY3VlbnRhIjoiVHJ1ZSIsInRpZW5lX3Byb2R1Y3RvX2J1cnNhdGlsIjoiVHJ1ZSIsInRpZW5lX3Byb2R1Y3RvX2FwaSI6IlRydWUiLCJ0aWVuZV9UeUMiOiJUcnVlIiwibmJmIjoxNzI5OTAzODEwLCJleHAiOjE3Mjk5MDQ3MTAsImlhdCI6MTcyOTkwMzgxMCwiaXNzIjoiSU9MT2F1dGhTZXJ2ZXIiLCJhdWQiOiJJT0xPYXV0aHNlcnZlciJ9.k4WTZFSeh5D3ZlqvtrMWlXlH-LDValmztzWst2T8JDTryLUANhzz6On4ysqkXpE3eTEcZRVcH50Q-_DqV_-SZGsu8KAgqHPUVDzxQc7uPcK3l9FpQ2IJS0PVdHS_Kgf1gA62ZHfDd3c8JffycY9w8vxn2Ra3uS0vJw7gz7cCQxMmHygPyET7hbN5-21xn5FN_w5BEMNPW2wZrMqdnqSN61yhM8OxeUdI_pi4GV6xwudF0BCD2cU4VtscsCdN2zLMITghhclTg93-_kwQtp_slvS4PgRjt8HKBL6grMMeGhLSJkPR8G7F7OGRXDaRRkFMOpJVthf7Fjl7ccDOzI_Zsw'; // Reemplaza con tu token real

// Función para obtener las cotizaciones
async function obtenerCotizaciones() {
    try {
        const response = await axios.get(url, {
            headers: {
                Authorization: `Bearer ${bearerToken}`
            }
        });

        // Imprimir la respuesta completa para verificar su estructura
        console.log(JSON.stringify(response.data, null, 2));

        // Acceder correctamente a las cotizaciones
        const cotizaciones = response.data.data; // Cambia esto si es necesario

        // Verificar si cotizaciones es un array
        if (!Array.isArray(cotizaciones)) {
            console.error('La respuesta no contiene un array de cotizaciones:', cotizaciones);
            return;
        }

        // Filtrar solo los instrumentos "AL30" y "GD30"
        const instrumentosBuscados = ['AL30', 'GD30'];
        const resultados = cotizaciones.filter(cotizacion => 
            instrumentosBuscados.includes(cotizacion.simbolo)
        );

        // Comprobar si se encontraron resultados
        if (resultados.length === 0) {
            console.log('No se encontraron cotizaciones para AL30 y GD30');
        } else {
            // Imprimir los últimos precios
            resultados.forEach(({ simbolo, ultimoPrecio }) => {
                console.log(`El último precio de ${simbolo} es: ${ultimoPrecio}`);
            });
        }

    } catch (error) {
        console.error('Error al obtener las cotizaciones:', error.message);
    }
}

// Llamar a la función
obtenerCotizaciones();
