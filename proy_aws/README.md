# Proyecto: AquaSenseCloud

Proyecto académico grupal que implementa una infraestructura **serverless** completa en **AWS** para el procesamiento y consulta de datos de temperatura. El sistema recibe ficheros CSV con medidas de temperatura diarias, calcula estadísticos mensuales de forma automática, los almacena en una base de datos NoSQL y los expone a través de una API REST. Además, incluye un sistema de alertas por correo electrónico cuando la desviación estándar supera un umbral definido.

---

## 📂 Contenido del repositorio

| Archivo | Descripción |
|--------|-------------|
| `proy-documentacion-grupo11_version_definitiva.pdf` | Memoria técnica completa del proyecto: diseño, implementación, justificaciones y pruebas |
| `proy-diagrama.pdf` | Diagrama visual de la arquitectura AWS desplegada |
| `Temperatura.csv` | Dataset de temperaturas medias y desviaciones estándar diarias (2017–2024) |

---

## 📊 Dataset: `Temperatura.csv`

Dataset de temperaturas utilizado para testear el pipeline de datos del sistema.

- **Dimensiones:** 384 registros × 3 columnas
- **Periodo:** marzo 2017 – julio 2024

### Variables

| Variable | Descripción |
|----------|-------------|
| `Fecha` | Fecha de la medición (`YYYY/MM/DD`) |
| `Medias` | Temperatura media diaria (en °C) |
| `Desviaciones` | Desviación estándar de la temperatura diaria |

### Distribución por año

| Año | Registros |
|-----|-----------|
| 2017 | 34 |
| 2018 | 46 |
| 2019 | 57 |
| 2020 | 60 |
| 2021 | 55 |
| 2022 | 52 |
| 2023 | 52 |
| 2024 | 28 |

> Para las pruebas del sistema, el fichero original de 384 registros se particionó en 10 ficheros de ~40 registros cada uno, subiéndolos secuencialmente al bucket S3 para validar la actualización incremental de los estadísticos en DynamoDB.

---

## 🏗️ Arquitectura

La infraestructura está desplegada íntegramente en AWS y se provisiona mediante **AWS CloudFormation** (plantilla `proy-infraestructura`). Consta de tres flujos principales:

### Pipeline de datos (S3 → Lambda → DynamoDB)
Un fichero CSV se sube al bucket S3 `landingzone-aquasensecloud`, lo que desencadena automáticamente la función Lambda `proy-lambda-statistics`. Esta función procesa cada fila del CSV, calcula o actualiza los estadísticos mensuales en la tabla DynamoDB `AquaSenseCloudDB`, y si la desviación estándar supera el umbral de 0.5, invoca a su vez la función `proy-lambda-notification`.

### Servicio de alertas (Lambda → SNS)
La función `proy-lambda-notification` publica un mensaje en el tema SNS `proy-sns-topic` (`ThresholdAlert`), que envía un correo personalizado con la fecha y el valor que superó el umbral a los usuarios suscritos.

### Servicio web (API Gateway → Lambda → DynamoDB)
Una API REST (`AquaSense-api`) expone tres endpoints HTTP GET que permiten consultar los estadísticos mensuales almacenados en DynamoDB, invocando la función Lambda `proy-lambda-WebService`.

---

## 🧰 Servicios de AWS utilizados

| Servicio | Rol en el proyecto |
|----------|--------------------|
| **Amazon S3** | Bucket de entrada (`landingzone-aquasensecloud`) donde se depositan los ficheros CSV |
| **AWS Lambda** | Tres funciones: `proy-lambda-statistics` (procesamiento CSV), `proy-lambda-notification` (alertas), `proy-lambda-WebService` (consultas API) |
| **Amazon DynamoDB** | Tabla `AquaSenseCloudDB` con clave de partición `Month&Year` y cinco claves de ordenación (`maxdiff`, `sd`, `temp`, `temp_max`, `num_day_set`) |
| **Amazon API Gateway** | API REST `AquaSense-api` con endpoints `/maxdiff`, `/sd` y `/temp` (método GET) |
| **Amazon SNS** | Tema `ThresholdAlert` con suscripción por correo electrónico para alertas de umbral |
| **AWS CloudFormation** | Provisioning automatizado de toda la infraestructura mediante plantilla `proy-infraestructura` |

