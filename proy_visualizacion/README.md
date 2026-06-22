# Práctica Dash: Dashboard de Análisis de Influencers en Redes Sociales

Práctica académica grupal de la asignatura **Visualización de Datos** (curso 2024/2025). El proyecto tiene dos partes diferenciadas: ejercicios introductorios de visualización interactiva con Plotly Express y un dashboard completo construido con Dash y Plotly para el análisis de influencers en Instagram, TikTok y YouTube.

---

## 📂 Contenido del repositorio

| Archivo | Descripción |
|--------|-------------|
| `app.py` | Aplicación Dash completa: preprocesamiento, layout y callbacks del dashboard |
| `Parte_Visualizaciones.ipynb` | Notebook con los ejercicios introductorios de Plotly Express (10 ejercicios sobre dos datasets) |
| `Explicación_Dash.pdf` | Memoria técnica del dashboard: selección del dataset, preprocesamiento, estructura y diseño por plataforma |

---

## 📊 Datasets utilizados

### Dashboard (`app.py`)
Dataset **"Social Media Influencers in 2022"** disponible en [Kaggle](https://www.kaggle.com/datasets/ramjasmaurya/top-1000-social-media-channels) (descargado automáticamente con `kagglehub`). Tres archivos CSV, uno por plataforma, con datos de diciembre de 2022:

| Archivo | Variables principales |
|--------|----------------------|
| `social media influencers-INSTAGRAM - -DEC 2022.csv` | rank, username, category, category_2, followers, country, engagement_auth, engagement_avg |
| `social media influencers-TIKTOK - ---DEC 2022.csv` | rank, username, name, followers, views, likes, comments, shares |
| `social media influencers-YOUTUBE - --DEC 2022.csv` | name, username, category, category_2, country, followers, views, likes, comments |

### Ejercicios de visualización (`Parte_Visualizaciones.ipynb`)
- **Telco Customer Churn** (`WA_Fn-UseC_-Telco-Customer-Churn.csv`): datos de clientes de telecomunicaciones con variables como tipo de contrato, cargos mensuales, antigüedad y tasa de abandono
- **Gapminder** (`px.data.gapminder()`): dataset incluido en Plotly con PIB per cápita, esperanza de vida y población de 142 países entre 1952 y 2007

---

## 🗂️ Parte 1: Ejercicios de visualización con Plotly Express

**`Parte_Visualizaciones.ipynb`** — 10 ejercicios en dos casos de estudio.

### Caso de estudio 1 — Telco Customer Churn
- **Ejercicio 1:** Exploración y limpieza del dataset. Resumen de variables categóricas (frecuencias y valores únicos) y cuantitativas. Corrección de `SeniorCitizen` (codificada como 0/1, convertida a categoría 'No'/'Yes'). Visualización de `gender`, `SeniorCitizen`, `tenure` y `MonthlyCharges` con diagramas de barras, explorando `color`, `color_discrete_map`, `pattern_shape` y `pattern_shape_sequence`.
- **Ejercicio 2:** Diagrama de caja y bigotes de `MonthlyCharges` por tipo de `Contract`, con color y facetas por `PhoneService`.
- **Ejercicio 3:** Diagrama de dispersión de `tenure` vs `MonthlyCharges` con color por `PhoneService` y facetas por `Contract`.
- **Ejercicio 4:** Análisis agrupado `Contract` × `PhoneService` calculando media y recuento de `tenure` con `groupby` + `aggregate`.
- **Ejercicio 5:** Diagrama de dispersión de tasa de abandono (`Churn`) por `tenure` y `MonthlyCharges` con facetas por `Contract`, histogramas marginales y transparencia.

### Caso de estudio 2 — Gapminder
- **Ejercicio 6:** Exploración del dataset: 142 países, años de 1952 a 2007 en intervalos de 5 años.
- **Ejercicio 7:** Scatter plot estático de PIB per cápita vs esperanza de vida para 1952 con escala logarítmica, color por continente y tamaño por población.
- **Ejercicio 8:** Scatter plot **dinámico** con `animation_frame='year'` mostrando la evolución temporal de PIB per cápita y esperanza de vida en todos los países.
- **Ejercicio 9:** Diagrama de barras de población por continente en 2007, con desglose por países dentro de cada barra.
- **Ejercicio 10:** Diagrama de barras **dinámico** con `animation_frame='year'` mostrando la evolución de la población de los países europeos a lo largo del tiempo.

---

## 🖥️ Parte 2: Dashboard Dash (`app.py`)

Aplicación web interactiva que se ejecuta localmente en `http://127.0.0.1:8050`. Organizada en cuatro pestañas y construida con callbacks reactivos.

### Preprocesamiento
Para cada plataforma se aplica:
- Eliminación de duplicados
- Conversión de variables numéricas codificadas como texto (sufijos `M` y `K` → float)
- Renombrado de columnas para nomenclatura consistente entre los tres datasets
- Cálculo de `engagement_rate` como métrica adicional:
  - Instagram: `engagement_avg / followers × 100`
  - TikTok: `(likes + comments + shares) / followers × 100`
  - YouTube: `(likes + comments) / followers × 100`
- Normalización de la columna `name` (minúsculas, sin espacios ni guiones) para el cruce entre plataformas, resultando en **11 creadores presentes en las tres plataformas simultáneamente**

### Estructura del dashboard

El layout principal incluye encabezado, cuatro pestañas (`dcc.Tabs`/`dcc.Tab`), contenedor dinámico `platform-content` y pie de página. Un callback central (`@callback`) escucha la pestaña activa y devuelve el layout correspondiente.

Esquema de colores: Instagram naranja (`#FFA500`), TikTok azul marino (`#000080`), YouTube rojo (`#FF0000`), Más mediáticos dorado (`#CDA434`), fondo azul claro (`#E0F7FA`).

---

### 📷 Pestaña Instagram

**Filtros:** dropdown de categoría, dropdown de país, slider de top N influencers (10–100, paso 10, por defecto 30).

**Resumen de métricas:** total de influencers, promedio de seguidores, promedio de engagement rate, máximo de seguidores y top influencer.

**Gráficos:**

| Gráfico | Tipo | Descripción |
|---------|------|-------------|
| Top influencers más relevantes | Barras horizontales | Ordenado por `rank`; longitud = seguidores; color = `engagement_rate` (escala Purples) |
| Tasa de Engagement vs Seguidores | Scatter (log X) | Tamaño proporcional a seguidores; color por categoría |
| Distribución por categoría | Pie (donut) | Proporción de influencers por categoría principal |
| Distribución geográfica | Mapa choropleth | Concentración de influencers por país |
| Estudio de subcategorías | Barras apiladas | Distribución de `category_2` dentro de cada `category` con paleta de colores personalizada (sin repeticiones) |
| Ficha de influencer | Dropdown + lista | Selección de cuenta individual y visualización de sus métricas completas |

---

### 🎵 Pestaña TikTok

**Filtros:** slider de mínimo de seguidores (1M–100M), slider de top N influencers.

**Resumen de métricas:** total, promedio de seguidores, promedio de visualizaciones, promedio de likes, promedio de engagement rate.

**Gráficos:**

| Gráfico | Tipo | Descripción |
|---------|------|-------------|
| Top influencers más relevantes | Barras horizontales | Ordenado por `rank`; color = `engagement_rate` (escala Turbo) |
| Análisis Views vs Likes | Scatter (log X, log Y) | Correlación vistas-likes; tamaño = seguidores; color = engagement rate |
| Followers vs Engagement | Scatter (log X) | Seguidores vs tasa de engagement; color = promedio de likes; puntos de tamaño fijo |
| Compartidos vs Comentarios | Scatter (log X, log Y) | Correlación shares-comments; tamaño = seguidores; color = likes |
| Gráfico de radar | `go.Scatterpolar` | Métricas (followers, views, likes, comments, shares) de la cuenta seleccionada |
| Ficha de tiktoker | Dropdown + lista | Métricas individuales de la cuenta seleccionada |

---

### ▶️ Pestaña YouTube

**Filtros:** dropdown de categoría, dropdown de país, slider de top N influencers.

**Resumen de métricas:** total, promedio de seguidores, promedio de engagement rate, máximo de seguidores y top influencer.

**Gráficos:**

| Gráfico | Tipo | Descripción |
|---------|------|-------------|
| Top influencers con más seguidores | Barras horizontales | Ordenado por `followers`; color = `engagement_rate` |
| Followers vs Visitas | Scatter | Seguidores vs visualizaciones; tamaño = seguidores; color por categoría |
| Distribución por categoría | Pie (donut) | Proporción de canales por categoría |
| Distribución geográfica | Mapa choropleth | Concentración de canales por país |
| Análisis País vs Categoría | Barras apiladas | Visualizaciones totales por categoría, desglosadas por país (paleta sin repeticiones) |
| Ficha de canal | Dropdown + lista | Métricas individuales del canal seleccionado |

---

### 🌟 Pestaña Más mediáticos

Muestra los **11 creadores activos simultáneamente en las tres plataformas**, identificados por unión (`merge`) de los tres datasets sobre el campo `name` normalizado.

**Gráficos:**
- Barras agrupadas comparando `engagement_rate` por plataforma para los top 15 creadores (ordenados por suma de engagement en las tres redes)
- Top 10 por `ig_engagement_rate` (barras horizontales, naranja)
- Top 10 por `tt_engagement_rate` (barras horizontales, azul marino)
- Top 10 por `yt_engagement_rate` (barras horizontales, rojo)

---

## 🛠️ Tecnologías

- **Python:** Dash, Plotly Express, Plotly Graph Objects, Pandas, kagglehub
- **Estilos:** hoja externa CSS de Codepen (`bWLwgP.css`)
- **Ejecución:** `python app.py` → `http://127.0.0.1:8050`

---

## ▶️ Cómo ejecutar

```bash
pip install dash plotly pandas kagglehub
python app.py
```

El dataset se descarga automáticamente desde Kaggle al ejecutar el script (requiere tener `kagglehub` configurado con credenciales de Kaggle). Una vez en ejecución, abrir `http://127.0.0.1:8050` en el navegador.

---

## 👥 Autores

Javier García Fernández · Miguel Ángel Véliz Ayala  
Grupo 11 — Visualización de Datos, curso 2024/2025  
Universidad de Murcia · Profesor: Juan Manuel Carrillo De Gea
