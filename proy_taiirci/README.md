# AQ-IIoT Lab — Monitorización de Calidad del Aire (Valencia · Alicante · Eivissa)

Proyecto académico de la asignatura **Tecnologías Avanzadas de Internet en la Industria, Redes, Comunicaciones e Infraestructuras** (curso 2025/2026).  
Implementa una arquitectura **IIoT de extremo a extremo** para la monitorización en tiempo real de la calidad del aire en el triángulo geográfico Valencia–Alicante–Eivissa, desde la adquisición de datos públicos hasta su visualización en Grafana con detección de anomalías y alertas.

Realizado por: **Javier García Fernández · Juan Andrés Álvarez Cascales**

---

## 📐 Arquitectura general

```
EEA (API) ──► Scraper ──► MQTT Broker ──► Intermediario ──► OPC-UA Server
                                                                    │
                                                               Telegraf (Starlark)
                                                                    │
                                                    ┌───────────────┴────────────────┐
                                                    │                                │
                                               InfluxDB                         MQTT Broker
                                                    │                                │
                                               Grafana                    ┌──────────┴──────────┐
                                                    │              CEP Consumer v2    Protobuf Serializer
                                             Alertas Telegram                              │
                                                                               proto_influx_consumer
                                                                                           │
                                                                                       InfluxDB
```

El sistema opera con **múltiples frecuencias por capa**, ajustadas a la naturaleza de cada componente:

| Capa | Frecuencia | Motivo |
|---|---|---|
| Scraper EEA | 1 hora | Cadencia de actualización de la API |
| Intermediario MQTT | 1 segundo | Forzar cambios en OPC-UA para generar notificaciones continuas |
| Telegraf (sampling) | 1 segundo | Granularidad necesaria para el motor CEP |
| CEP (evaluación) | ~9 eventos/s | 3 ciudades × 3 contaminantes |

---

## 🗂️ Estructura del repositorio

```
.
├── python/
│   ├── scraper_mqtt_MUESTRA.py            # Adquisición EEA → MQTT
│   ├── intermediario_suscripcion_MUESTRA.py  # Pipes and Filters (ruido periódico)
│   ├── opcua_server_bridge_MUESTRA.py     # Bridge MQTT → OPC-UA
│   ├── cep_consumer_v2_MUESTRA.py         # Motor CEP con 3 reglas + Telegram
│   ├── protobuf_serializer_MUESTRA.py     # JSON → Protobuf binario
│   ├── proto_influx_consumer_MUESTRA.py   # Protobuf → InfluxDB
│   └── sensor_data_pb2_MUESTRA.py        # Clase generada por protoc
├── docker-compose_MUESTRA.yml
├── telegraf/
│   └── telegraf.conf                      # Configuración Telegraf (no incluida en muestra)
├── mosquitto/
│   └── config/
│       └── mosquitto.conf
└── README.md
```

> **Nota sobre los ficheros `_MUESTRA`:** los archivos de código publicados son versiones parciales con la lógica de implementación eliminada. Conservan la estructura completa, los comentarios explicativos y el contrato de cada función (docstring con los pasos a seguir), pero sustituyen los cuerpos de las funciones clave por `raise NotImplementedError` o `pass`. Las memorias completas de ambas prácticas están disponibles en el repositorio.

---

## 🔧 Componentes

### 1. Web Scraper — `scraper_mqtt.py`

Consulta periódicamente la **EEA Air Quality Download Service** para obtener mediciones de PM10, NO2 y SO2 de las tres ciudades. El proceso interno:

1. Resuelve el nombre exacto de cada ciudad en la API (`resolve_city`).
2. Solicita un CSV con URLs a ficheros Apache **Parquet** por contaminante (`request_parquet_urls_csv`).
3. Filtra y ordena las URLs para priorizar los ficheros más recientes (`select_relevant_urls`).
4. Descarga cada Parquet y extrae el último valor válido, filtrando datos de los últimos 30 días disponibles (`download_and_extract_latest`).
5. Normaliza todas las muestras en un único `AirQualityRecord` calculando la media por contaminante cuando hay varias estaciones (`normalize_records`).
6. Publica un mensaje JSON por ciudad en `airquality/{city}/eea` (`publish_mqtt`).

