Guardian Clima ITBA

Equipo 42

Integrantes:
Trzicky, Max - 68571 
Lancestremere Lewi, Santino - 69103
Sarkis, Santiago - 69185
Tamini, Joaquín - 69042

Descripción del proyecto
GuardianClima es una aplicación desarrollada con Python para consultar información climática en tiempo real a través del uso de una API meteorológica, guardar un historial global de consultas y obtener recomendación de vestimenta utilizando una inteligencia artificial.

Objetivos
Los objetivos de la aplicación son:
Consultar información sobre el clima de cualquier ciudad del mundo
Registrar usuarios mediante la validación de contraseñas que cumplan requisitos de seguridad (Más de 8 caracteres, usar al menos una mayúscula y un carácter especial)
Conservar un historial global de consultas
Desarrollar estadísticas a partir de los datos almacenados
Utilizar inteligencia artificial para dar consejos personalizados dependiendo del clima.

Requisitos
Antes de ejecutar el proyecto es necesario tener instalado
Python 3.x
Conexión a internet
También se necesita agregar las siguiente librerías
python -m pip install requests 
python -m pip install google-genai

Configuración de APIs
OpenWeatherMap
El proyecto utiliza OpenWeatherMap para obtener datos climáticos en tiempo real.
Pasos para obtener una API:
Crear una cuenta en OpenWeatherMap.
Generar una API Key.
Reemplazar la variable:
Al inicio del código tendrás que escribir esa API reemplazando a la X que hay originalmente.
OWM_API_KEY = "Tu API key" 

Google Gemini
La aplicación utiliza la inteligencia artificial Google Gemini para generar recomendaciones de vestimenta.
Pasos:
Ingresar a Google AI Studio.
Crear una API Key.
Reemplazar la variable:
Al igual que en el paso anterior, se debe escribir la nueva API reemplazando a la X al incio del código de esta manera:
GEMINI API_KEY = "Tu API Key"

Ejecución del Programa
Abrir una terminal en la carpeta del proyecto y ejecutar:
python guardian clima completo(final).py
Al iniciar, el sistema mostrará el menú de acceso para iniciar sesión o registrar un nuevo usuario.
Funcionalidades
Menú de Acceso
1. Iniciar Sesión
Permite ingresar utilizando un usuario y contraseña previamente registrados.
2. Registrar Nuevo Usuario
Permite crear un nuevo usuario validando que la contraseña cumpla criterios mínimos de seguridad.
3. Salir
Finaliza la ejecución de la aplicación.
Menú Principal
1. Consultar Clima y Guardar
Obtiene información climática actual de una ciudad y almacena la consulta en el historial global.
Información que se obtiene:
Temperatura
Sensación térmica
Humedad
Velocidad del viento
Condición climática
2. Historial Personal
Permite consultar el historial de búsquedas hechas por el usuario en una ciudad específica.
3. Estadísticas Globales
Calcula y muestra:
Cantidad total de consultas.
Ciudad más consultada.
Temperatura promedio registrada.
Además, los datos pueden exportarse mediante el archivo CSV para análisis arse en Excel o Google Sheets.
4. Consejo IA
Utiliza Google Gemini para analizar los datos climáticos obtenidos y generar una recomendación de vestimenta personalizada.
Ejemplo:
"Se recomienda utilizar una campera liviana debido a la baja temperatura y la presencia de viento."
5. Acerca de
Muestra información general sobre el trabajo, el funcionamiento interno y a los integrantes del equipo.
6. Cerrar Sesión
Finaliza la sesión del usuario y regresa al menú de acceso.
Archivos Generados
usuarios simulados.csv
Almacena los usuarios registrados junto con sus contraseñas para la simulación del sistema de autenticación.
Columnas:
username
password simulada
historial global.csv
Almacena todas las consultas climáticas realizadas por los usuarios.
Columnas
NombreDeUsuario
Ciudad
FechaHora
Temperatura C
Condición Clima
Humedad Porcentaje
Viento Km H
Tecnologías Utilizadas
Python 3
OpenWeatherMap API
Google Gemini API
Requests
Google GenAI
CSV
Google Sheets / Microsoft Excel
Conclusiones
Este proyecto permitió integrar conocimientos de programación, manejo de APIs, almacenamiento de datos, validación de y utilización de inteligencia artificial en una aplicación funcional. Además, permitió analizar información mediante herramientas de visualización de datos como Excel y Google Sheets.

