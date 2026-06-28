#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AQ-IIoT Lab — Consumidor CEP v2

Motor CEP con tres reglas activas evaluadas en tiempo real sobre el
flujo MQTT publicado por Telegraf (tópico telegraf/#):

  Regla 1 — Umbral simple:
    Dispara alerta cuando un contaminante supera su límite en una sola
    lectura. Stateless: no requiere memoria del pasado.

  Regla 2 — Ventana temporal (patrón secuencial):
    Detecta si el mismo contaminante supera el umbral dos veces
    consecutivas en menos de 60 s sin que entre un valor normal entre
    ellas. Stateful: requiere guardar el estado del último evento.

  Regla 3 — Correlación de incendio:
    Alerta crítica cuando PM10 + NO2 + SO2 superan sus umbrales
    simultáneamente en la misma ciudad dentro de una ventana de 30 s.
    Físicamente realista: un incendio genera humo (PM10) y gases de
    combustión (NO2, SO2) al mismo tiempo.

Actuador: notificación por Telegram para alertas críticas (Reglas 2 y 3).

Umbrales: normativa europea Directiva 2024/2881 y OMS.
"""

import json
import requests
import paho.mqtt.client as mqtt
from datetime import datetime

# Configuración
MQTT_HOST  = "localhost"
MQTT_PORT  = 1883
MQTT_TOPIC = "telegraf/#"

UMBRALES = {
    "pm10": 45.0,   # µg/m³
    "no2":  200.0,  # µg/m³
    "so2":  125.0,  # µg/m³
}

# Actuador Telegram
TELEGRAM_ENABLED  = True
TELEGRAM_TOKEN    = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID  = "YOUR_CHAT_ID_HERE"

# Cooldown anti-spam para la alerta de incendio
FIRE_COOLDOWN_S = 120
last_fire_alert = {}


# -----------------------------------------------------------------------
# Actuador
# -----------------------------------------------------------------------
def send_telegram(mensaje: str) -> None:
    """Envía una notificación al bot de Telegram configurado."""
    if not TELEGRAM_ENABLED:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(
            url,
            json={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje},
            timeout=5
        )
    except Exception as e:
        print(f"WARN: No se pudo enviar mensaje Telegram: {e}")


# -----------------------------------------------------------------------
# Estado por ciudad
# -----------------------------------------------------------------------
estado_ciudades = {}

def get_estado(ciudad: str) -> dict:
    """Devuelve (e inicializa si no existe) el estado de una ciudad."""
    if ciudad not in estado_ciudades:
        estado_ciudades[ciudad] = {}
    return estado_ciudades[ciudad]


# -----------------------------------------------------------------------
# Regla 3: correlación de incendio
# -----------------------------------------------------------------------
def check_correlacion_incendio(ciudad: str, estado: dict, hora: str, ts: int) -> None:
    """
    Detecta si PM10, NO2 y SO2 están todos por encima de sus umbrales
    en la misma ciudad y dentro de un intervalo de 30 segundos entre sí.

    Lógica:
      1. Leer los sub-dicts de pm10, no2, so2 del estado de la ciudad.
      2. Comprobar que todos tienen anomalía == True.
      3. Verificar que max(timestamps) - min(timestamps) <= 30.
      4. Aplicar cooldown (FIRE_COOLDOWN_S) para no spammear.
      5. Si todo se cumple: imprimir alerta y llamar a send_telegram().

    TODO: implementar la lógica descrita arriba.
    """
    # --- implementación eliminada como muestra ---
    pass


# -----------------------------------------------------------------------
# MQTT callbacks
# -----------------------------------------------------------------------
def on_connect(client, userdata, flags, reason_code, properties) -> None:
    print(f"Conectado al broker MQTT. Escuchando en: {MQTT_TOPIC}")
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg) -> None:
    """
    Callback principal del motor CEP.

    Pasos:
      1. Deserializar el JSON del payload.
      2. Extraer fields, tags, ciudad y timestamp.
      3. Para cada contaminante en UMBRALES:
           a. Ignorar valores None o <= -999 (código EEA de dato no disponible).
           b. REGLA 1: si valor > umbral, imprimir alerta.
           c. REGLA 2: si el estado anterior también era anomalía y el
              intervalo entre ambos ts es <= 60 s, enviar alerta por Telegram.
           d. Actualizar estado[contaminante] con valor, ts y es_anomalia.
      4. REGLA 3: llamar a check_correlacion_incendio() fuera del bucle,
         sobre el estado ya actualizado.

    TODO: implementar la lógica descrita arriba.
    """
    raw_payload = msg.payload.decode("utf-8")
    try:
        evento = json.loads(raw_payload)
    except json.JSONDecodeError:
        print("WARN: mensaje no es JSON válido, ignorando.")
        return

    fields = evento.get("fields", {})
    tags   = evento.get("tags", {})
    nombre = evento.get("name", "desconocido")
    ciudad = tags.get("city", "desconocida")
    ts     = evento.get("timestamp", 0)
    hora   = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    estado = get_estado(ciudad)

    # TODO: implementar las tres reglas CEP aquí.
    pass


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------
def main() -> None:
    print("=== Motor CEP v2 - Detección de Anomalías y Correlaciones ===")
    print(f"Umbrales: {UMBRALES}")
    print(f"Telegram: {'ACTIVO' if TELEGRAM_ENABLED else 'DESACTIVADO'}")
    print()
    print("Reglas activas:")
    print("  Regla 1 — Umbral simple")
    print("  Regla 2 — Ventana temporal (60 s, stateful)")
    print("  Regla 3 — Correlación de incendio (PM10 + NO2 + SO2 simultáneos)")
    print()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
