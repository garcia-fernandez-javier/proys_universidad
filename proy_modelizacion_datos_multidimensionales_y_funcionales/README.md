# Proyecto de Modelización de Datos Multidimensionales y Funcionales

Proyecto académico grupal de la asignatura **Modelización de Datos Multidimensionales y Funcionales** (curso 2024/2025). El proyecto consta de dos partes completamente independientes: un análisis de dependencia multivariante mediante **Cópulas Vine** aplicado a activos financieros, y un análisis completo de **Datos Funcionales** sobre series climáticas del Pacífico ecuatorial.

---

## 📂 Contenido del repositorio

| Archivo | Descripción |
|--------|-------------|
| `proy_mdmf_v3.qmd` | Parte 1 — Modelización de dependencia con Vine Cópulas sobre rendimientos de acciones tecnológicas |
| `analisis_datos_funcionales_v2.qmd` | Parte 2 — Análisis estadístico funcional de temperaturas superficiales del mar (SST y SSTA) |

Ambos documentos están escritos en **Quarto** (`.qmd`) y generan un informe HTML autocontenido al renderizarse.

---

## 📈 Parte 1: Cópulas Vine — `proy_mdmf_v3.qmd`

### Origen de los datos

Los datos provienen de la API de **Alpha Vantage**, que proporciona series temporales ajustadas de mercados financieros. Se trabaja con precios de cierre ajustados semanales (`adjusted.close`) de cuatro grandes empresas tecnológicas estadounidenses:

| Símbolo | Empresa |
|---------|---------|
| `AAPL` | Apple |
| `MSFT` | Microsoft |
| `AMZN` | Amazon |
| `GOOGL` | Google (Alphabet) |

La ventana temporal compartida entre los cuatro activos abarca más de 20 años de historia. Los datos se descargan directamente desde la API mediante `httr` y `jsonlite`.

### Estructura del análisis

**1. Carga y origen de los datos**
Descarga de precios ajustados semanales mediante la función `get_alpha_vantage_data()`. Se accede a los cuatro activos en bucle y se almacenan en lista. La columna `adjusted.close` corrige por dividendos y splits, siendo la variable más representativa del retorno económico real.

**2. Preparación y exploración**
Los precios en niveles presentan correlaciones muy elevadas (Pearson ≈ 0.95), por ser casi redundantes como series integradas. Se transforman a **rendimientos logarítmicos** para estacionarizar:

$$r_t = \log(P_t) - \log(P_{t-1})$$

Las correlaciones entre rendimientos se reducen a un rango de 0.41–0.51 (Pearson), más relevante estadísticamente. Se obtienen matrices de correlación con tres métodos (Pearson, Spearman, Kendall) y gráficos de dispersión pareados.

**3. Ajuste de distribuciones marginales**
Para cada activo se comparan cuatro distribuciones candidatas mediante AIC/BIC:

- Normal
- t-Student generalizada
- Laplace
- Hiperbólica Generalizada

En todos los casos la **t-Student** resulta la más adecuada, evidenciando colas pesadas simétricas en los rendimientos.

**4. Transformación a pseudo-observaciones**
Aplicación del Teorema de Sklar: los datos se transforman al espacio $U[0,1]$ mediante rangos empíricos (`pobs()`), lo que permite separar la estructura de dependencia de las marginales.

**5. Selección y ajuste de Vine Cópula**
Selección automática de la estructura y familias mediante `RVineStructureSelect()`, comparando R-Vine y C-Vine con criterios AIC y BIC. El modelo óptimo es una **C-Vine con Google (GOOGL) como nodo central**, con cópulas **t-Student** en todos los pares:

- *Árbol 1* — Dependencias directas: Google empareja con los tres activos restantes (τ ≈ 0.36–0.38). Los bajos grados de libertad confirman dependencia de cola significativa.
- *Árboles 2 y 3* — Dependencias condicionales: una vez descontado Google, la dependencia residual entre Apple y Amazon cae a τ ≈ 0.11, revelando que su comovimiento es principalmente inducido por el actor central.

AIC y BIC convergen en la misma estructura, lo que aporta robustez al resultado.

**6. Diagnóstico y validación**
Test de bondad de ajuste de Breymann (`RVineGofTest`) con 10.000 simulaciones. El modelo supera el umbral p > 0.05, descartando el rechazo.

**7. Simulación**
Generación de `n` muestras sintéticas desde el modelo ajustado (`RVineSim`) y transformación inversa a escala original mediante cuantiles de la t-Student. Comparación visual entre datos originales y simulados mediante `pairs()` con escalas comunes.

**8. Conclusión**
Los rendimientos de activos tecnológicos presentan colas pesadas y dependencia de cola simétrica, incompatibles con modelos gaussianos. La C-Vine con Google como nodo central captura adecuadamente la estructura de dependencia multivariante, con consistencia total entre criterios AIC y BIC.

### Tecnologías

- **R:** `VineCopula`, `copula`, `fitdistrplus`, `ghyp`, `fGarch`, `httr`, `jsonlite`, `ggplot2`, `MASS`
- **Quarto** para renderizado de informe HTML

---

## 🌊 Parte 2: Análisis de Datos Funcionales — `analisis_datos_funcionales_v2.qmd`

### Origen de los datos

Datos de **OISST v2.1** (Optimum Interpolation Sea Surface Temperature), descargados directamente de la NOAA. Comprenden observaciones semanales desde el **2 de septiembre de 1982** hasta el **12 de noviembre de 2025** de cuatro regiones estándar del Pacífico ecuatorial:

