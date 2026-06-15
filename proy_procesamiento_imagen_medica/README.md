# Proyecto: Clasificación Automática de Retinopatía Diabética

Proyecto académico grupal que construye un **pipeline completo de gradación automática de retinopatía diabética** en cinco grados de severidad clínica (G0–G4), partiendo de un baseline sólido y mejorándolo de forma iterativa mediante diez experimentos. El trabajo cubre preprocesamiento específico para imagen retiniana, aprendizaje profundo con MONAI, radiómica cuantitativa, fusión multimodal e interpretabilidad con Grad-CAM.

---

## 📂 Contenido del repositorio

| Archivo | Descripción |
|--------|-------------|
| `PIM_memoria.pdf` | Memoria técnica completa: introducción, estado del arte, metodología, resultados y conclusiones |
| `presentacion_PIM.pdf` | Presentación de diapositivas de la defensa (14 slides) |
| `retinopatia-diabetica-completo.ipynb` | Notebook principal con sistema de caché de checkpoints para reanudación rápida |
| `retinopatia-diabetica-completo-sincache.ipynb` | Versión limpia del notebook sin caché, para ejecución completa desde cero |

---

## 🩺 Problema clínico

La **retinopatía diabética** (RD) es una complicación microvascular de la diabetes mellitus y una de las principales causas de ceguera prevenible en el mundo. Con más de 540 millones de adultos diabéticos y una prevalencia de afectación retiniana del ~35 %, el cribado masivo mediante retinografías de fondo de ojo es una necesidad clínica urgente que no puede escalarse con revisión manual. El sistema se entrena sobre el problema de **gradación ordinal** en cinco estadios:

| Grado | Nombre | Características clínicas |
|-------|--------|--------------------------|
| G0 | Sin RD | Fondo de ojo normal, sin lesiones visibles |
| G1 | Leve | Microaneurismas aislados (15–100 µm, ≤3 px a 224 px) |
| G2 | Moderada | Hemorragias, exudados duros y anomalías vasculares |
| G3 | Severa | Múltiples hemorragias, venous beading e IRMA en cuatro cuadrantes |
| G4 | Proliferativa | Neovascularización con riesgo de hemorragia vítrea y desprendimiento de retina |

---

## 📊 Datasets