**Decisión de diseño destacable:** Alicante tiene nombre compuesto con barra (`Alicante/Alacant`), lo que crearía un nivel extra en la jerarquía MQTT. Se normaliza reemplazando `/` y espacios por `_` para obtener un nombre de tópico plano sin ambigüedad.

---

### 2. Intermediario — `intermediario_suscripcion.py`

Componente propio que implementa el **patrón Pipes and Filters**. Motivación: la API de la EEA actualiza sus datos cada hora, lo que significa que el servidor OPC-UA (en modo suscripción) no genera notificaciones hacia Telegraf si los valores no cambian, paralizando el pipeline.

Solución: este script se suscribe a `airquality/+/eea`, aplica una pequeña perturbación aleatoria (ruido de ±0.5 µg/m³ en PM10, ±0.2 en NO2, ±0.1 en SO2) y republica en `airquality/{city}/eea_modified` cada segundo. El servidor OPC-UA siempre percibe un valor distinto y genera notificaciones continuas.

No modifica el scraper ni el servidor OPC-UA: actúa exclusivamente como filtro intermedio.

---

### 3. Servidor OPC-UA — `opcua_server_bridge.py`

Eleva los datos del mundo IoT al mundo industrial. Se suscribe a los tópicos `_modified`, parsea el JSON y actualiza los nodos OPC-UA correspondientes. Opera de forma asíncrona con `asyncio`.

**Árbol de nodos:**
```
Objects
  └─ AirQuality
       ├─ Valencia       → PM10, PM2_5, NO2, O3, SO2, CO, Timestamp, Station
       ├─ Alicante/Alacant → ...
       └─ Eivissa        → ...
```

**Decisión de diseño clave — NodeIds estáticos:** por defecto `asyncua` asigna NodeIds numéricos dinámicos (`ns=2;i=2`) que cambian entre reinicios. Se fuerzan NodeIds de tipo string predecibles (`ns=2;s=valencia_pm10`, `ns=2;s=eivissa_no2`, etc.) para poder configurar Telegraf de forma estática.

**Política last known good value:** si un contaminante llega como `None`, el nodo OPC-UA no se sobreescribe, conservando el último valor válido conocido y evitando saltos bruscos a cero en Grafana.

---

### 4. Telegraf + Starlark

Telegraf actúa como agente de adquisición en **modo suscripción OPC-UA** (`inputs.opcua_listener`), no en modo polling. Esto significa que el servidor OPC-UA notifica activamente a Telegraf cada vez que un nodo cambia de valor — de ahí la necesidad del intermediario.

**Salidas configuradas simultáneamente:**
- `[[outputs.influxdb_v2]]` → escribe en InfluxDB
- `[[outputs.mqtt]]` → publica en `telegraf/airquality` para el motor CEP y el serializador Protobuf

**Procesador Starlark — inyección de anomalías sintéticas:**

| Contaminante | Tipo de anomalía | Descripción |
|---|---|---|
| SO2 | Drift acumulativo | +0.3 µg/m³ por muestra; reset cada 50 muestras. Simula sensor que se ensucia progresivamente |
| PM10 | Ruido gaussiano (Box-Muller) | Probabilidad 25% por muestra. Simula fluctuaciones eléctricas o ráfagas de viento |
| NO2 | Onda sinusoidal | Amplitud ±20 µg/m³, ciclo de 60 muestras. Simula variación cíclica del tráfico urbano |

Los spikes periódicos (añadidos en la Práctica 2) garantizan que los valores crucen los umbrales de forma controlada para que el motor CEP pueda disparar alertas. Un contador global `counter_fire` sincroniza los tres contaminantes cada 90 métricas para simular un incendio.

