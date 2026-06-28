"""
Intermediario de suscripción MQTT — AQ-IIoT Lab

Motivación:
  La API de la EEA actualiza sus datos aproximadamente una vez por hora.
  El servidor OPC-UA, configurado en modo suscripción, sólo genera
  notificaciones hacia Telegraf cuando detecta un cambio real en el valor
  de un nodo: si los datos no cambian, no hay notificaciones y Telegraf
  no escribe nada en InfluxDB durante esa hora.

  Solución (patrón Pipes and Filters):
    1. Este script se suscribe a los tópicos originales del scraper
       (airquality/+/eea).
    2. Aplica una pequeña perturbación aleatoria a cada contaminante
       en cada ciclo de publicación.
    3. Republica los datos modificados en tópicos nuevos
       (airquality/{city}/eea_modified).
    4. El servidor OPC-UA se suscribe a estos tópicos modificados,
       de modo que siempre percibe variaciones y genera notificaciones.

  Este componente NO modifica el scraper ni el servidor OPC-UA: actúa
  exclusivamente como filtro intermedio en la cadena de datos.
"""

from __future__ import annotations

import random
import time
import json
from datetime import datetime, timezone
from typing import Any, Dict
import paho.mqtt.client as mqtt

MQTT_HOST  = "localhost"
MQTT_PORT  = 1883
POLLUTANTS = ["PM10", "NO2", "SO2"]
CITY_NAMES = ["Valencia", "Alicante/Alacant", "Eivissa"]

MQTT_TOPIC_SUBSCRIBE = "airquality/+/eea"
MQTT_TOPIC_PUBLICATE = "airquality/{city}/eea_modified"

# Frecuencia de republicación: debe ser menor que el sampling_interval de Telegraf
# para garantizar que el servidor OPC-UA siempre vea un valor distinto al anterior.
PUBLISH_EVERY_S = 1

latest_by_city: Dict[str, Dict[str, Any]] = {}


def on_message(client, userdata, msg) -> None:
    """
    Extrae el nombre de la ciudad del tópico MQTT (segundo segmento de
    airquality/<city>/eea) y guarda el payload en latest_by_city.

    El tratamiento especial de Alicante/Alacant es necesario porque el
    carácter '/' haría que MQTT interpretara un nivel extra de jerarquía
    en el nombre del tópico. Por eso se normaliza a 'alicante_alacant'.
    """
    global latest_by_city
    try:
        parts = msg.topic.split("/")
        if len(parts) >= 2:
            city_key = "/".join(parts[1:len(parts)-1]).lower().replace("/", "_").replace(" ", "_")
        else:
            return
        payload = json.loads(msg.payload.decode("utf-8"))
        latest_by_city[city_key] = payload
    except Exception:
        pass


# -----------------------------------------------------------------------------
# Funciones de perturbación aleatoria
# -----------------------------------------------------------------------------
def anomalia_pm10(valor: float | None) -> float | None:
    """
    Aplica un pequeño ruido uniforme a PM10.
    TODO: definir el rango apropiado para que el cambio sea perceptible
          por el servidor OPC-UA pero no distorsione el valor real.
    """
    # --- implementación eliminada como muestra ---
    raise NotImplementedError

def anomalia_no2(valor: float | None) -> float | None:
    """Aplica un pequeño ruido uniforme a NO2. Ver anomalia_pm10."""
    raise NotImplementedError

def anomalia_so2(valor: float | None) -> float | None:
    """Aplica un pequeño ruido uniforme a SO2. Ver anomalia_pm10."""
    raise NotImplementedError


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main() -> None:
    """
    Inicializa el cliente MQTT, se suscribe con wildcard a todos los
    tópicos del scraper y entra en un bucle que cada PUBLISH_EVERY_S
    segundos republica los últimos datos conocidos con ruido añadido.

    TODO:
      - Conectar el cliente MQTT y activar loop_start().
      - Iterar sobre latest_by_city, aplicar las funciones de perturbación
        y publicar en MQTT_TOPIC_PUBLICATE con el city_key correcto.
      - Actualizar el campo 'ingested_at' en cada publicación.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