| Región | Ubicación geográfica | Característica principal |
|--------|---------------------|--------------------------|
| **NINO 1+2** | 0–10°S, 90°W–80°W | Costa de Sudamérica; zona de afloramiento, muy volátil |
| **NINO 3** | 5°N–5°S, 150°W–90°W | Pacífico Oriental; exhibe la Barrera de Predictibilidad de Primavera |
| **NINO 3.4** | 5°N–5°S, 170°W–120°W | Referencia oficial ENSO; región de transición |
| **NINO 4** | 5°N–5°S, 160°E–150°W | Pacífico Occidental; "Piscina Cálida", muy estable |

Para cada región se dispone de dos variables: **SST** (temperatura superficial en °C) y **SSTA** (anomalía respecto al promedio histórico). El formato crudo concatena ambos valores en una sola cadena (`20.6-0.1`), lo que requiere un preprocesamiento dedicado.

### Estructura del análisis

**1. Introducción**
Fundamentos del Análisis de Datos Funcionales (ADF): tratamiento de observaciones como curvas en espacio de Hilbert. Justificación del enfoque funcional frente al multivariante clásico para capturar la evolución continua de señales climáticas.

**2. Conjunto de datos y preparación**
Pipeline de limpieza completo:
- Lectura línea a línea del fichero NOAA con separadores irregulares
- Adición de signo `+` explícito para anomalías positivas (que venían sin signo)
- Función `separar_valor()` para descomponer cada celda en SST y SSTA
- Función `extraer_year_week()` para parsear fechas `02SEP1981` a formato estándar
- Eliminación de años incompletos (1981, 2025)
- Tratamiento de la semana 53: reasignación al año siguiente para mantener 52 semanas exactas por curva

**3. Idea y objetivos**
La **unidad funcional es el año**: cada curva $x_i(t)$ describe la evolución de temperatura en 52 semanas. Esto proporciona $N > 40$ individuos funcionales (frente a $N = 4$ si se tomaran las regiones). Objetivos: caracterización univariante por región, comparación este-oeste, análisis sobre anomalías, detección de outliers funcionales.

**4. Análisis estadístico funcional — Representación cruda y suavizado**

*Representación cruda:* Se visualizan las curvas anuales en bruto para cada región y variable. Hallazgos principales:
- NINO 1+2: ciclo estacional pronunciado (20–28°C), mayor dispersión en anomalías
- NINO 3: "Barrera de Predictibilidad de Primavera" (colapso de varianza en semanas 15–20)
- NINO 4: curvas casi planas (27–30°C), mínima variabilidad estacional

*Suavizado funcional:* Aproximación $x(t) = \sum_{k=1}^K c_k \phi_k(t)$ mediante bases de Fourier con penalización en segunda derivada. Selección conjunta de número de bases $K \in \{13, 15, 17, 19, 21\}$ y parámetro $\lambda \in [10^{-10}, 10^{10}]$ mediante minimización del **GCV** (Validación Cruzada Generalizada).

**5. Temperaturas (SST) — Análisis funcional completo por región**

Para cada una de las 4 regiones:
- Búsqueda en rejilla del par $(K^*, \lambda^*)$ óptimo por GCV
- Ajuste de objetos `fd` con `smooth.basis()`
- **Media funcional** y **desviación típica funcional** — bandas de variabilidad
- **FPCA** (Análisis de Componentes Principales Funcional): extracción de modos de variación dominantes y sus scores para cada año
- **Detección de outliers funcionales** con MS-Plot (Magnitude-Shape Plot): distinción entre outliers por *magnitud* (años muy cálidos/fríos como 1983, 1997–98) y outliers por *forma* (años con evoluciones temporales atípicas como 2017)
- Mapa de scores PC1 vs PC2 para ubicar cada año en el espacio de variación

**6. Anomalías (SSTA) — Replicación del análisis**

Mismo pipeline aplicado sobre anomalías para aislar la señal climática pura (eliminando la estacionalidad). Permite caracterizar la magnitud y dinámica real de eventos El Niño/La Niña más allá de sus promedios.

### Tecnologías

- **R:** `fda`, `dplyr`, `tidyr`, `ggplot2`
- **Quarto** para renderizado de informe HTML
- Datos NOAA descargables directamente desde URL pública: `https://www.cpc.ncep.noaa.gov/data/indices/wksst9120.for`

---

## ▶️ Cómo ejecutar

### Parte 1 (Cópulas)
```r
# Instalar dependencias
install.packages(c("VineCopula", "copula", "fitdistrplus", "ghyp",
                   "fGarch", "httr", "jsonlite", "ggplot2", "MASS"))

# Renderizar con Quarto (desde terminal)
quarto render proy_mdmf_v3.qmd
```

> Se requiere una API key válida de Alpha Vantage. Sustituir el valor de `api_key` en el primer chunk por la propia clave (registro gratuito en [alphavantage.co](https://www.alphavantage.co)).

### Parte 2 (Datos Funcionales)
```r
# Instalar dependencias
install.packages(c("fda", "dplyr", "tidyr", "ggplot2"))

# Renderizar con Quarto (desde terminal)
quarto render analisis_datos_funcionales_v2.qmd
```

> Los datos NOAA se descargan automáticamente desde la URL pública al ejecutar. Alternativamente se puede usar el archivo local `noa_data.txt` (ver opción comentada en el código).

---

## 👥 Autores

Javier García Fernández · Martín Solano Martínez · Miguel Ángel Véliz Ayala  
Grupo — Modelización de Datos Multidimensionales y Funcionales, curso 2024/2025  
Universidad de Murcia
