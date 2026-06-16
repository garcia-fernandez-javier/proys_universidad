# Proyecto: Aplicación de Procesamiento del Lenguaje Natural sobre Reddit

Proyecto académico grupal que implementa una pipeline completa de **Procesamiento del Lenguaje Natural (PLN)** sobre un corpus de comentarios extraídos de Reddit. El sistema abarca desde la recolección y curación del corpus hasta tareas avanzadas como clasificación de texto, búsqueda de similitud, análisis de subjetividad, resumen automático y detección de contenido inapropiado.

---

## 📂 Contenido del repositorio

| Archivo | Descripción |
|--------|-------------|
| `1_Compilacion_del_corpus_y_uso_de_procesamiento_léxico.ipynb` | Extracción del corpus desde Reddit y preprocesamiento léxico |
| `2_Clasificador_de_comentarios_en_subreddits.ipynb` | Clasificador multiclase de comentarios por subreddit |
| `3_Busqueda_de_hilos_similares.ipynb` | Búsqueda de hilos temáticamente similares mediante embeddings |
| `4_Análisis_de_subjetividad.ipynb` | Análisis de sentimientos y emociones en comentarios |
| `5_Resumen_automático_abstractivo.ipynb` | Generación automática de resúmenes abstractivos por hilo |
| `6_Detección_de_contenido_inapropiado.ipynb` | Detección de contenido inapropiado con ZSL, FSL y Chain-of-Thought |
| `data/` | Carpeta con los 7 archivos JSON del corpus (uno por subreddit) |

---

## 📊 Corpus

El corpus está compuesto por comentarios reales extraídos de **7 subreddits deportivos** mediante la API de Reddit (librería `praw`):

| Subreddit | Temática |
|-----------|----------|
| `r/sports` | Deportes en general |
| `r/soccer` | Fútbol |
| `r/nba` | Baloncesto (NBA) |
| `r/formula1` | Automovilismo (Fórmula 1) |
| `r/hockey` | Hockey sobre hielo |
| `r/cricket` | Cricket |
| `r/nfl` | Fútbol americano (NFL) |

El corpus consta de aproximadamente **7400 comentarios** organizados en hilos. Cada archivo JSON sigue la estructura:

```json
[
  {
    "flair": "Stats",
    "title": "Título del hilo",
    "author": "usuario",
    "date": 1746365840.0,
    "score": 118,
    "description": "",
    "comments": [
      {
        "user": "usuario",
        "comment": "texto del comentario",
        "score": 8,
        "date": 1746371333.0
      }
    ]
  }
]
```

---

## 🔐 Configuración de credenciales

Este proyecto utiliza la **API de Reddit** (mediante `praw`) y en algunos notebooks la **API de Hugging Face**. Las credenciales **no deben escribirse directamente en el código**.

Usa los **Secretos de Google Colab** (icono 🔑 en el panel izquierdo) y accede a ellos así:

```python
from google.colab import userdata

reddit = praw.Reddit(
    client_id=userdata.get('REDDIT_CLIENT_ID'),
    client_secret=userdata.get('REDDIT_CLIENT_SECRET'),
    user_agent="nombre-de-tu-app"
)
```

Para Hugging Face:
```python
from huggingface_hub import login
login(token=userdata.get('HF_TOKEN'))
```

Debes añadir las siguientes variables como secretos en tu entorno de Colab antes de ejecutar los notebooks:

- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`
- `HF_TOKEN` *(solo necesario para modelos restringidos como Gemma)*

---

## 📓 Descripción de los notebooks

### 1. Compilación del corpus y preprocesamiento léxico

Conecta con la API de Reddit mediante `praw` y extrae hilos y comentarios de los 7 subreddits seleccionados durante un rango temporal de una semana. Implementa un pipeline de curación que filtra comentarios demasiado cortos, con exceso de emojis o formados únicamente por URLs, y aplica corrección ortográfica automática con **Hunspell**. El resultado se almacena en archivos JSON individuales por subreddit.

### 2. Clasificador de comentarios en subreddits

Entrena y evalúa modelos de clasificación multiclase para identificar a qué subreddit pertenece un comentario. Compara tres familias de representaciones de texto:

- **Técnicas tradicionales** — Bag of Words, TF-IDF, BM25, n-gramas de palabras y de caracteres — combinadas con clasificadores como LinearSVC, Random Forest, Decision Tree y SVM.
- **Word Embeddings** — GloVe, FastText, Word2Vec y Doc2Vec — con los mismos clasificadores.
- **Fine-tuning de Transformers** — BERT (`bert-base-uncased`) ajustado sobre el corpus con la librería Hugging Face `Trainer`.

Algunos notebooks de esta sección generan salidas como matrices de confusión, classification reports y gráficas comparativas de accuracy.

### 3. Búsqueda de hilos similares

Representa cada hilo como un vector denso a partir del contenido de sus comentarios y calcula similitudes entre hilos de distintos subreddits mediante **cosine similarity**. Compara tres modelos de embeddings:

- **fastText** (`cc.en.300.bin`)
- **all-MiniLM-L6-v2** (Sentence Transformers)
- **all-mpnet-base-v2** (Sentence Transformers)

Genera visualizaciones 2D del espacio de embeddings mediante **t-SNE** e identifica hilos potencialmente fuera de lugar (outliers) cuya temática no encaja con la de su subreddit. Evalúa la concordancia entre modelos mediante el **índice de Jaccard**.

### 4. Análisis de subjetividad

Aplica dos modelos de clasificación de texto preentrenados sobre todos los comentarios del corpus:

- **Análisis de sentimientos** con `cardiffnlp/twitter-roberta-base-sentiment` (negativo / neutro / positivo).
- **Análisis de emociones** con `michellejieli/emotion_text_classifier` (anger, disgust, fear, joy, neutral, sadness, surprise).

Presenta la distribución de sentimientos y emociones por subreddit y analiza diferencias entre comunidades deportivas. Genera salidas de estadísticas y guarda los resultados enriquecidos en nuevos archivos JSON.

### 5. Resumen automático abstractivo

Genera resúmenes automáticos de cada hilo combinando el título, la descripción y los comentarios. Compara dos estrategias:

- **mT5** (`csebuetnlp/mT5_multilingual_XLSum`) — modelo encoder-decoder especializado en resumen multilingüe.
- **Gemma 2B** — Small Language Model usado en modo offline con estrategia **Zero-shot prompting**.

Incluye un módulo de evaluación cualitativa manual sobre 10 hilos de muestra, con herramientas de visualización estadística (gráficos comparativos, dispersión, prueba t pareada y correlación de Pearson). Nota: por limitaciones de GPU en Colab, la carga de los JSON se procesa un subreddit a la vez (las rutas están comentadas en la función `load_json_files`).

### 6. Detección de contenido inapropiado

Extrae comentarios del subreddit `r/OpinionesPolemicas` (10 hilos × 50 comentarios) y aplica tres estrategias de prompting sobre un SLM (`TinyLlama/TinyLlama-1.1B-Chat-v1.0`) para clasificar cada comentario como apropiado o inapropiado:

- **Zero-Shot Learning (ZSL)** — sin ejemplos, solo instrucción directa.
- **Few-Shot Learning (FSL)** — con ejemplos etiquetados de ambas categorías.
- **Chain-of-Thought (CoT)** — razonamiento paso a paso siguiendo criterios explícitos (lenguaje ofensivo, discriminación, amenazas, contenido sexual).

Genera métricas de rendimiento por técnica (precisión global, precisión sobre apropiados e inapropiados, F1-score, matrices de confusión) y un informe en Markdown con ejemplos seleccionados.

---

## 🧰 Dependencias principales

```
praw
emoji
hunspell
scikit-learn
gensim
fasttext
sentence-transformers
transformers
datasets
torch
evaluate
nltk
matplotlib
seaborn
pandas
numpy
tqdm
scipy
```

---

## 👥 Autores

Javier García Fernández · Miguel Ángel Véliz Ayala  
Grado en Ciencia e Ingeniería de Datos  
Facultad de Informática, Universidad de Murcia · Universidad Politécnica de Cartagena  
Curso: 2024/2025 — Procesamiento del Lenguaje Natural

---

## 🛡️ Licencia

Contenido disponible solo para revisión académica o profesional.  
No se autoriza la reproducción o reutilización del material sin consentimiento previo.
