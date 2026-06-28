#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AQ-IIoT Lab — Serializador Protobuf

Posición en la arquitectura:
  MQTT(telegraf/airquality) → [este script] → MQTT(telegraf/airquality/proto)

Funciones:
  1. Suscribirse al tópico de Telegraf y recibir mensajes JSON.
  2. Deserializar el JSON y reserializar como Protobuf binario usando
     la clase AirQualityEvent definida en sensor_data.proto.
  3. Publicar el binario en un nuevo tópico (preparado para Kafka).
  4. Medir y comparar tamaños JSON vs Protobuf.
  5. Tras TARGET_EVENTS eventos, imprimir la tabla comparativa y el
     porcentaje de ahorro medio.

Ventaja del timestamp como int64:
  En JSON el timestamp se codifica como string ISO 8601 (~25 bytes).
  En Protobuf, un int64 con varint ocupa ~5 bytes para valores Unix
  actuales (~1.7×10⁹). Ahorro: hasta 20 bytes sólo en este campo.
"""

import json
import paho.mqtt.client as mqtt
import sensor_data_pb2

MQTT_HOST  = "localhost"
MQTT_PORT  = 1883
TOPIC_IN   = "telegraf/#"
TOPIC_OUT  = "telegraf/airquality/proto"

TARGET_EVENTS = 100
resultados = []   # lista de {"json_bytes": x, "proto_bytes": y, "city": z, "contaminante": w}


def json_to_proto(evento: dict) -> bytes | None:
    """
    Convierte un evento JSON de Telegraf al formato Protobuf binario.
    Devuelve None si el evento no contiene campos de contaminantes.

    Pasos:
      1. Extraer fields y tags del dict.
      2. Leer pm10, no2, so2 (default 0.0 si ausentes).
      3. Si todos son 0.0, devolver None (evento sin contaminantes).
      4. Construir sensor_data_pb2.AirQualityEvent con todos los campos.
      5. Devolver msg.SerializeToString().

    TODO: implementar la lógica descrita arriba.
    """
    # --- implementación eliminada como muestra ---
    raise NotImplementedError


def imprimir_informe() -> None:
    """
    Imprime la tabla comparativa JSON vs Protobuf tras TARGET_EVENTS eventos.

    Formato esperado:
      #    Ciudad               JSON (bytes)  Proto (bytes)   Ahorro
      -------------------------------------------------------------------
      1    valencia                      320            133    58.4%
      ...
      TOTAL                           32000          13370    58.2%

      Promedio por evento:
        JSON:   320.0 bytes
        Proto:  133.7 bytes
        Ahorro: 58.2%

    TODO: iterar sobre 'resultados', calcular ahorro por fila y totales,
          e imprimir la tabla con format strings alineados.
    """
    # --- implementación eliminada como muestra ---
    raise NotImplementedError


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Conectado al broker MQTT.")
    print(f"Suscrito a: {TOPIC_IN}")
    print(f"Publicando Protobuf en: {TOPIC_OUT}")
    print(f"Analizando {TARGET_EVENTS} eventos para el informe comparativo...\n")
    client.subscribe(TOPIC_IN)


def on_message(client, userdata, msg):
    """
    Callback principal del serializador.

    Pasos:
      1. Ignorar mensajes del propio TOPIC_OUT (evitar bucle).
      2. Deserializar JSON del payload.
      3. Llamar a json_to_proto(); si devuelve None, descartar.
      4. Publicar el binario en TOPIC_OUT con qos=0, retain=False.
      5. Acumular en 'resultados' para el informe comparativo,
         identificando qué contaminante trae el evento.
      6. Cuando len(resultados) == TARGET_EVENTS: llamar a
         imprimir_informe() y limpiar resultados.

    TODO: implementar la lógica descrita arriba.
    """
    global resultados
    # --- implementación eliminada como muestra ---
    pass


def main():
    print("=== Serializador Protobuf — AQ-IIoT Lab ===")
    print(f"Esquema: AirQualityEvent (sensor_data.proto)")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
