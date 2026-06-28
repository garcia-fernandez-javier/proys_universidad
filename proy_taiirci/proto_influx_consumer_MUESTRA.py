#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AQ-IIoT Lab — Consumidor Protobuf → InfluxDB

Posición en la arquitectura:
  MQTT(telegraf/airquality/proto) → [este script] → InfluxDB

Modelo de datos en InfluxDB:
  ┌─────────────────┬──────────────────────────────────────────────────┐
  │ Measurement     │ air_quality_proto                                │
  ├─────────────────┼──────────────────────────────────────────────────┤
  │ Tags (índices)  │ city, anomaly, anomaly_type, project, location   │
  │                 │ Se indexan → búsquedas WHERE muy rápidas O(log n)│
  ├─────────────────┼──────────────────────────────────────────────────┤
  │ Fields (valores)│ pm10, no2, so2                                   │
  │                 │ Alta cardinalidad → NO indexar → son fields       │
  ├─────────────────┼──────────────────────────────────────────────────┤
  │ Timestamp       │ Del propio mensaje Protobuf (marca de Telegraf,  │
  │                 │ actualizada cada segundo → cada punto es único)   │
  └─────────────────┴──────────────────────────────────────────────────┘

Por qué 'city' debe ser tag y no field:
  Si fuera field, cada consulta filtrada por ciudad requeriría un
  escaneo O(n) sobre todos los puntos. Al ser tag, la búsqueda es
  O(log n) sobre el índice. Con millones de puntos la diferencia
  es determinante para el rendimiento de Grafana.
"""

import paho.mqtt.client as mqtt
from datetime import datetime, timezone

import sensor_data_pb2
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# -----------------------------------------------------------------------
# Configuración MQTT
# -----------------------------------------------------------------------
MQTT_HOST   = "localhost"
MQTT_PORT   = 1883
TOPIC_PROTO = "telegraf/airquality/proto"

# -----------------------------------------------------------------------
# Configuración InfluxDB
# -----------------------------------------------------------------------
INFLUX_URL    = "http://localhost:8086"
INFLUX_TOKEN  = "YOUR_INFLUX_TOKEN_HERE"
INFLUX_ORG    = "iot_hub"
INFLUX_BUCKET = "airq-Javi-Juan"
MEASUREMENT   = "air_quality_proto"

# -----------------------------------------------------------------------
# Cliente InfluxDB (modo síncrono: garantiza persistencia antes de
# procesar el siguiente mensaje, adecuado para este volumen de datos)
# -----------------------------------------------------------------------
influx_client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)


def proto_to_influx(proto_msg) -> Point:
    """
    Convierte un mensaje AirQualityEvent Protobuf en un Point de InfluxDB.

    Pasos:
      1. Convertir proto_msg.timestamp (Unix int64) a datetime UTC.
      2. Construir Point(MEASUREMENT).
      3. Añadir tags: city, anomaly, anomaly_type, project, location.
      4. Añadir fields: pm10, no2, so2.
      5. Añadir timestamp con .time(ts).

    TODO: implementar la lógica descrita arriba.
    """
    # --- implementación eliminada como muestra ---
    raise NotImplementedError


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Conectado al broker MQTT.")
    print(f"Suscrito a: {TOPIC_PROTO}")
    print(f"Escribiendo en InfluxDB: bucket={INFLUX_BUCKET}, measurement={MEASUREMENT}\n")
    client.subscribe(TOPIC_PROTO)


def on_message(client, userdata, msg):
    """
    Callback principal del consumidor Protobuf → InfluxDB.

    Pasos:
      1. Deserializar el binario con sensor_data_pb2.AirQualityEvent()
         y ParseFromString(msg.payload).
      2. Descartar eventos con pm10 == no2 == so2 == 0.0.
      3. Llamar a proto_to_influx() para construir el Point.
      4. Escribir en InfluxDB con write_api.write().
      5. Imprimir línea de log con timestamp, ciudad y valores.

    TODO: implementar la lógica descrita arriba.
    """
    # --- implementación eliminada como muestra ---
    pass


def main():
    print("=== Consumidor Protobuf → InfluxDB — AQ-IIoT Lab ===")
    print(f"Measurement: {MEASUREMENT}")
    print(f"Tags:   city, anomaly, anomaly_type, project, location")
    print(f"Fields: pm10, no2, so2\n")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