**Configuración técnica clave:**
- `interval = "1s"`, `flush_interval = "1s"` en el bloque `[agent]`
- `subscription_interval = "1s"` en el `opcua_listener`
- En Docker: usar `172.17.0.1:1883` en lugar de `localhost:1883` para el broker MQTT

---

### 5. Motor CEP — `cep_consumer_v2.py`

Consumidor Python suscrito a `telegraf/#` que evalúa **tres reglas de detección** en tiempo real sobre cada evento recibido:

**Regla 1 — Umbral simple (Stateless):**  
Alerta en consola cuando un contaminante supera su límite en una sola lectura.

**Regla 2 — Ventana temporal / patrón secuencial (Stateful):**  
Detecta si el mismo contaminante supera el umbral **dos veces consecutivas en menos de 60 s** sin que entre un valor normal entre ellas. El estado (último valor, timestamp, flag de anomalía) se mantiene en memoria por ciudad y contaminante en `estado_ciudades`. Envía alerta por Telegram.

**Regla 3 — Correlación de incendio (Stateful):**  
Alerta crítica cuando PM10 + NO2 + SO2 están todos en estado de anomalía en la **misma ciudad** y con timestamps dentro de una ventana de 30 segundos. Correlación físicamente realista: un incendio genera simultáneamente humo (PM10) y gases de combustión (NO2, SO2). Incluye cooldown de 120 s por ciudad para evitar spam. Envía alerta por Telegram con recomendación de evacuación.

**Umbrales (Directiva europea 2024/2881 y OMS):**

| Contaminante | Umbral |
|---|---|
| PM10 | 45 µg/m³ |
| NO2 | 200 µg/m³ |
| SO2 | 125 µg/m³ |

**Regla EPL equivalente para la Regla 3:**
```sql
SELECT ciudad, pm10, no2, so2, timestamp
FROM AirQualityStream.win:time(30 sec)
WHERE pm10 > 45.0 AND no2 > 200.0 AND so2 > 125.0
GROUP BY ciudad
HAVING MAX(timestamp) - MIN(timestamp) <= 30
OUTPUT FIRST EVERY 120 seconds
-> TRIGGER ALERT "POSIBLE INCENDIO: EVACUAR " + ciudad
```

**Edge vs. Cloud:** el motor CEP corre en la misma máquina que el broker MQTT, actuando como Edge node. La latencia de red de un motor Cloud haría imposible cumplir requisitos de detección en tiempo real.

---

### 6. Serialización Protobuf — `protobuf_serializer.py` + `proto_influx_consumer.py`

**Esquema `sensor_data.proto` — mensaje `AirQualityEvent` (13 campos):**

```protobuf
syntax = "proto3";
package airquality;

message AirQualityEvent {
  string name          = 1;   // measurement (ciudad_group)
  int64  timestamp     = 2;   // Unix segundos — int64 ocupa ~5B vs ~25B del ISO 8601
  double pm10          = 3;
  double no2           = 4;
  double so2           = 5;
  string city          = 6;
  string project       = 7;
  string asset_id      = 8;
  string location      = 9;
  string host          = 10;
  string node_id       = 11;
  string anomaly       = 12;
  string anomaly_type  = 13;
}
```

Generar la clase Python: `python -m grpc_tools.protoc -I. --python_out=. sensor_data.proto`

**Resultados del análisis comparativo (100 eventos):**

| | JSON | Protobuf | Ahorro |
|---|---|---|---|
| Promedio por evento | 321.5 bytes | 133.7 bytes | **~58%** |

El ahorro se debe principalmente a: ausencia de claves de campo (sustituidas por tags de 1-2 bytes), timestamp como `int64` varint (~5 B vs ~25 B), y omisión de campos con valor cero.

**Pipeline Protobuf:**
```
MQTT(telegraf/airquality)
    → protobuf_serializer.py  → MQTT(telegraf/airquality/proto)
                                     → proto_influx_consumer.py → InfluxDB(air_quality_proto)
```