---

## 🌐 API REST

La API expone tres endpoints HTTP GET en la región `us-east-1`:

| Endpoint | Descripción | Formato de respuesta |
|----------|-------------|----------------------|
| `GET /maxdiff?month=MM&year=YYYY` | Diferencia entre temperatura máxima del mes actual y la del mes anterior | `Real` |
| `GET /sd?month=MM&year=YYYY` | Máxima desviación estándar mensual registrada | `Real` |
| `GET /temp?month=MM&year=YYYY` | Temperatura media mensual y número de días procesados | `{"mean": Real, "days": Integer}` |

Ejemplo de respuesta real del sistema:
```json
{
  "Month&Year": "2017/03",
  "URI": "temp",
  "value": 17.0569839477539
}
```

---

## 🧮 Estadísticos calculados y almacenados

La función `proy-lambda-statistics` calcula y actualiza los siguientes estadísticos de forma incremental con cada fila del CSV procesada:

| Estadístico | Descripción | Lógica de actualización |
|-------------|-------------|-------------------------|
| `maxdiff` | Diferencia de temperatura máxima entre meses consecutivos | `temp_max_actual − temp_max_mes_anterior` |
| `sd` | Máxima desviación estándar mensual | `max(sd_actual, sd_nueva_fila)` |
| `temp` (mean) | Temperatura media mensual acumulada | `(media_actual × días + temp_nueva) / (días + 1)` |
| `temp_max` | Temperatura media máxima registrada en el mes | `max(temp_max_actual, temp_nueva)` |
| `num_day_set` | Conjunto de días ya procesados | Se añade el día de cada fila; evita reprocesar registros duplicados |

El umbral de alerta SNS se activa cuando `sd > 0.5`.

---

## 🔧 Funciones Lambda (Python 3.12)

### `proy-lambda-statistics`
Función principal del pipeline. Se dispara por eventos de S3 al subir un CSV. Módulos internos:
- `comprobar_umbral()` — verifica si `sd > 0.5` e invoca la notificación
- `obtener_datos_mes()` — consulta DynamoDB para un mes dado
- `obtener_partition_key()` — calcula las claves del mes actual, anterior y posterior
- `insert_or_upload_registers()` — inserta o actualiza registros en DynamoDB
- `calcular_nuevos_valores()` — recalcula estadísticos combinando datos existentes con los nuevos
- `procesar_fila()` — orquesta el procesamiento de cada fila del CSV

### `proy-lambda-WebService`
Recibe eventos de API Gateway, extrae parámetros de la URI, consulta DynamoDB y devuelve el resultado como JSON.

### `proy-lambda-notification`
Publica un mensaje personalizado en el tema SNS indicando la fecha y el valor de la desviación que superó el umbral. Tiempo de espera configurado a 5 minutos para evitar mensajes duplicados.

---

## 📋 Recursos desplegados

| Nombre | Tipo |
|--------|------|
| `landingzone-aquasensecloud` | Bucket S3 |
| `AquaSenseCloudDB` | Tabla DynamoDB |
| `AquaSense-api` | API REST (API Gateway) |
| `proy-lambda-WebService` | Función Lambda |
| `proy-lambda-statistics` | Función Lambda |
| `proy-lambda-notification` | Función Lambda |
| `proy-sns-topic` (`ThresholdAlert`) | Tema SNS |

---

## 🧪 Pruebas realizadas

- Particionado del CSV en 10 ficheros de ~40 registros y subida secuencial al bucket S3
- Verificación de actualización incremental de estadísticos en DynamoDB tras cada carga
- Comprobación de recepción de alertas por correo cuando `sd > 0.5`
- Validación de los tres endpoints de la API REST con diferentes parámetros de mes y año

---

## 👥 Autores

Víctor López Martínez · Javier García Fernández · Miguel Ángel Véliz Ayala  
Grado en Ciencia e Ingeniería de Datos  
Facultad de Informática, Universidad de Murcia · Universidad Politécnica de Cartagena  
Curso: 2024/2025 — Infraestructura para la Computación de Altas Prestaciones

---

## 🛡️ Licencia

Contenido disponible solo para revisión académica o profesional.  
No se autoriza la reproducción o reutilización del material sin consentimiento previo.
