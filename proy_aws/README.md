# Proyecto AWS Serverless

Este repositorio contiene la documentación y el diseño de una infraestructura **serverless** desarrollada como parte de un proyecto académico sobre servicios en la nube con **AWS**. El proyecto se centra en la implementación de un servicio web sin servidores, el tratamiento de datos mediante funciones Lambda y el uso de diversos servicios gestionados de Amazon.

## 📄 Contenido del repositorio

- `proyecto.pdf`: Memoria explicativa que incluye el diseño, el código, la justificación técnica y pruebas realizadas.
- `infraestructura.png`: Diagrama visual de la arquitectura desplegada.

## 🧰 Servicios de AWS utilizados

- **AWS Lambda**: Procesamiento sin servidor.
- **Amazon API Gateway**: Exposición de endpoints web.
- **Amazon DynamoDB**: Base de datos NoSQL para almacenamiento de datos.
- **Amazon SNS**: Envío de notificaciones automáticas.
- **Amazon S3**: Almacenamiento de archivos y eventos asociados.

## 🧪 Funcionalidades implementadas

- Consulta de datos mediante una función Lambda integrada con API Gateway.
- Envío automático de alertas vía SNS tras determinados eventos.
- Procesamiento automático de archivos CSV almacenados en S3, con actualización de estadísticos.
- Desencadenamiento de funciones Lambda a través de eventos de S3.

## 📎 Nota

El código fuente se encuentra embebido dentro del documento PDF (`proyecto.pdf`).  
Este repositorio se publica exclusivamente con fines demostrativos y académicos.

## 🧑‍💻 Autor

Javier García Fernández  
Grado en Ciencia e Ingeniería de Datos

## 🛡️ Licencia

Contenido disponible solo para revisión académica o profesional.  
No se autoriza la reproducción o reutilización del material sin consentimiento previo.