---

### 7. InfluxDB + Grafana

**Modelo de datos (measurement `air_quality_proto`):**

| Componente | Valores | Justificación |
|---|---|---|
| Tags | `city`, `anomaly`, `anomaly_type`, `project`, `location` | Baja cardinalidad, indexados → filtros O(log n) |
| Fields | `pm10`, `no2`, `so2` | Alta cardinalidad, no se filtran → values |
| Timestamp | Del mensaje Protobuf | Actualizado cada segundo → cada punto es único |

**Dashboards en Grafana:** panel Time series de PM10 por ciudad (últimos 5 min) y gauge de NO2 (valor actual). Alerta configurada sobre PM10 > 45 µg/m³ con notificación al bot de Telegram.

---

## 🚀 Ejecución

Orden de arranque (siempre en este orden):

```bash
# Terminal 1 — Infraestructura Docker
cd /opt/aq-iiot-lab
docker compose up -d

# Terminal 2 — Servidor OPC-UA (arrancar ANTES de Telegraf)
cd /opt/aq-iiot-lab/python && source venv/bin/activate
python3 opcua_server_bridge.py
# Una vez activo, reiniciar Telegraf:
# docker compose restart telegraf

# Terminal 3 — Intermediario
python3 intermediario_suscripcion.py

# Terminal 4 — Scraper
python3 scraper_mqtt.py

# Terminal 5 — Verificación MQTT (opcional)
mosquitto_sub -h localhost -p 1883 -t "telegraf/#" -v

# Terminal 6 — Motor CEP y consumidor Protobuf
python3 cep_consumer_v2.py
python3 protobuf_serializer.py
python3 proto_influx_consumer.py
```

**Errores frecuentes y soluciones:**

| Error | Causa | Solución |
|---|---|---|
| Telegraf: `Exited` al levantar | Servidor OPC-UA no está activo | Arrancar `opcua_server_bridge.py` primero, luego `docker compose restart telegraf` |
| `dial tcp [::1]:1883 connection refused` | Telegraf intenta conectar a `localhost` dentro de Docker | Cambiar `servers` a `["tcp://172.17.0.1:1883"]` en `telegraf.conf` |
| `topic_prefix not used` | Parámetro incorrecto en Telegraf 1.37+ | Usar `topic = "telegraf/airquality"` (no `topic_prefix`) |

---

## 🛠️ Stack tecnológico

| Categoría | Tecnología |
|---|---|
| Lenguaje | Python 3.12 |
| Mensajería IoT | MQTT (Eclipse Mosquitto 2) |
| Protocolo industrial | OPC-UA (`asyncua`) |
| Agente de métricas | Telegraf 1.37 (plugin `opcua_listener`, procesador `starlark`) |
| Serialización binaria | Protocol Buffers 3 (`grpcio-tools`) |
| Base de datos | InfluxDB 2 (Flux query language) |
| Visualización | Grafana |
| Motor CEP | Python (implementación propia, stateful) |
| Actuador | Telegram Bot API |
| Infraestructura | Docker Compose |
| Cliente MQTT Python | `paho-mqtt` |
| HTTP / Parquet | `requests`, `pandas`, `pyarrow` |

---

## 📄 Memorias

Las memorias completas de ambas prácticas están incluidas en el repositorio:

- `Memoria_Práctica_1_TAIIRCI.pdf` — Arquitectura base: scraper, MQTT, OPC-UA, Telegraf, InfluxDB, Grafana
- `Memoria_Práctica_2_TAIIRCI.pdf` — Ampliaciones: motor CEP, Telegram, Protobuf, almacenamiento en InfluxDB, validación de arquitectura

---

## 👤 Autores

Javier García Fernández · Juan Andrés Álvarez Cascales  
Grado en Ciencia e Ingeniería de Datos — Universidad de Murcia  
Tecnologías Avanzadas de Internet en la Industria, Redes, Comunicaciones e Infraestructuras — Curso 2025/2026