### APTOS 2019 (fuente principal)
- **Fuente:** [Kaggle APTOS 2019 Blindness Detection](https://www.kaggle.com/c/aptos2019-blindness-detection) — licencia CC BY 4.0
- **Total:** 3 662 retinografías capturadas en clínicas rurales de la India, con alta variabilidad de iluminación y resolución

| Split | G0 | G1 | G2 | G3 | G4 | Total |
|-------|----|----|----|----|-----|-------|
| Train | 1 434 | 300 | 808 | 154 | 234 | 2 930 |
| Val | 172 | 40 | 104 | 22 | 28 | 366 |
| Test | 199 | 30 | 87 | 17 | 33 | 366 |
| % global | 49.3 % | 10.1 % | 27.3 % | 5.3 % | 8.1 % | 100 % |

> El severo desbalance (G0 representa el ~49 % frente al ~5 % de G3) es uno de los principales desafíos técnicos del proyecto.

### APTOS 2015 (preentrenamiento — Exp. J)
- **35 126 retinografías** con las mismas 5 etiquetas, incluyendo ~873 imágenes de G3
- Usado exclusivamente para preentrenamiento antes del fine-tuning en APTOS 2019, debido al domain shift entre ambos datasets
- Dataset: `resized-2015-2019-diabetic-retinopathy-detection` (autor: c7934597, Kaggle)

---

## 🔬 Metodología

### Pipeline de preprocesamiento común
Aplicado a todas las imágenes antes del entrenamiento:

1. **Máscara circular** — detección del bounding box en el canal verde y enmascarado para eliminar bordes negros no informativos (fuente de shortcuts)
2. **CLAHE** — aplicado sobre el canal L (espacio LAB) con `clipLimit=2.0` y tiles 8×8 para mejorar contraste local de microaneurismas sin amplificar ruido
3. **Resize** — a 224 px (baseline y Exp. A–E) o 384 px (Exp. F en adelante) mediante interpolación `INTER_AREA`
4. **Normalización ImageNet** — media y desviación típica estándar para compatibilidad con pesos preentrenados

> El Experimento G sustituye CLAHE por la normalización de Ben Graham.

### Data augmentation (conservadora)
Solo transformaciones que preservan la semántica clínica retiniana:
- ✅ Flip horizontal (p=0.5), rotación ±20°, zoom 0.9–1.1, ruido gaussiano (σ=0.03), ajuste de contraste (γ ∈ [0.8, 1.2])
- ❌ Flip vertical (anatomía imposible), rotación >30°, padding con ceros (crea shortcuts)

### Métricas de evaluación
- **κ² (kappa cuadrático ponderado):** métrica principal, estándar en APTOS 2019. Penaliza los errores proporcionalmente al cuadrado de la distancia ordinal entre grados, alineándose con la relevancia clínica. Valores >0.85 se consideran nivel profesional.
- **F1-score macro:** complementa al kappa detectando fallos en clases minoritarias (G1, G3)

### Baseline
EfficientNet-B3 (MONAI, preentrenado en ImageNet) con entrada 224×224 px, cabeza lineal de 5 neuronas + softmax, Weighted CrossEntropy (pesos inversamente proporcionales a la frecuencia de clase), optimizador Adam (lr=1e-4), 20 épocas, selección del mejor checkpoint por κ² sobre validación.

**Resultado baseline: κ² = 0.862 · F1 = 0.602**

---

## 🧪 Experimentos (A–J)

Cada experimento ataca una limitación concreta identificada de forma iterativa:

| Exp. | Problema atacado | Técnica | κ² | F1 |
|------|-----------------|---------|----|----|
| **J** | Escasez de datos de G3 | Pretrain en APTOS 2015 (35k imgs) → Fine-tune en 2019 (lr=2×10⁻⁵) | **0.885** | 0.551 |
| **G** | Shortcut learning (artefactos de iluminación) | Filtro Ben Graham (paso alto) + máscara dura a nivel de tensor + aug. solo fotométricas | 0.882 | 0.575 |
| **A** | Desbalance de clases | Sobremuestreo con `WeightedRandomSampler` hasta ≥12 % por clase | 0.880 | 0.631 |
| **F** | Resolución insuficiente + función de pérdida desalineada | 384 px + MSELoss (1 neurona) + umbrales Nelder-Mead | 0.872 | 0.507 |
| Baseline | — | EfficientNet-B3 + Weighted CE (224 px) | 0.862 | 0.602 |
| **D** | Confusión G0 vs G1 | Pipeline jerárquico 2 etapas: binario G0/RD+ → severidad G1–G4 | 0.860 | **0.631** |
| **E** | Confusión entre grados intermedios | Árbol jerárquico 3 niveles: ¿RD? → ¿Mild/Severe? → Grado final | 0.855 | 0.602 |
| **I** | CNN y radiómica como señales complementarias | Fusión 1536 deep features (Exp. G) + 107 radiómicas → LightGBM | 0.855 | **0.631** |
| **B** | Interpretabilidad sin deep learning | 107 features PyRadiomics (GLCM, GLRLM, GLSZM) + Regresión Logística L1 | 0.722 | 0.479 |
| **C** | ¿Es necesario el ajuste fino? | BiomedCLIP zero-shot: prompts simples (κ²=0.711) / clínicos (κ²=0.515) | 0.711 | 0.354 |

### Hallazgos destacados

**Exp. D — Mejor F1 macro y +16 % en G4 (la clase más crítica).** Al separar el screening (G0 vs RD+) de la gradación (G1–G4), el F1 de G4 Proliferativa sube de 0.51 a 0.59.

**Exp. F — G4 infradiagnosticada por MSELoss + desbalance.** De 33 imágenes de G4 en test, el modelo solo detecta 3 (recall=9.1 %). La pérdida MSE con desbalance provoca compresión hacia el centro, infradiagnosticando la clase más peligrosa.

**Exp. G — Hallazgo clave: métrica alta ≠ modelo fiable.** El filtro de Graham sube κ² (+0.01 respecto a F) pero empeora los mapas Grad-CAM: las activaciones se dispersan hacia la periferia del disco en lugar de concentrarse sobre las lesiones. Demuestra empíricamente que la auditoría de interpretabilidad es tan necesaria como la evaluación cuantitativa.

**Exp. I — El 96.5 % del peso proviene del CNN.** En la fusión multimodal con LightGBM, las 107 features radiómicas representan solo el 3.5 % de la importancia, pero mejoran el F1 en las clases difíciles (G1, G3) donde el CNN duda más.

**Exp. J — Mejor κ² del proyecto (0.885).** Desde la primera época de fine-tuning el modelo ya alcanza κ²=0.883: ha aprendido la anatomía retiniana con las 35k imágenes de 2015 y solo ajusta los detalles específicos de 2019. El recall de G4 sube del 9.1 % al 27.3 %.

---

## 🧠 Interpretabilidad: Grad-CAM

Se utiliza `pytorch-grad-cam` sobre la última capa convolucional del backbone para validar que las activaciones caen sobre estructuras retinianas reales (vasos, lesiones) y no sobre artefactos de adquisición (bordes, iluminación uniforme). El análisis comparativo entre Exp. F (CLAHE) y Exp. G (Ben Graham) constituye el hallazgo más relevante del proyecto: el modelo con mejor kappa no es necesariamente el más interpretable ni el más fiable clínicamente.

---

## 🛠️ Tecnologías y librerías

| Categoría | Herramienta |
|-----------|-------------|
| Framework DL | PyTorch + MONAI |
| Backbone | EfficientNet-B3 (ImageNet preentrenado) |
| Radiómica | PyRadiomics (GLCM, GLRLM, GLSZM — 107 features) |
| Zero-shot | BiomedCLIP (`microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224`) via `open_clip` |
| Boosting | LightGBM |
| Clasificación lineal | Scikit-learn (Regresión Logística L1) |
| Interpretabilidad | pytorch-grad-cam |
| Optimización | Nelder-Mead (scipy) para umbrales ordinales |
| Preprocesamiento | OpenCV, Pillow |
| Entorno | Kaggle Notebooks (GPU) |

---

## ▶️ Reproducción

El notebook está diseñado para ejecutarse en **Kaggle**. El dataset principal se monta automáticamente desde:
```
/kaggle/input/datasets/c7934597/resized-2015-2019-diabetic-retinopathy-detection
```

Para activar el **Experimento J** (preentrenamiento con APTOS 2015):
1. En el notebook de Kaggle, clic en **"+ Add Input"** → pestaña "Datasets"
2. Buscar: `resized-2015-2019-diabetic-retinopathy-detection` (autor: c7934597)
3. Clic en "Add". La variable `USE_2015` detecta automáticamente su presencia y activa el experimento sin ningún cambio adicional en el código.

**Diferencia entre los dos notebooks:**
- `retinopatia-diabetica-completo.ipynb` — incluye lógica de caché de checkpoints (`.pth`). Si el checkpoint existe, lo carga y omite el entrenamiento. Recomendado para reanudar ejecuciones interrumpidas.
- `retinopatia-diabetica-completo-sincache.ipynb` — sin lógica de caché, con una celda adicional de tabla Markdown del split del dataset. Ejecuta todo el pipeline de entrenamiento desde cero.

---

## 📋 Conclusiones principales

1. **El desbalance necesita variedad, no volumen.** Replicar datos (Exp. A) apenas mejora G3; incorporar 35k imágenes reales de distribución distinta (Exp. J) sí funciona.
2. **Dividir el problema ayuda.** El pipeline jerárquico (Exp. D) logra el mejor F1 macro y la mayor mejora en G4, la clase clínicamente más crítica (+16 %).
3. **Métrica alta ≠ modelo fiable.** El Exp. G sube κ² pero empeora Grad-CAM respecto a F: la auditoría de interpretabilidad es imprescindible antes de cualquier despliegue clínico.
4. **El ajuste fino supervisado es irreemplazable.** Radiómica (B) y zero-shot (C) quedan 14–15 puntos por debajo del CNN, aunque B aporta una interpretabilidad feature→significado clínico que el CNN no puede ofrecer.

---

## 👥 Autores

Javier García Fernández · Miguel Ángel Véliz Ayala · Martín Solano Martínez  
Grado en Ciencia e Ingeniería de Datos  
Asignatura: Procesamiento de Imagen en Medicina — Curso 2025/2026  
Fecha de entrega: 24 de abril de 2026

---

## 🛡️ Licencia

Contenido disponible únicamente con fines demostrativos y académicos.  
No se autoriza su reproducción o reutilización sin consentimiento previo de los autores.  
Dataset APTOS 2019: licencia CC BY 4.0.
