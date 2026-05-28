import csv
import requests
from datetime import datetime


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

ARCHIVO_USUARIOS = "usuarios_simulados.csv"
ARCHIVO_HISTORIAL = "historial_global.csv"

CAMPOS_USUARIOS = ["username", "password_simulada"]

CAMPOS_HISTORIAL = [
    "NombreDeUsuario",
    "Ciudad",
    "FechaHora",
    "Temperatura_C",
    "SensacionTermica_C",
    "Condicion_Clima",
    "Humedad_Porcentaje",
    "Viento_kmh"
]

# Reemplazar estas claves por las claves reales del equipo.
# Importante: no subir las claves reales a repositorios públicos.
API_KEY_OPENWEATHER = "ae5ca3c68ed830f787df31ce22b2e01bR"
API_KEY_GEMINI = "TU_API_KEY_GEMINI"

NOMBRE_GRUPO = "Equipo GuardiánClima"
DESARROLLADORES = "Santino y equipo"


# ============================================================
# FUNCIONES PARA ARCHIVOS CSV
# ============================================================

def crear_archivo_usuarios_si_no_existe():
    """
    Verifica si existe usuarios_simulados.csv.
    Si no existe, lo crea con los encabezados correspondientes.
    """
    try:
        with open(ARCHIVO_USUARIOS, "r", newline="", encoding="utf-8") as archivo:
            pass
    except FileNotFoundError:
        with open(ARCHIVO_USUARIOS, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_USUARIOS)
            escritor.writeheader()


def crear_archivo_historial_si_no_existe():
    """
    Verifica si existe historial_global.csv.
    Si no existe, lo crea con los encabezados correspondientes.
    """
    try:
        with open(ARCHIVO_HISTORIAL, "r", newline="", encoding="utf-8") as archivo:
            pass
    except FileNotFoundError:
        with open(ARCHIVO_HISTORIAL, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_HISTORIAL)
            escritor.writeheader()


