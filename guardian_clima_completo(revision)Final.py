"""
  GuardiánClima ITBA
  Integrantes: Santino Lancestremere Lewi, Santiago Sarkis, Max Trzicky, Joaquin Maria Tamini (Equipo 42)
"""

import csv
import os
import requests
from datetime import datetime

#  APIs

OWM_API_KEY    = "X"
GEMINI_API_KEY = "X"

ARCHIVO_USUARIOS  = "usuarios_simulados.csv"
ARCHIVO_HISTORIAL = "historial_global.csv"

NOMBRE_EQUIPO = "42"
INTEGRANTES   = ["Santiago Sarkis", "Max Trzicky", "Joaquin Maria Tamini", "Santino Lancestremere Lewi"]

#  ARCHIVOS CSV

def inicializar_archivos():
    """Crea los archivos CSV con encabezados si no existen."""
    if not os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["username", "password_simulada"])

    if not os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                "NombreDeUsuario", "Ciudad", "FechaHora",
                "Temperatura_C", "Condicion_Clima",
                "Humedad_Porcentaje", "Viento_kmh"
            ])


def leer_usuarios():
    """Devuelve una lista de dicts con todos los usuarios."""
    usuarios = []
    if not os.path.exists(ARCHIVO_USUARIOS):
        return usuarios
    with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            usuarios.append(fila)
    return usuarios


def guardar_usuario(username, password):
    """Agrega un nuevo usuario al CSV."""
    with open(ARCHIVO_USUARIOS, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([username, password])


def guardar_consulta(username, ciudad, temp, condicion, humedad, viento):
    """Agrega una fila al historial global."""
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ARCHIVO_HISTORIAL, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            username, ciudad, fecha_hora,
            temp, condicion, humedad, viento
        ])


def leer_historial():
    """Devuelve una lista de dicts con todo el historial."""
    historial = []
    if not os.path.exists(ARCHIVO_HISTORIAL):
        return historial
    with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            historial.append(fila)
    return historial

#  VALIDACIÓN CONTRASEÑAS

def validar_password(password):
    """
    Valida que la contraseña cumpla al menos 3 criterios de seguridad:
      1. Mínimo 8 caracteres
      2. Al menos una letra mayúscula
      3. Al menos una letra minúscula
      4. Al menos un número
      5. Al menos un carácter especial (!@#$%^&*)

    Devuelve (es_valida: bool, errores: list[str])
    """
    errores = []

    if len(password) < 8:
        errores.append("Debe tener al menos 8 caracteres")

    if not any(c.isupper() for c in password):
        errores.append("Debe contener al menos una MAYÚSCULA")

    if not any(c.islower() for c in password):
        errores.append("Debe contener al menos una minúscula")

    if not any(c.isdigit() for c in password):
        errores.append("Debe contener al menos un número")

    if not any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password):
        errores.append("Debe contener al menos un carácter especial (!@#$%...)")

    return (len(errores) == 0), errores

# API OpenWeatherMap 

