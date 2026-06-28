#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AQ-IIoT Lab — Bridge MQTT → OPC-UA (múltiples ciudades)

Objetivo:
  - Suscribirse a los tópicos MQTT de cada ciudad (tópicos _modified
    publicados por el intermediario).
  - Exponer los datos como variables OPC-UA bajo un árbol con un nivel
    por ciudad:
      Objects → AirQuality → {Valencia, Alicante, Eivissa}
                           → {PM10, PM2_5, NO2, O3, SO2, CO, Timestamp, Station}

Decisión de diseño clave — NodeIds estáticos:
  La librería asyncua asigna NodeIds numéricos dinámicos por defecto
  (p. ej. ns=2;i=2), que pueden cambiar entre reinicios. Esto impide
  configurar Telegraf de forma estática apuntando a nodos concretos.

  Solución: forzar un NodeId de tipo string por nodo, construido a
  partir del nombre de ciudad y contaminante:
    ns=2;s=valencia_pm10, ns=2;s=eivissa_no2, etc.

  Esto genera identificadores predecibles que pueden configurarse
  directamente en telegraf.conf sin riesgo de cambio entre reinicios.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

import paho.mqtt.client as mqtt
from asyncua import Server, ua


# -----------------------------------------------------------------------------
# Configuración
# -----------------------------------------------------------------------------
MQTT_HOST  = "localhost"
MQTT_PORT  = 1883
CITY_NAMES = ["Valencia", "Alicante/Alacant", "Eivissa"]

MQTT_TOPIC_SUBSCRIBE = "airquality/+/eea_modified"
OPCUA_ENDPOINT = "opc.tcp://0.0.0.0:4840/airquality/"
NAMESPACE_URI  = "urn:iot_hub:airquality"


# -----------------------------------------------------------------------------
# Modelo interno
# -----------------------------------------------------------------------------
@dataclass
class AirQualityPayload:
    timestamp: str = ''
    station:   Optional[str]   = None
    pm10:      Optional[float] = None
    pm2_5:     Optional[float] = None
    no2:       Optional[float] = None
    o3:        Optional[float] = None
    so2:       Optional[float] = None
    co:        Optional[float] = None


# -----------------------------------------------------------------------------
# Estado compartido
# -----------------------------------------------------------------------------
latest_by_city: Dict[str, Dict[str, Any]] = {}


# -----------------------------------------------------------------------------
# MQTT callbacks
# -----------------------------------------------------------------------------
def on_message(client, userdata, msg) -> None:
    """
    Extrae la ciudad del tópico (airquality/<city>/eea_modified)
    y almacena el payload JSON en latest_by_city.
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


def parse_payload(raw: Dict[str, Any]) -> AirQualityPayload:
    """
    Convierte el JSON MQTT a un objeto tipado AirQualityPayload.
    Usa .get() para todos los campos opcionales: si un contaminante
    llega como None el campo queda como None (política last known good
    value aplicada después en update_nodes).
    """
    record = AirQualityPayload()
    for field in record.__dataclass_fields__:
        value = raw.get(field)
        if field in ["timestamp", "station"]:
            setattr(record, field, str(value) if value is not None else "")
        else:
            try:
                setattr(record, field, float(value) if value is not None else None)
            except (ValueError, TypeError):
                setattr(record, field, None)
    return record


# -----------------------------------------------------------------------------
# OPC-UA: creación del modelo
# -----------------------------------------------------------------------------
async def create_server() -> tuple[Server, int]:
    """Inicializa el servidor OPC-UA y registra el namespace."""
    server = Server()
    await server.init()
    server.set_endpoint(OPCUA_ENDPOINT)
    server.set_server_name("Air Quality OPC-UA Server (Lab)")
    idx = await server.register_namespace(NAMESPACE_URI)
    return server, idx


async def create_nodes(server: Server, idx: int, city_names: list[str]) -> Dict[str, Dict[str, Any]]:
    """
    Construye el árbol OPC-UA completo:

      Objects
        └─ AirQuality
             ├─ Valencia   → PM10, PM2_5, NO2, O3, SO2, CO, Timestamp, Station
             ├─ Alicante/Alacant → ...
             └─ Eivissa    → ...

    Todos los nodos se crean con NodeId de tipo string estático para que
    Telegraf pueda referenciarlos de forma predecible (ver docstring del módulo).

    TODO: implementar la creación del nodo raíz 'AirQuality', iterar sobre
          city_names, crear un objeto hijo por ciudad y dentro de él las
          ocho variables con ua.NodeId(f"{city_key}_{campo}", idx).
          Marcar todos como set_writable() y devolver nodes_by_city.
    """
    # --- implementación eliminada como muestra ---
    raise NotImplementedError


async def update_nodes(nodes: Dict[str, Any], aq: AirQualityPayload) -> None:
    """
    Escribe los valores de AirQualityPayload en los nodos OPC-UA.

    Política last known good value: si un campo es None no se
    sobreescribe el nodo, conservando el último valor válido conocido.
    Esto evita saltos bruscos a cero en Grafana por ausencias de dato.

    TODO: iterar sobre los campos del dataclass, obtener el valor con
          getattr y llamar a node.write_value(value) sólo si no es None.
    """
    # --- implementación eliminada como muestra ---
    raise NotImplementedError


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
async def main() -> None:
    """
    Inicializa el cliente MQTT y el servidor OPC-UA de forma concurrente.
    El bucle principal itera cada segundo sobre latest_by_city y actualiza
    los nodos OPC-UA con los últimos datos recibidos.

    Nota: asyncio permite que el servidor OPC-UA no bloquee el hilo
    principal, de modo que los mensajes MQTT siguen recibiéndose mientras
    se actualizan los nodos.

    TODO:
      - Conectar cliente MQTT con on_message y activar loop_start().
      - Llamar a create_server() y create_nodes().
      - Dentro de 'async with server:', bucle while True que llame a
        parse_payload() y update_nodes() para cada ciudad en latest_by_city.
    """
    raise NotImplementedError


if __name__ == "__main__":
    asyncio.run(main())
