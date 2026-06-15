# Proyecto: Análisis Estadístico Multivariante

Proyecto académico de análisis estadístico multivariante aplicado a datos reales de la NBA. Se aplican técnicas de exploración, reducción de dimensionalidad, clustering y clasificación sobre medidas físicas de jugadores en el proceso de selección (Draft), con el objetivo de identificar qué cualidades físicas influyen en la probabilidad de ser elegido.

---

## 📂 Contenido del repositorio

| Archivo | Descripción |
|--------|-------------|
| `proyecto_multivariante_MUESTRA.pdf` | Informe *parcial* con algunos análisis, gráficos e interpretaciones |
| `proyecto_multivariante_MUESTRA.qmd` | Documento fuente *parcial* en Quarto (R + Markdown), reproducible en RStudio |
| `nba_draft_combine_all_years.csv` | Dataset con medidas físicas de jugadores del Draft NBA (2009–2017) |

---

## 📊 Dataset: `nba_draft_combine_all_years.csv`

- **Fuente:** [data.world/achou/nba-draft-combine-measurements](https://data.world/achou/nba-draft-combine-measurements)
- **Dimensiones:** 517 jugadores × 19 variables
- **Periodo:** temporadas NBA 2009 a 2017

### Variables incluidas

| Variable | Descripción |
|----------|-------------|
| `Player` | Nombre del jugador |
| `Year` | Año del Draft |
| `Draft pick` | Posición en el Draft (NA si no fue seleccionado) |
| `Height (No Shoes)` | Altura sin calzado (en pulgadas) |
| `Height (With Shoes)` | Altura con calzado (en pulgadas) |
| `Wingspan` | Envergadura: distancia entre puntas de dedos con brazos extendidos |
| `Standing reach` | Altura máxima con brazos extendidos sin saltar |
| `Vertical (Max)` | Altura máxima de salto con carrerilla |
| `Vertical (Max Reach)` | Altura de salto con carrerilla + altura del jugador |
| `Vertical (No Step)` | Altura máxima de salto sin carrerilla |
| `Vertical (No Step Reach)` | Altura de salto sin carrerilla + altura del jugador |
| `Weight` | Peso (en libras) |
| `Body Fat` | Porcentaje de grasa corporal |
| `Hand (Length)` | Longitud de la mano |
| `Hand (Width)` | Anchura de la mano |
| `Bench` | Repeticiones en press de banca a 84 kg |
| `Agility` | Tiempo en prueba de agilidad (menor = más ágil) |
| `Sprint` | Tiempo en prueba de velocidad (menor = más rápido) |

> **Nota de unidades:** las alturas están en pulgadas (÷ 39.37 → metros) y los pesos en libras (÷ 2.2046 → kg).

---

## 🧪 Técnicas aplicadas

### 1. Análisis exploratorio y limpieza de datos
- Detección y cuantificación de valores faltantes por variable
- Imputación razonada: media para valores puntuales (altura con zapatos, peso); estimación basada en literatura deportiva para grasa corporal (~10.5% del peso); redondeo a valores discretos observados para medidas de mano
- Análisis de patrones de missingness entre variables relacionadas (verticales, manos, agilidad/sprint)
- Eliminación de variables redundantes (`Height With Shoes`, `Vertical Max Reach`, `Vertical No Step Reach`, `Bench`) y de individuos con datos faltantes en variables clave
- Dataset final analizado: **403 jugadores × 11 variables**

### 2. Análisis de Componentes Principales (PCA)
- Matriz de correlaciones y visualización de pares de variables
- Extracción e interpretación de las dos primeras componentes principales:
  - **Y₁:** Componente de "tamaño físico" (altura, envergadura, peso, standing reach)
  - **Y₂:** Componente de "atletismo" (salto, velocidad, agilidad, baja grasa corporal)
- Biplot con localización de jugadores individuales (e.g., Nolan Smith)
- Selección del número de componentes mediante regla de Rao, regla del codo y prueba de esfericidad
- Validación de la relación entre posición en el PCA y Draft pick

### 3. Análisis de Clústeres
- Escalado previo de variables
- Determinación del número óptimo de grupos con `NbClust` (método complete linkage)
- Estadísticos de validación: índice de Hubert y diferencias de segundo orden

### 4. Análisis Discriminante
- Clasificación supervisada de jugadores según grupos identificados en el clustering
- Uso del paquete `MASS` con función `lda()`

### 5. Regresión
- Regresión lineal y múltiple
- Regresión logística (variable respuesta: seleccionado / no seleccionado en el Draft)

---

## 🛠️ Herramientas utilizadas

- **Lenguaje:** R
- **Entorno:** RStudio + Quarto (`.qmd`)
- **Paquetes principales:** `mvtnorm`, `Hmisc`, `NbClust`, `factoextra`, `cluster`, `ggplot2`, `stats`, `MASS`

---

## 🧑‍💻 Autor

**Javier García Fernández**  
Grado en Ciencia e Ingeniería de Datos  
Facultad de Informática, Universidad de Murcia

---

## 📎 Notas

- Este repositorio contiene únicamente una **muestra ilustrativa** del proyecto; no se incluye el código fuente completo por motivos de protección académica.
- Curso académico: 2023/24.

---

## 🛡️ Licencia

Disponible únicamente con fines demostrativos y académicos.  
No se autoriza su reproducción ni distribución sin consentimiento del autor.