def consultar_clima(ciudad):
    """
    Consulta el clima actual de una ciudad via OpenWeatherMap.
    Devuelve un dict con los datos o None si hay error.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": ciudad,
        "appid": OWM_API_KEY,
        "units": "metric",
        "lang": "es"
    }

    try:
        respuesta = requests.get(url, params=params, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()

        return {
            "ciudad":    datos["name"],
            "temp":      datos["main"]["temp"],
            "sensacion": datos["main"]["feels_like"],
            "humedad":   datos["main"]["humidity"],
            "condicion": datos["weather"][0]["description"].capitalize(),
            "viento":    round(datos["wind"]["speed"] * 3.6, 1)  # m/s → km/h
        }

    except requests.exceptions.HTTPError:
        if respuesta.status_code == 401:
            print("  ❌ API Key de OpenWeatherMap inválida.")
        elif respuesta.status_code == 404:
            print(f"  ❌ Ciudad '{ciudad}' no encontrada.")
        else:
            print(f"  ❌ Error HTTP: {respuesta.status_code}")
        return None

    except requests.exceptions.ConnectionError:
        print("  ❌ Sin conexión a internet.")
        return None

    except requests.exceptions.Timeout:
        print("  ❌ La solicitud tardó demasiado (timeout).")
        return None

#  API Gemini

def consejo_vestimenta_ia(temp, condicion, humedad, viento):
    """
    Pide a Gemini un consejo de vestimenta según el clima.
    Usa la librería google-genai (pip install google-genai).
    """
    try:
        from google import genai

        cliente = genai.Client(api_key="AQ.Ab8RN6IG_tmavW1ZZu6F37RIsRAJAVh59y2YUeaT07hEFCXXlQ")

        prompt = (
            f"Soy una persona que necesita saber cómo vestirse hoy. "
            f"El clima actual es: temperatura {temp}°C, sensación térmica similar, "
            f"condición '{condicion}', humedad {humedad}%, viento a {viento} km/h. "
            f"Dame un consejo breve, amigable y práctico (máximo 4 oraciones) "
            f"sobre qué ropa ponerme hoy. Responde en español."
        )

        print("\n  🤖 Consultando IA...")
        respuesta = cliente.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return respuesta.text if respuesta.text else "La IA no pudo generar un consejo."

    except ImportError:
        return "⚠️  Librería no instalada. Ejecutá: pip install google-genai"
    except Exception as e:
        return f"Error al contactar Gemini: {e}"



#  MENÚ DE ACCESO 


def menu_registro():
    """Flujo de registro de un nuevo usuario. Devuelve el username o None."""
    print("\n─── REGISTRO DE NUEVO USUARIO ───")
    usuarios = leer_usuarios()
    usernames_existentes = [u["username"].lower() for u in usuarios]

    # Elegir username
    while True:
        username = input("  Nombre de usuario: ").strip()
        if not username:
            print("  El nombre no puede estar vacío.")
            continue
        if username.lower() in usernames_existentes:
            print("  ❌ Ese nombre de usuario ya existe. Probá con otro.")
        else:
            break

    # Elegir contraseña con validación
    intentos_password = 0
    while True:
        intentos_password += 1
        password = input("  Contraseña: ").strip()
        es_valida, errores = validar_password(password)

        if es_valida:
            guardar_usuario(username, password)
            print(f"\n  ✅ ¡Usuario '{username}' registrado exitosamente!")
            return username
        else:
            print(f"\n  ❌ Contraseña rechazada. Problemas encontrados:")
            for e in errores:
                print(f"     • {e}")
            print("\n  💡 Para una contraseña más segura, considerá:")
            print("     → Usar al menos 8 caracteres")
            print("     → Mezclar MAYÚSculas, minúsculas, números y símbolos")
            print("     → Ejemplo: L0c0sITB4!")
            print(f"  (Intento {intentos_password} — seguí intentando)\n")


def menu_login():
    """Flujo de inicio de sesión. Devuelve el username o None."""
    print("\n─── INICIAR SESIÓN ───")
    usuarios = leer_usuarios()

    for _ in range(3):  # máximo 3 intentos
        username = input("  Usuario: ").strip()
        password = input("  Contraseña: ").strip()

        for u in usuarios:
            if u["username"] == username and u["password_simulada"] == password:
                print(f"\n  ✅ ¡Bienvenido, {username}!")
                return username

        print("  ❌ Usuario o contraseña incorrectos. Intentá de nuevo.")

    print("  Demasiados intentos fallidos.")
    return None


def menu_acceso():
    """Menú inicial de la app. Devuelve el username del usuario logueado."""
    while True:
        print("\n╔══════════════════════════════════╗")
        print("║    🌤  GuardiánClima ITBA  🌤      ║")
        print("╠══════════════════════════════════╣")
        print("║  1. Iniciar Sesión               ║")
        print("║  2. Registrar Nuevo Usuario      ║")
        print("║  3. Salir                        ║")
        print("╚══════════════════════════════════╝")
        opcion = input("  Elegí una opción: ").strip()

        if opcion == "1":
            usuario = menu_login()
            if usuario:
                return usuario

        elif opcion == "2":
            usuario = menu_registro()
            if usuario:
                return usuario  # auto-login tras registro

        elif opcion == "3":
            print("\n  👋 ¡Hasta luego!")
            exit()

        else:
            print("  ⚠️  Opción inválida. Ingresá 1, 2 o 3.")



#  MENÚ PRINCIPAL


def opcion_consultar_clima(username):
    """Opción 1: consulta el clima y guarda en historial."""
    print("\n─── CONSULTAR CLIMA ───")
    ciudad = input("  ¿De qué ciudad querés saber el clima? ").strip()
    if not ciudad:
        print("  Ciudad no ingresada.")
        return None

    datos = consultar_clima(ciudad)
    if not datos:
        return None

    print(f"\n  🌍 Clima en {datos['ciudad']}:")
    print(f"     🌡  Temperatura:     {datos['temp']}°C")
    print(f"     🤔 Sensación térm.: {datos['sensacion']}°C")
    print(f"     💧 Humedad:         {datos['humedad']}%")
    print(f"     🌬  Viento:          {datos['viento']} km/h")
    print(f"     ☁️  Condición:       {datos['condicion']}")

    guardar_consulta(
        username, datos["ciudad"],
        datos["temp"], datos["condicion"],
        datos["humedad"], datos["viento"]
    )
    print("\n  💾 Consulta guardada en el historial global.")
    return datos


def opcion_historial_personal(username):
    """Opción 2: muestra el historial del usuario para una ciudad."""
    print("\n─── MI HISTORIAL PERSONAL ───")
    ciudad = input("  ¿Qué ciudad querés ver? ").strip().lower()

    historial = leer_historial()
    resultados = [
        h for h in historial
        if h["NombreDeUsuario"] == username and h["Ciudad"].lower() == ciudad
    ]

    if not resultados:
        print(f"  Sin registros para '{ciudad}' en tu historial.")
        return

    print(f"\n  📋 Tu historial para '{ciudad.title()}':")
    print(f"  {'Fecha/Hora':<20} {'Temp':>6} {'Condición':<25} {'Humedad':>8}")
    print("  " + "─" * 65)
    for h in resultados:
        print(f"  {h['FechaHora']:<20} {h['Temperatura_C']:>5}°C  "
              f"{h['Condicion_Clima']:<25} {h['Humedad_Porcentaje']:>6}%")


def opcion_estadisticas():
    """Opción 3: calcula y muestra estadísticas globales."""
    print("\n─── ESTADÍSTICAS GLOBALES ───")
    historial = leer_historial()

    if not historial:
        print("  Sin datos en el historial todavía.")
        return

    total = len(historial)

    # Ciudad más consultada
    conteo_ciudades = {}
    for h in historial:
        c = h["Ciudad"]
        conteo_ciudades[c] = conteo_ciudades.get(c, 0) + 1
    ciudad_top = max(conteo_ciudades, key=conteo_ciudades.get)

    # Temperatura promedio
    temperaturas = []
    for h in historial:
        try:
            temperaturas.append(float(h["Temperatura_C"]))
        except ValueError:
            pass
    promedio_temp = round(sum(temperaturas) / len(temperaturas), 1) if temperaturas else 0

    print(f"\n  📊 Total de consultas:       {total}")
    print(f"  🏙️  Ciudad más consultada:    {ciudad_top} ({conteo_ciudades[ciudad_top]} veces)")
    print(f"  🌡  Temperatura promedio:     {promedio_temp}°C")
    print(f"\n  Podés abrir '{ARCHIVO_HISTORIAL}' en Excel/Google Sheets")
    print("     para analizar los datos.")


def opcion_consejo_ia(username):
    """Opción 4: pide consejo de vestimenta a Gemini según el clima."""
    print("\n─── CONSEJO IA: ¿CÓMO ME VISTO? ───")

    #última consulta del usuario
    historial = leer_historial()
    mis_consultas = [h for h in historial if h["NombreDeUsuario"] == username]

    if mis_consultas:
        ultima = mis_consultas[-1]
        print(f"  Usando tu última consulta: {ultima['Ciudad']} — {ultima['FechaHora']}")
        temp      = float(ultima["Temperatura_C"]  or 0)
        condicion = ultima["Condicion_Clima"]     or "Sin datos"
        humedad   = float(ultima["Humedad_Porcentaje"] or 0)
        viento    = float(ultima["Viento_kmh"]    or 0)
    else:
        print("  No tenés consultas previas. Hacé una consulta de clima primero.")
        ciudad = input("  Ciudad para consultar ahora: ").strip()
        datos = consultar_clima(ciudad)
        if not datos:
            return
        guardar_consulta(
            username, datos["ciudad"],
            datos["temp"], datos["condicion"],
            datos["humedad"], datos["viento"]
        )
        temp      = datos["temp"]
        condicion = datos["condicion"]
        humedad   = datos["humedad"]
        viento    = datos["viento"]

    consejo = consejo_vestimenta_ia(temp, condicion, humedad, viento)
    print(f"\n  🤖 Consejo de vestimenta:\n")
    print(f"  {consejo}")


def opcion_acerca_de():
    """Opción 5: información sobre la app y el equipo."""
    print("\n╔════════════════════════════════════════════════════╗")
    print("║             ACERCA DE GuardiánClima ITBA           ║")
    print("╠════════════════════════════════════════════════════╣")
    print("║                                                    ║")
    print("║  Aplicación de consola en Python que permite:      ║")
    print("║  • Consultar el clima de cualquier ciudad          ║")
    print("║  • Guardar un historial global de consultas        ║")
    print("║  • Ver estadísticas de uso globales                ║")
    print("║  • Recibir consejos de vestimenta con IA           ║")
    print("║                                                    ║")
    print("╠════════════════════════════════════════════════════╣")
    print("║  CÓMO FUNCIONA INTERNAMENTE:                       ║")
    print("║                                                    ║")
    print("║  🔐 Seguridad:                                     ║")
    print("║     Validamos contraseñas acorde a lo estudiado.   ║")
    print("║                                                    ║")
    print("║  ☁️  Cloud/APIs:                                    ║")
    print("║     OpenWeatherMap para datos climáticos.          ║")
    print("║     Google Gemini para consejos con IA.            ║")
    print("║                                                    ║")
    print("║  📊 Datos:                                         ║")
    print("║     historial_global.csv acumula todas las         ║")
    print("║     consultas para análisis y gráficos.            ║")
    print("╠════════════════════════════════════════════════════╣")
    print(f"║  👥 Equipo: {NOMBRE_EQUIPO:<39}║")
    print("║  Integrantes:                                      ║")
    print("║     • Santiago Sarkis                              ║")
    print("║     • Max Trzicky                                  ║")
    print("║     • Joaquin Maria Tamini                         ║")
    print("║     • Santino Lancestremere Lewi                   ║")
    print("╚════════════════════════════════════════════════════╝")


#  MENÚ PRINCIPAL (Post-Login)

def menu_principal(username):
    """Menú principal de la app una vez logueado."""
    ultima_consulta = None  # guarda la última consulta de clima

    while True:
        print(f"\n╔══════════════════════════════════════╗")
        print(f"║   GuardiánClima  |  👤 {username:<13} ║")
        print(f"╠══════════════════════════════════════╣")
        print(f"║  1. Consultar Clima y Guardar        ║")
        print(f"║  2. Mi Historial por Ciudad          ║")
        print(f"║  3. Estadísticas Globales            ║")
        print(f"║  4. Consejo IA: ¿Cómo me visto?      ║")
        print(f"║  5. Acerca De...                     ║")
        print(f"║  6. Cerrar Sesión                    ║")
        print(f"╚══════════════════════════════════════╝")
        opcion = input("  Elegí una opción: ").strip()

        if opcion == "1":
            resultado = opcion_consultar_clima(username)
            if resultado:
                ultima_consulta = resultado

        elif opcion == "2":
            opcion_historial_personal(username)

        elif opcion == "3":
            opcion_estadisticas()

        elif opcion == "4":
            opcion_consejo_ia(username)

        elif opcion == "5":
            opcion_acerca_de()

        elif opcion == "6":
            print(f"\n  Sesión cerrada. ¡Hasta la próxima, {username}!")
            return  # vuelve al menú de acceso

        else:
            print("  ⚠️  Opción inválida. Ingresá un número del 1 al 6.")

        input("\n  [Enter para continuar]")

#  BIENVENIDA

def main():
    """Función principal: inicializa archivos y arranca el menú de acceso."""
    inicializar_archivos()

    print("\n  ┌─────────────────────────────────────┐")
    print("  │  Bienvenido a GuardiánClima ITBA    │")
    print("  └─────────────────────────────────────┘")

    while True:
        # El menú de acceso devuelve el username logueado
        username = menu_acceso()
        # Entramos al menú principal con ese usuario
        menu_principal(username)
        # Al cerrar sesión, volvemos al while y se muestra el menú de acceso


if __name__ == "__main__":
    main()