def leer_usuarios():
    """
    Lee todos los usuarios guardados en usuarios_simulados.csv.
    Devuelve una lista de diccionarios.
    """
    crear_archivo_usuarios_si_no_existe()

    usuarios = []

    with open(ARCHIVO_USUARIOS, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            usuarios.append(fila)

    return usuarios


def leer_historial():
    """
    Lee todas las consultas guardadas en historial_global.csv.
    Devuelve una lista de diccionarios.
    """
    crear_archivo_historial_si_no_existe()

    historial = []

    with open(ARCHIVO_HISTORIAL, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            historial.append(fila)

    return historial


# ============================================================
# FUNCIONES DE USUARIOS Y CONTRASEÑAS
# ============================================================

def existe_usuario(username):
    """
    Verifica si un nombre de usuario ya existe.
    """
    usuarios = leer_usuarios()

    for usuario in usuarios:
        if usuario["username"] == username:
            return True

    return False


def validar_contrasena(contrasena):
    """
    Valida una contraseña según criterios básicos de seguridad.
    Devuelve una lista con las reglas no cumplidas.
    Si la lista queda vacía, la contraseña es válida.
    """
    reglas_no_cumplidas = []

    tiene_mayuscula = False
    tiene_minuscula = False
    tiene_numero = False
    tiene_simbolo = False

    if len(contrasena) < 8:
        reglas_no_cumplidas.append("tener al menos 8 caracteres")

    for caracter in contrasena:
        if caracter.isupper():
            tiene_mayuscula = True
        elif caracter.islower():
            tiene_minuscula = True
        elif caracter.isdigit():
            tiene_numero = True
        else:
            tiene_simbolo = True

    if not tiene_mayuscula:
        reglas_no_cumplidas.append("incluir al menos una letra mayúscula")

    if not tiene_minuscula:
        reglas_no_cumplidas.append("incluir al menos una letra minúscula")

    if not tiene_numero:
        reglas_no_cumplidas.append("incluir al menos un número")

    if not tiene_simbolo:
        reglas_no_cumplidas.append("incluir al menos un símbolo")

    return reglas_no_cumplidas


def mostrar_recomendacion_contrasena(reglas_no_cumplidas):
    """
    Muestra al usuario las reglas que no cumplió su contraseña.
    """
    print("\nTu contraseña no cumple con estas reglas:")

    for regla in reglas_no_cumplidas:
        print("- Debe " + regla)

    print("\nPara una contraseña más segura, considerá usar:")
    print("- Una contraseña larga.")
    print("- Una combinación de mayúsculas y minúsculas.")
    print("- Números.")
    print("- Símbolos como !, ?, @, #, $, %.")
    print("- Evitar datos personales o contraseñas obvias como 12345678.\n")


def guardar_usuario(username, contrasena):
    """
    Guarda un usuario nuevo en usuarios_simulados.csv.
    """
    crear_archivo_usuarios_si_no_existe()

    with open(ARCHIVO_USUARIOS, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_USUARIOS)

        nuevo_usuario = {
            "username": username,
            "password_simulada": contrasena
        }

        escritor.writerow(nuevo_usuario)


def registrar_usuario():
    """
    Registra un nuevo usuario.
    Si el registro es exitoso, devuelve el nombre de usuario registrado.
    """
    print("\n--- Registro de Nuevo Usuario ---")

    while True:
        username = input("Elegí un nombre de usuario: ").strip()

        if username == "":
            print("El nombre de usuario no puede estar vacío.")
        elif existe_usuario(username):
            print("Ese nombre de usuario ya existe. Probá con otro.")
        else:
            break

    while True:
        contrasena = input("Elegí una contraseña: ")

        reglas_no_cumplidas = validar_contrasena(contrasena)

        if len(reglas_no_cumplidas) == 0:
            guardar_usuario(username, contrasena)
            print("\nRegistro exitoso. Ingresando al menú principal...")
            return username
        else:
            mostrar_recomendacion_contrasena(reglas_no_cumplidas)


def iniciar_sesion():
    """
    Solicita usuario y contraseña.
    Si las credenciales son correctas, devuelve el nombre de usuario.
    Si no, devuelve una cadena vacía.
    """
    print("\n--- Iniciar Sesión ---")

    username = input("Usuario: ").strip()
    contrasena = input("Contraseña: ")

    usuarios = leer_usuarios()

    for usuario in usuarios:
        if usuario["username"] == username and usuario["password_simulada"] == contrasena:
            print("\nInicio de sesión exitoso.")
            return username

    print("\nUsuario o contraseña incorrectos.")
    return ""


# ============================================================
# FUNCIONES DE CLIMA
# ============================================================

def obtener_clima_ciudad(ciudad):
    """
    Consulta la API de OpenWeatherMap y devuelve los datos climáticos.
    Si ocurre un error, devuelve None.
    """
    if API_KEY_OPENWEATHER == "TU_API_KEY_OPENWEATHER":
        print("\nFalta configurar la API Key de OpenWeatherMap.")
        print("Reemplazá TU_API_KEY_OPENWEATHER por tu clave real.")
        return None

    base_url = "https://api.openweathermap.org/data/2.5/weather"

    parametros = {
        "q": ciudad,
        "appid": API_KEY_OPENWEATHER,
        "units": "metric",
        "lang": "es"
    }

    print("\nConsultando el clima para:", ciudad)

    try:
        respuesta = requests.get(base_url, params=parametros, timeout=10)
        respuesta.raise_for_status()
        datos_clima = respuesta.json()
        return datos_clima

    except requests.exceptions.HTTPError:
        if respuesta.status_code == 401:
            print("Error: API Key inválida.")
        elif respuesta.status_code == 404:
            print("Error: ciudad no encontrada.")
        else:
            print("Error HTTP al consultar la API.")
        return None

    except requests.exceptions.RequestException:
        print("Error de conexión. Revisá tu internet o intentá más tarde.")
        return None

    except ValueError:
        print("Error: la respuesta de la API no tiene formato JSON válido.")
        return None


def convertir_clima_a_fila(usuario_actual, datos_clima):
    """
    Recibe los datos crudos de la API y los transforma en una fila simple
    para mostrar y guardar.
    """
    ciudad = datos_clima["name"]
    temperatura = datos_clima["main"]["temp"]
    sensacion = datos_clima["main"]["feels_like"]
    humedad = datos_clima["main"]["humidity"]
    condicion = datos_clima["weather"][0]["description"]
    viento_m_s = datos_clima["wind"]["speed"]
    viento_kmh = viento_m_s * 3.6

    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    fila = {
        "NombreDeUsuario": usuario_actual,
        "Ciudad": ciudad,
        "FechaHora": fecha_hora_actual,
        "Temperatura_C": round(temperatura, 1),
        "SensacionTermica_C": round(sensacion, 1),
        "Condicion_Clima": condicion,
        "Humedad_Porcentaje": humedad,
        "Viento_kmh": round(viento_kmh, 1)
    }

    return fila


def mostrar_clima(fila_clima):
    """
    Muestra los datos climáticos de forma clara.
    """
    print("\n--- Clima Actual ---")
    print("Ciudad:", fila_clima["Ciudad"])
    print("Fecha y hora:", fila_clima["FechaHora"])
    print("Temperatura:", fila_clima["Temperatura_C"], "°C")
    print("Sensación térmica:", fila_clima["SensacionTermica_C"], "°C")
    print("Condición:", fila_clima["Condicion_Clima"].capitalize())
    print("Humedad:", fila_clima["Humedad_Porcentaje"], "%")
    print("Viento:", fila_clima["Viento_kmh"], "km/h")


def guardar_consulta_historial(fila_clima):
    """
    Guarda una consulta climática en historial_global.csv.
    """
    crear_archivo_historial_si_no_existe()

    with open(ARCHIVO_HISTORIAL, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_HISTORIAL)
        escritor.writerow(fila_clima)

    print("\nConsulta guardada correctamente en historial_global.csv.")


def consultar_clima_y_guardar(usuario_actual):
    """
    Opción 1 del menú principal.
    Pide una ciudad, consulta el clima, muestra los datos y guarda la consulta.
    Devuelve la última consulta realizada.
    """
    print("\n--- Consultar Clima Actual ---")

    ciudad = input("Ingresá el nombre de una ciudad: ").strip()

    if ciudad == "":
        print("La ciudad no puede estar vacía.")
        return {}

    datos_clima = obtener_clima_ciudad(ciudad)

    if datos_clima == None:
        print("No se pudo obtener el clima.")
        return {}

    try:
        fila_clima = convertir_clima_a_fila(usuario_actual, datos_clima)
        mostrar_clima(fila_clima)
        guardar_consulta_historial(fila_clima)
        return fila_clima

    except KeyError:
        print("Error: la API devolvió datos con un formato inesperado.")
        return {}


# ============================================================
# FUNCIÓN DE HISTORIAL PERSONAL
# ============================================================

def ver_historial_personal_por_ciudad(usuario_actual):
    """
    Opción 2 del menú principal.
    Muestra las consultas del usuario actual para una ciudad específica.
    """
    print("\n--- Mi Historial Personal por Ciudad ---")

    ciudad_buscada = input("Ingresá la ciudad que querés buscar: ").strip()

    if ciudad_buscada == "":
        print("La ciudad no puede estar vacía.")
        return

    historial = leer_historial()
    resultados = []

    for fila in historial:
        mismo_usuario = fila["NombreDeUsuario"] == usuario_actual
        misma_ciudad = fila["Ciudad"].lower() == ciudad_buscada.lower()

        if mismo_usuario and misma_ciudad:
            resultados.append(fila)

    if len(resultados) == 0:
        print("\nNo se encontraron consultas para ese usuario y esa ciudad.")
        return

    print("\nConsultas encontradas:")

    for fila in resultados:
        print("----------------------------------------")
        print("Fecha y hora:", fila["FechaHora"])
        print("Ciudad:", fila["Ciudad"])
        print("Temperatura:", fila["Temperatura_C"], "°C")
        print("Sensación térmica:", fila["SensacionTermica_C"], "°C")
        print("Condición:", fila["Condicion_Clima"])
        print("Humedad:", fila["Humedad_Porcentaje"], "%")
        print("Viento:", fila["Viento_kmh"], "km/h")


# ============================================================
# FUNCIÓN DE ESTADÍSTICAS GLOBALES
# ============================================================

def mostrar_estadisticas_globales():
    """
    Opción 3 del menú principal.
    Calcula estadísticas usando todas las consultas del historial global.
    """
    print("\n--- Estadísticas Globales de Uso ---")

    historial = leer_historial()

    if len(historial) == 0:
        print("Todavía no hay consultas guardadas.")
        return

    total_consultas = len(historial)
    suma_temperaturas = 0
    cantidad_temperaturas_validas = 0

    consultas_por_ciudad = {}

    for fila in historial:
        ciudad = fila["Ciudad"]

        if ciudad in consultas_por_ciudad:
            consultas_por_ciudad[ciudad] = consultas_por_ciudad[ciudad] + 1
        else:
            consultas_por_ciudad[ciudad] = 1

        try:
            temperatura = float(fila["Temperatura_C"])
            suma_temperaturas = suma_temperaturas + temperatura
            cantidad_temperaturas_validas = cantidad_temperaturas_validas + 1
        except ValueError:
            pass

    ciudad_mas_consultada = ""
    mayor_cantidad = 0

    for ciudad in consultas_por_ciudad:
        if consultas_por_ciudad[ciudad] > mayor_cantidad:
            mayor_cantidad = consultas_por_ciudad[ciudad]
            ciudad_mas_consultada = ciudad

    if cantidad_temperaturas_validas > 0:
        temperatura_promedio = suma_temperaturas / cantidad_temperaturas_validas
    else:
        temperatura_promedio = 0

    print("Número total de consultas:", total_consultas)
    print("Ciudad más consultada:", ciudad_mas_consultada)
    print("Cantidad de consultas de esa ciudad:", mayor_cantidad)
    print("Temperatura promedio global:", round(temperatura_promedio, 1), "°C")

    print("\nConsultas por ciudad:")
    for ciudad in consultas_por_ciudad:
        print("-", ciudad + ":", consultas_por_ciudad[ciudad])

    print("\nEl archivo historial_global.csv queda disponible para armar gráficos en Excel o Google Sheets.")


# ============================================================
# FUNCIÓN DE CONSEJO DE VESTIMENTA
# ============================================================

def generar_consejo_local(fila_clima):
    """
    Genera un consejo básico sin IA externa.
    Esto sirve como respaldo si Gemini no está configurado.
    """
    temperatura = float(fila_clima["Temperatura_C"])
    humedad = int(fila_clima["Humedad_Porcentaje"])
    viento = float(fila_clima["Viento_kmh"])
    condicion = fila_clima["Condicion_Clima"].lower()

    consejo = "Consejo básico: "

    if temperatura <= 10:
        consejo = consejo + "hace frío, conviene usar abrigo pesado"
    elif temperatura <= 18:
        consejo = consejo + "conviene usar buzo, campera liviana o varias capas"
    elif temperatura <= 26:
        consejo = consejo + "el clima está templado, ropa cómoda y liviana debería alcanzar"
    else:
        consejo = consejo + "hace calor, conviene usar ropa fresca"

    if "lluvia" in condicion or "tormenta" in condicion:
        consejo = consejo + ", y llevar paraguas o campera impermeable"

    if viento >= 25:
        consejo = consejo + ". Además, hay bastante viento, así que evitá ropa demasiado suelta"

    if humedad >= 80 and temperatura >= 24:
        consejo = consejo + ". La humedad es alta, así que priorizá telas livianas"

    consejo = consejo + "."

    return consejo


def generar_consejo_ia(fila_clima):
    """
    Intenta generar un consejo usando Gemini.
    Si Gemini no está configurado o falla, usa un consejo local como respaldo.
    """
    if API_KEY_GEMINI == "TU_API_KEY_GEMINI":
        print("\nGemini no está configurado. Se usará un consejo básico local.")
        return generar_consejo_local(fila_clima)

    try:
        import google.generativeai as genai

        genai.configure(api_key=API_KEY_GEMINI)
        model = genai.GenerativeModel("gemini-pro")

        prompt = (
            "Sos un asistente de vestimenta para una aplicación climática. "
            "Tenés que dar un consejo breve, claro y práctico en español rioplatense. "
            "No exageres y no des una explicación larga. "
            "Datos del clima: "
            "Ciudad: " + str(fila_clima["Ciudad"]) + ". "
            "Temperatura: " + str(fila_clima["Temperatura_C"]) + " grados Celsius. "
            "Sensación térmica: " + str(fila_clima["SensacionTermica_C"]) + " grados Celsius. "
            "Condición climática: " + str(fila_clima["Condicion_Clima"]) + ". "
            "Humedad: " + str(fila_clima["Humedad_Porcentaje"]) + "%. "
            "Viento: " + str(fila_clima["Viento_kmh"]) + " km/h. "
            "Consejo:"
        )

        print("\nGenerando consejo con IA...")
        respuesta = model.generate_content(prompt)

        if respuesta.text:
            return respuesta.text
        else:
            return generar_consejo_local(fila_clima)

    except Exception:
        print("\nNo se pudo contactar correctamente a Gemini. Se usará un consejo básico local.")
        return generar_consejo_local(fila_clima)


def consejo_como_me_visto(usuario_actual, ultima_consulta):
    """
    Opción 4 del menú principal.
    Usa la última consulta climática del usuario para generar un consejo de vestimenta.
    Si no hay última consulta, permite hacer una nueva consulta.
    """
    print("\n--- Consejo IA: ¿Cómo Me Visto Hoy? ---")

    if ultima_consulta == {}:
        print("Todavía no hay una última consulta climática en esta sesión.")
        respuesta = input("¿Querés hacer una consulta de clima ahora? (s/n): ").strip().lower()

        if respuesta == "s":
            ultima_consulta = consultar_clima_y_guardar(usuario_actual)
        else:
            print("No se generó consejo porque no hay datos climáticos.")
            return ultima_consulta

    if ultima_consulta != {}:
        consejo = generar_consejo_ia(ultima_consulta)

        print("\nConsejo de vestimenta:")
        print(consejo)

    return ultima_consulta


# ============================================================
# FUNCIÓN ACERCA DE
# ============================================================

def mostrar_acerca_de():
    """
    Opción 5 del menú principal.
    Explica qué hace la aplicación y cómo funciona internamente.
    """
    print("\n--- Acerca De GuardiánClima ITBA ---")

    print("\nNombre del grupo:", NOMBRE_GRUPO)
    print("Desarrolladores:", DESARROLLADORES)

    print("\nDescripción:")
    print("GuardiánClima ITBA es una aplicación de consola en Python que permite")
    print("registrar usuarios, iniciar sesión, consultar el clima actual de una ciudad,")
    print("guardar las consultas en un historial global, ver historiales personales,")
    print("generar estadísticas globales y obtener consejos de vestimenta.")

    print("\nCómo usar el Menú de Acceso:")
    print("1. Iniciar sesión: permite ingresar con un usuario ya registrado.")
    print("2. Registrar nuevo usuario: permite crear un usuario con una contraseña validada.")
    print("3. Salir: termina la aplicación.")

    print("\nCómo usar el Menú Principal:")
    print("1. Consultar clima: pide una ciudad, consulta OpenWeatherMap y guarda el resultado.")
    print("2. Historial personal: muestra consultas del usuario actual para una ciudad.")
    print("3. Estadísticas globales: calcula ciudad más consultada, total de consultas y temperatura promedio.")
    print("4. Consejo IA: genera un consejo de vestimenta usando los datos climáticos.")
    print("5. Acerca De: muestra esta explicación.")
    print("6. Cerrar sesión: vuelve al menú de acceso.")

    print("\nFuncionamiento interno:")
    print("- Los usuarios se guardan en usuarios_simulados.csv.")
    print("- Las consultas climáticas se guardan en historial_global.csv.")
    print("- La validación de contraseña revisa longitud, mayúsculas, minúsculas, números y símbolos.")
    print("- La consulta de clima se realiza con la API de OpenWeatherMap.")
    print("- El consejo de vestimenta intenta usar Gemini y, si no está configurado, usa un respaldo local.")

    print("\nAdvertencia de seguridad:")
    print("El almacenamiento de contraseñas en este proyecto es una simulación educativa.")
    print("No es seguro para una aplicación real porque las contraseñas se guardan en texto visible.")
    print("En una aplicación real deberían usarse técnicas como hashing y otras medidas de seguridad.")


# ============================================================
# MENÚ PRINCIPAL Y MENÚ DE ACCESO
# ============================================================

def menu_principal(usuario_actual):
    """
    Menú principal de GuardiánClima ITBA.
    Se accede únicamente después de login o registro exitoso.
    """
    ultima_consulta = {}

    while True:
        print("\n--- Menú Principal: GuardiánClima ITBA ---")
        print("Usuario actual:", usuario_actual)
        print("1. Consultar clima actual y guardar en historial global")
        print("2. Ver mi historial personal de consultas por ciudad")
        print("3. Estadísticas globales de uso")
        print("4. Consejo IA: ¿Cómo me visto hoy?")
        print("5. Acerca De...")
        print("6. Cerrar sesión")

        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            consulta_realizada = consultar_clima_y_guardar(usuario_actual)

            if consulta_realizada != {}:
                ultima_consulta = consulta_realizada

        elif opcion == "2":
            ver_historial_personal_por_ciudad(usuario_actual)

        elif opcion == "3":
            mostrar_estadisticas_globales()

        elif opcion == "4":
            ultima_consulta = consejo_como_me_visto(usuario_actual, ultima_consulta)

        elif opcion == "5":
            mostrar_acerca_de()

        elif opcion == "6":
            print("\nCerrando sesión...")
            return

        else:
            print("\nOpción inválida. Probá de nuevo.")


def menu_acceso():
    """
    Menú inicial de la aplicación.
    Desde acá se puede iniciar sesión, registrar usuario o salir.
    """
    crear_archivo_usuarios_si_no_existe()
    crear_archivo_historial_si_no_existe()

    while True:
        print("\n=== GuardiánClima ITBA ===")
        print("1. Iniciar sesión")
        print("2. Registrar nuevo usuario")
        print("3. Salir de la aplicación")

        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            usuario_logueado = iniciar_sesion()

            if usuario_logueado != "":
                menu_principal(usuario_logueado)

        elif opcion == "2":
            usuario_registrado = registrar_usuario()
            menu_principal(usuario_registrado)

        elif opcion == "3":
            print("\nGracias por usar GuardiánClima ITBA.")
            break

        else:
            print("\nOpción inválida. Probá de nuevo.")


# ============================================================
# INICIO DEL PROGRAMA
# ============================================================

menu_acceso()
