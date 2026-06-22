### SELECCIÓN DEL CONJUNTO DE DATOS

import os
import pandas as pd

# Descarga de los archivos desde Kaggle
import kagglehub

# Establecemos un directorio de caché concreto
os.environ["KAGGLEHUB_CACHE"] = "datos"

# Descargamos la versión más reciente del conjunto de datos
path = kagglehub.dataset_download("ramjasmaurya/top-1000-social-media-channels")

print("Path to dataset files:", path)

# Carga de datos en dataframes: df_ig, df_tt, df_yt

instagram = 'social media influencers-INSTAGRAM - -DEC 2022.csv'
tiktok = 'social media influencers-TIKTOK - ---DEC 2022.csv'
youtube = 'social media influencers-YOUTUBE - --DEC 2022.csv'

df_ig = pd.read_csv(os.path.join(path, instagram))
df_tt = pd.read_csv(os.path.join(path, tiktok))
df_yt = pd.read_csv(os.path.join(path, youtube))

print(df_ig.head())

print(df_tt.head())

print(df_yt.head())


### PREPROCESAMIENTO DE DATOS

# Limpieza de Datos
# Eliminamos posibles duplicados

df_ig = df_ig.drop_duplicates()
df_tt = df_tt.drop_duplicates()
df_yt = df_yt.drop_duplicates()


# INSTAGRAM
print(df_ig.info())

# Variables que tenemos que pasar a numéricas (float): followers, Eng.(Auth.) y Eng (Avg.)

columns_to_convert = ['followers', 'Eng. (Auth.)', 'Eng. (Avg.)']

for column in columns_to_convert:
  df_ig[column] = df_ig[column].apply(lambda x:
      float(x.replace('M', '')) * 1_000_000 if 'M' in x else
      float(x.replace('K', '')) * 1_000 if 'K' in x else
      float(x))

print(df_ig.info())

# Renombramos las columnas para que todos los dataset tengan nombres consistentes

df_ig = df_ig.rename(columns={
    'Rank': 'rank',
    'instagram name': 'username',
    'Category_1': 'category',
    'Category_2': 'category_2',
    'Eng. (Auth.)': 'engagement_auth',
    'Eng. (Avg.)': 'engagement_avg'
})
df_ig.head()

# Exploramos los datos categóricos

df_ig_cat = df_ig[["category", "category_2", "country"]]

# Mostramos los valores únicos de cada variables categórica

for col in df_ig_cat.columns:
    print(f"Valores únicos en '{col}':")
    print(df_ig_cat[col].unique())
    print("-" * 40)

# Observamos que las tres variables categóricas tiene valores nulos,
# esto tenemos que tenerlo en cuenta a la hora de visualizar los datos.


# TIK TOK
print(df_tt.info())

# Variables que tenemos que convertir: followers, views(avg), likes(avg.), comments(avg.), shares(avg.)

columns_to_convert = ['followers', 'views(avg)', 'likes(avg.)', 'comments(avg.)', 'shares(avg.)']

for column in columns_to_convert:
    df_tt[column] = df_tt[column].apply(lambda x:
      float(x.replace('M', '')) * 1_000_000 if 'M' in x else
      float(x.replace('K', '')) * 1_000 if 'K' in x else
      float(x))
    
print(df_tt.info())

# Renombramos las columnas

df_tt = df_tt.rename(columns={
    'Rank': 'rank',
    'Tiktoker name': 'username',
    'Tiktok name': 'name',
    'views(avg)': 'views',
    'likes(avg.)': 'likes',
    'comments(avg.)': 'comments',
    'shares(avg.)': 'shares'
})
df_tt.head()


# YOUTUBE
print(df_yt.info())

# Varibles a convertir: Followers,\nViews (Avg.),Likes (Avg.),Comments (Avg.)

columns_to_convert = ['Followers','\nViews (Avg.)', 'Likes (Avg.)', 'Comments (Avg.)']

for column in columns_to_convert:
    df_yt[column] = df_yt[column].apply(lambda x:
    float(x.replace('M', '')) * 1_000_000 if 'M' in x else
    float(x.replace('K', '')) * 1_000 if 'K' in x else
    float(x))

print(df_yt.info())

# Eliminamos la columna 's.no' que no aporta ninguna información, ya que es simplemente una columna que enumera las filas del dataset
df_yt = df_yt.drop(columns=["s.no"])

# Renombramos las columnas

df_yt = df_yt.rename(columns={'Youtube channel': 'name',
                              'youtuber name': 'username',
                              'Category': 'category',
                              'Country': 'country',
                              'Followers': 'followers',
                              '\nViews (Avg.)': 'views',
                              'Likes (Avg.)': 'likes',
                              'Comments (Avg.)': 'comments',
                              'Category-2': 'category_2'})
df_yt.head()

# Exploramos los datos categóricos

df_yt_cat = df_yt[["category", "category_2", "country"]]

# Mostramos los valores únicos de cada variables categórica

for col in df_yt_cat.columns:
    print(f"Valores únicos en '{col}':")
    print(df_yt_cat[col].unique())
    print("-" * 40)

# Observamos que las tres variables categóricas tiene valores nulos, 
# esto tenemos que tenerlo en cuenta a la hora de visualizar los datos.


# METRICAS ADICIONALES
# Calculamos una nueva variable, el Engagement Rate que es una métrica clave en redes sociales para medir qué tan activa o
# comprometida está la audiencia de un influencer o cuenta con su contenido.

df_ig['engagement_rate'] = (df_ig['engagement_avg'] / df_ig['followers']) * 100
df_tt['engagement_rate'] = ((df_tt['likes'] + df_tt['comments'] + df_tt['shares']) / df_tt['followers']) * 100
df_yt['engagement_rate'] = ((df_yt['likes'] + df_yt['comments']) / df_yt['followers']) * 100


# CONCATENACIONES FINALES
# Necesitamos ver todas las coincidencias entre los nombres ('name') de Instagram, TikTok y Youtube
df_ig_full = df_ig.copy()
df_tt_full = df_tt.copy()
df_yt_full = df_yt.copy()

# Poner toda la columna name a minuscula, quitar todos los espacios y guiones
df_ig_full['name'] = df_ig_full['name'].str.lower().str.replace(' ', '').str.replace('-', '')
df_tt_full['name'] = df_tt_full['name'].str.lower().str.replace(' ', '').str.replace('-', '')
df_yt_full['name'] = df_yt_full['name'].str.lower().str.replace(' ', '').str.replace('-', '')

# Añadir prefijo a todas las columnas excepto 'name'
df_ig_full = df_ig_full.rename(columns={col: f"ig_{col}" for col in df_ig.columns if col != 'name'})
df_tt_full = df_tt_full.rename(columns={col: f"tt_{col}" for col in df_tt.columns if col != 'name'})
df_yt_full = df_yt_full.rename(columns={col: f"yt_{col}" for col in df_yt.columns if col != 'name'})

# Concatenamos los dataframes

df_full = pd.merge(df_tt_full, df_ig_full, on='name')
df_full = pd.merge(df_full, df_yt_full, on='name')
df_full



### APLICACION DASH

# Importamos las librerías necesarias

import dash
from dash import dcc, html, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

import plotly.colors as pc # Para no repetir colores cuando mapeamos
# por color las categorías

# Inicializamos la aplicación Dash

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
                suppress_callback_exceptions=True)

"""
-> 'external_stylesheets' aplica una hoja de estilos externa prediseñados que ofrece Dash para facilitar el diseño visual sin
tener que escribir CSS desde cero.

-> 'supress_callback_exception' permiten registrar callbacks para componentes que no están presentes en el layout inicial de la aplicación,
lo cual es útil en aplicaciones con páginas dinámicas o layouts que cambian según la interacción del usuario.

"""

app.title = 'Dashboard de Influencers en Redes Sociales'   # Título que aparece en la pestaña del navegador

# Definir esquema de colores para las plataformas

colors = {
    'instagram': '#FFA500',   # naranja
    'tiktok': '#000080',      # azul marino
    'youtube': '#FF0000',     # rojo
    'full': '#CDA434' ,        # Dorado
    'background': '#E0F7FA',  # azul claro
    'text': '#000000'         # negro
}

##### Estructura del Dashboard: diseño de la aplicación #####

app.layout = html.Div(
    style={'backgroundColor': colors['background'], 'fontFamily': 'Roboto, sans-serif'},
    children=[

        # Encabezado
        html.Div([
            html.H1('Dashboard de Análisis de Influencers en Redes Sociales',
                    style={'textAlign': 'center', 'color': colors['text'], 'paddingTop': '20px'}),
            html.P('Explora y analiza datos de los principales influencers en Instagram, TikTok y Youtube',
                   style={'textAlign': 'center', 'fontSize': '18px', 'color': colors['text']}),
        ], style={'marginBottom': '30px'}),

        # Pestañas de selección de plataforma
        dcc.Tabs(id='platform-tabs',
                 value='instagram',
                 children=[
                    dcc.Tab(label='📷 Instagram', value='instagram', style={'backgroundColor': colors['instagram'], 'color': 'white'}),
                    dcc.Tab(label='🎵 TikTok', value='tiktok', style={'backgroundColor': colors['tiktok'], 'color': 'white'}),
                    dcc.Tab(label='▶️ YouTube', value='youtube', style={'backgroundColor': colors['youtube'], 'color': 'black'}),
                    dcc.Tab(label='🌟Más mediáticos', value='full', style={'backgroundColor': colors['full'], 'color': 'black'} ),
                  ], style={'marginBottom': '20px'}),

        # Contenido principal: se actualizará según la pestaña seleccionada
        html.Div(id='platform-content', style={'padding': '20px'}),

        # Pie de página
        html.Div([
            html.Hr(),
            html.P('Dashboard creado con Dash y Plotly | Datos de Kaggle: Top 1000 Social Media Channels',
                  style={'textAlign': 'center', 'fontSize': '14px', 'color': colors['text']}),
        ], style={'marginTop': '30px'})
    ]
)

##### Interactividad: Declaración de Callbacks #####

@callback(
    Output('platform-content', 'children'),
    Input('platform-tabs', 'value')
)


def update_platform_content(platform):
    if platform == 'instagram':
        return instagram_layout()
    elif platform == 'tiktok':
        return tiktok_layout()
    elif platform == 'youtube':
        return youtube_layout()
    elif platform == 'full':
        return full_layout()

##### Diseño de cada plataforma #####

### Instagram ###

def instagram_layout():
    # Lista de categorías disponibles para Instagram
    categories = ['All'] + sorted(df_ig['category'].dropna().unique().tolist())

    # Lista de países disponibles para Instagram
    countries = ['All'] + sorted(df_ig['country'].dropna().unique().tolist())

    return html.Div([
        ## Filtros ##
        html.Div([
            html.Div([
                html.Label('Seleccionar Categoría:'),
                dcc.Dropdown(
                    id='ig-category-dropdown',
                    options=[{'label': cat, 'value': cat} for cat in categories],
                    value='All',
                    clearable=False
                ),
            ], style={'width': '33%', 'display': 'inline-block', 'paddingRight': '10px'}),

            html.Div([
                html.Label('Seleccionar País:'),
                dcc.Dropdown(
                    id='ig-country-dropdown',
                    options=[{'label': country, 'value': country} for country in countries],
                    value='All',
                    clearable=False
                ),
            ], style={'width': '33%', 'display': 'inline-block', 'paddingRight': '10px'}),

            html.Div([
                html.Label('Número de Top Influencers más Relevantes:'),
                dcc.Slider(
                    id='ig-top-n-slider',
                    min=10,
                    max=100,
                    step=10,
                    value=30,
                    marks={i: str(i) for i in range(10, 101, 10)}
                ),
            ], style={'width': '33%', 'display': 'inline-block'}),
        ], style={'marginBottom': '20px'}),

        ## Resumen de métricas ##
        html.Div([
            html.Div([
                html.H3('Resumen de Influencers en Instagram', style={'textAlign': 'center'}),
                html.Div(id='ig-summary-metrics'),
            ], style={'marginBottom': '20px'})
        ]),

        ## Gráficos ##
        html.Div([
            html.Div([
                html.H3('Top influencers  más relevantes en Instagram', style={'textAlign': 'center'}),
                dcc.Graph(id='ig-top-followers-chart')
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
                html.H3('Tasa de Engagement vs Seguidores', style={'textAlign': 'center'}),
                dcc.Graph(id='ig-engagement-scatter')
            ], style={'width': '50%', 'display': 'inline-block'}),
        ]),

        html.Div([
            html.Div([
                html.H3('Distribución por categoría', style={'textAlign': 'center'}),
                dcc.Graph(id='ig-category-distribution')
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
                html.H3('Distribución geográfica', style={'textAlign': 'center'}),
                dcc.Graph(id='ig-geo-distribution')
            ], style={'width': '50%', 'display': 'inline-block'}),
        ]),

        html.Div([
    html.H3('Estudio de subcategorías', style={'textAlign': 'left'}),

    html.Div([
        html.Div([
            dcc.Graph(id='ig-barras-apiladas')
        ], style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        html.Div([
            html.Label('Selecciona una cuenta de Instagram:'),
            dcc.Dropdown(
                id='ig-account-dropdown',
                options=[{'label': name, 'value': name} for name in df_ig['name'].unique()],
                value=df_ig['name'].iloc[0],
                style={'width': '100%'}
            ),
            html.Br(),
            html.Div(id='account-details')
        ], style={
            'width': '38%',
            'display': 'inline-block',
            'paddingLeft': '20px',
            'verticalAlign': 'top'
        })
      ])
    ])
  ])

### TikTOk ###
def tiktok_layout():
    return html.Div([
        ## Filtros ##
        html.Div([
            html.Div([
                html.Label('Filtrar por Mínimo de Seguidores:'),
                dcc.Slider(
                    id='tt-followers-slider',
                    min=10000,
                    max=100000000,
                    step=1000000,
                    value=10000000,
                    marks={i: f'{i/1000000}M' for i in range(1000000, 101000000, 10000000)}
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
                html.Label('Número de Top Influencers:'),
                dcc.Slider(
                    id='tt-top-n-slider',
                    min=10,
                    max=100,
                    step=10,
                    value=30,
                    marks={i: str(i) for i in range(10, 101, 10)}
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
        ], style={'marginBottom': '20px'}),

        ## Resumen de métricas ##
        html.Div([
            html.Div([
                html.H3('Resumen TikTok', style={'textAlign': 'center'}),
                html.Div(id='tt-summary-metrics'),
            ], style={'marginBottom': '20px'})
        ]),

        ## Gráficos ##
        html.Div([
            html.Div([
                html.H3('Top influencers  más relevantes en Tik Tok', style={'textAlign': 'center'}),
                dcc.Graph(id='tt-top-rank-chart')
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
                html.H3('Análisis Views vs Likes', style={'textAlign': 'center'}),
                dcc.Graph(id='tt-views-likes-scatter')
            ], style={'width': '50%', 'display': 'inline-block'}),
        ]),

        html.Div([
            html.Div([
                html.H3('Análisis Followers Vs Engagement', style={'textAlign': 'center'}),
                dcc.Graph(id='tt-followers_engagement')
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
                html.H3('Análisis Compartidos vs Comentarios', style={'textAlign': 'center'}),
                dcc.Graph(id='tt-shares-comments-analysis')
            ], style={'width': '50%', 'display': 'inline-block'}),
        ]),

        html.Div([
          html.Div([
              html.Label('Selecciona un Canal de Tik Tok:'),
        dcc.Dropdown(
            id='tt-channel-dropdown',
            options=[{'label': name, 'value': name} for name in df_tt['name'].dropna().unique()],
            value=df_tt['name'].dropna().iloc[0],
            style={'width': '100%'}
        ),
        html.Br(),
        dcc.Graph(id='tt-radar-chart')
    ], style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    html.Div([
        html.H4('Estadísticas Cuenta TikTok', style={'textAlign': 'center'}),
        html.Div(id='tt-channel-details')
    ], style={
        'width': '38%',
        'display': 'inline-block',
        'paddingLeft': '20px',
        'verticalAlign': 'top'
    })
  ])
    ])


### Youtube ###

def youtube_layout():
    # Lista de categorías disponibles
    categories = ['All'] + sorted(df_yt['category'].dropna().unique().tolist())

    # Lista de países disponibles
    countries = ['All'] + sorted(df_yt['country'].dropna().unique().tolist())

    return html.Div([
               ## Filtros ##
        html.Div([
            html.Div([
                html.Label('Seleccionar Categoría:'),
                dcc.Dropdown(
                    id='yt-category-dropdown',
                    options=[{'label': cat, 'value': cat} for cat in categories],
                    value='All',
                    clearable=False
                ),
            ], style={'width': '33%', 'display': 'inline-block', 'paddingRight': '10px'}),

            html.Div([
                html.Label('Seleccionar País:'),
                dcc.Dropdown(
                    id='yt-country-dropdown',
                    options=[{'label': country, 'value': country} for country in countries],
                    value='All',
                    clearable=False
                ),
            ], style={'width': '33%', 'display': 'inline-block', 'paddingRight': '10px'}),

            html.Div([
                html.Label('Número de Top Influencers más Relevantes:'),
                dcc.Slider(
                    id='yt-top-n-slider',
                    min=10,
                    max=100,
                    step=10,
                    value=30,
                    marks={i: str(i) for i in range(10, 101, 10)}
                ),
            ], style={'width': '33%', 'display': 'inline-block'}),
        ], style={'marginBottom': '20px'}),

        ## Resumen de métricas ##
        html.Div([
            html.Div([
                html.H3('Resumen Canales Youtube', style={'textAlign': 'center'}),
                html.Div(id='yt-summary-metrics'),
            ], style={'marginBottom': '20px'})
        ]),

         ## Gráficos ##
        html.Div([
            html.Div([
                html.H3('Top Influencers con más seguidores en Youtube', style={'textAlign': 'center'}),
                dcc.Graph(id='yt-top-followers-chart')
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
                html.H3('Análisis Followers Vs Visitas', style={'textAlign': 'center'}),
                dcc.Graph(id='yt-followers-views-scatter')
            ], style={'width': '50%', 'display': 'inline-block'}),
        ]),

        html.Div([
            html.Div([
                html.H3('Distribución por categoría', style={'textAlign': 'center'}),
                dcc.Graph(id='yt-category-distribution')
            ], style={'width': '50%', 'display': 'inline-block'}),

            html.Div([
                html.H3('Distribución geográfica', style={'textAlign': 'center'}),
                dcc.Graph(id='yt-geo-distribution')
            ], style={'width': '50%', 'display': 'inline-block'}),
        ]),

 html.Div([
    html.H3('Análisis País Vs Categoría', style={'textAlign': 'left'}),

    html.Div([
        html.Div([
            dcc.Graph(id='yt-barras-apiladas')
        ], style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        html.Div([
            html.Label('Selecciona un canal de Youtube:'),
            dcc.Dropdown(
                id='yt-channel-dropdown',
                options=[{'label': name, 'value': name} for name in df_yt['name'].unique()],
                value=df_yt['name'].iloc[0],
                style={'width': '100%'}
            ),
            html.Br(),
            html.Div(id='yt-channel-details')
        ], style={
            'width': '38%',
            'display': 'inline-block',
            'paddingLeft': '20px',
            'verticalAlign': 'top'
        })
      ])
    ])
  ])

### Más mediáticos ###

def unified_engagement_chart():
    # Primero, identificamos los influencers que están presentes en las tres plataformas
    # Esto dependerá de cómo está estructurado tu df_full

    # Asumimos que un influencer está presente en una plataforma si su tasa de engagement no es NaN
    influencers_with_complete_data = df_full.dropna(subset=['ig_engagement_rate', 'tt_engagement_rate', 'yt_engagement_rate'])
    
    # Seleccionamos los top N influencers por la suma de sus tasas de engagement
    # Esto nos dará una lista de influencers relevantes en las tres plataformas
    top_n = 15  # Puedes ajustar este número
    
    # Calculamos una "puntuación total" para ordenar
    influencers_with_complete_data['total_score'] = (
        influencers_with_complete_data['ig_engagement_rate'] + 
        influencers_with_complete_data['tt_engagement_rate'] + 
        influencers_with_complete_data['yt_engagement_rate']
    )

    # Ordenamos y seleccionamos los top N
    top_influencers = influencers_with_complete_data.sort_values('total_score', ascending=False).head(top_n)
    
    # Preparamos los datos para el gráfico de barras agrupadas
    # Reorganizamos el dataframe para que sea adecuado para plotly

    # Creamos un dataframe en formato largo para facilitar la creación del gráfico
    data_long = pd.melt(
        top_influencers, 
        id_vars=['name'], 
        value_vars=['ig_engagement_rate', 'tt_engagement_rate', 'yt_engagement_rate'],
        var_name='platform', 
        value_name='engagement_rate'
    )

    # Renombramos las plataformas para mayor claridad
    platform_names = {
        'ig_engagement_rate': 'Instagram',
        'tt_engagement_rate': 'TikTok',
        'yt_engagement_rate': 'YouTube'
    }
    data_long['platform'] = data_long['platform'].map(platform_names)

    # Creamos el gráfico de barras agrupadas
    fig = px.bar(
        data_long,
        x='name',
        y='engagement_rate',
        color='platform',
        barmode='group',
        title='Comparativa de Engagement Rate por Plataforma',
        labels={'name': 'Influencer', 'engagement_rate': 'Engagement Rate', 'platform': 'Plataforma'},
        color_discrete_map={
            'Instagram': '#FFA500', 
            'TikTok': '#000080', 
            'YouTube': '#FF0000'
        }
    )

    # Mejoramos el diseño del gráfico
    fig.update_layout(
        xaxis_tickangle=-45,  # Rotamos las etiquetas del eje X para mejor legibilidad
        legend_title_text='Plataforma',
        yaxis_title='Engagement Rate',
        xaxis_title='',
        barmode='group',
        bargap=0.15,  # Ajusta el espacio entre grupos de barras
        bargroupgap=0.1  # Ajusta el espacio entre barras dentro de un grupo
    )
    
    return fig

# Incorporamos este gráfico en el layout
def full_layout():
    # Obtenemos el nuevo gráfico unificado
    fig_unified = unified_engagement_chart()
    
    return html.Div([
        html.H1("Creadores de Contenido Activos en todas las plataformas", style={'text-align': 'center', 'color': '#333'}),
        html.Div([
            dcc.Graph(figure=fig_unified)
        ], style={'margin-bottom': '30px'}),
        html.H2("Top Engagement Rate por Plataforma", style={'text-align': 'center', 'color': '#333'}),
        html.Div([
            dcc.Graph(figure=px.bar(
                df_full.sort_values('ig_engagement_rate', ascending=False).head(10),
                x='ig_engagement_rate',
                y='name',
                orientation='h',
                title='Instagram - Top 10 Engagement Rate',
                labels={'name': 'Usuario', 'ig_engagement_rate': 'Engagement Rate'},
                color_discrete_sequence=['#FFA500']
            ).update_layout(yaxis=dict(autorange="reversed")))
        ]),
        html.Div([
            dcc.Graph(figure=px.bar(
                df_full.sort_values('tt_engagement_rate', ascending=False).head(10),
                x='tt_engagement_rate',
                y='name',
                orientation='h',
                title='TikTok - Top 10 Engagement Rate',
                labels={'name': 'Usuario', 'tt_engagement_rate': 'Engagement Rate'},
                color_discrete_sequence=['#000080']
            ).update_layout(yaxis=dict(autorange="reversed")))
        ]),
        html.Div([
            dcc.Graph(figure=px.bar(
                df_full.sort_values('yt_engagement_rate', ascending=False).head(10),
                x='yt_engagement_rate',
                y='name',
                orientation='h',
                title='YouTube - Top 10 Engagement Rate',
                labels={'name': 'Usuario', 'yt_engagement_rate': 'Engagement Rate'},
                color_discrete_sequence=['#FF0000']
            ).update_layout(yaxis=dict(autorange="reversed")))
        ])
    ])



### Callbacks para Instagram ###
@callback(
    [Output('ig-summary-metrics', 'children'),
     Output('ig-top-followers-chart', 'figure'),
     Output('ig-engagement-scatter', 'figure'),
     Output('ig-category-distribution', 'figure'),
     Output('ig-geo-distribution', 'figure'),
     Output('ig-barras-apiladas', 'figure'),
     Output('account-details', 'children')],
    [Input('ig-category-dropdown', 'value'),
     Input('ig-country-dropdown', 'value'),
     Input('ig-top-n-slider', 'value'),
     Input('ig-account-dropdown', 'value')],
    prevent_initial_call='initial_duplicate'
)


def update_ig_charts(category, country, top_n, name):
    # Filtrar datos según las selecciones
    filtered_df = df_ig.copy()

    if category != 'All':
        filtered_df = filtered_df[filtered_df['category'] == category]

    if country != 'All':
        filtered_df = filtered_df[filtered_df['country'] == country]

    # Gráfico de top influencers relevantes
    top_rank_df = filtered_df.sort_values('rank', ascending=False).head(top_n)

    followers_fig = px.bar(
    top_rank_df,
    y='name',
    x='followers',
    color='engagement_rate',
    custom_data=['username', 'category', 'country'],
    labels={
        'name': 'Nombre del Influencer',
        'followers': 'Cantidad de Seguidores',
        'engagement_rate': 'Tasa de Engagement'
    },
    color_continuous_scale=px.colors.sequential.Purples,
    title=f'Top {top_n} Influencers en Instagram más relevantes'
    )

    # Editamos el texto que aparece al pasar el ratón
    followers_fig.update_traces(
    hovertemplate=
    '<b>%{y}</b><br>' +
    'Seguidores: %{x}<br>' +
    'Tasa de Engagement: %{marker.color:.2f}%<br>' +
    'Usuario Instagram: %{customdata[0]}<br>' +
    'Categoría: %{customdata[1]}<br>' +
    'País: %{customdata[2]}<extra></extra>'
    )


    # Gráfico de dispersión de engagement
    engagement_fig = px.scatter(
        filtered_df,
        x='followers',
        y='engagement_rate',
        size='followers',
        color='category',
        hover_name='name',
        labels={
        'category': 'Categoría',
        'followers': 'Cantidad de Seguidores',
        'engagement_rate': 'Tasa de Engagement'},
        log_x=True,
        size_max=60,
        title='Tasa de Engagement vs. Seguidores (escala logarítmica)'
    )
    engagement_fig.update_xaxes(title_text='Seguidores (escala log)')
    engagement_fig.update_yaxes(title_text='Tasa de Engagement (%)')

    # Distribución por categoría
    category_counts = filtered_df['category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']
    category_fig = px.pie(
        category_counts,
        values='Count',
        names='Category',
        title='Distribución por Categoría',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    category_fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        insidetextorientation='radial',
        textfont_size=12,
        marker=dict(line=dict(color='#FFFFFF', width=1)))

    # En la parte donde creamos el category_fig (dentro de update_ig_charts), modificamos el update_layout así:
    category_fig.update_layout(
        margin=dict(l=50, r=250, t=40, b=20),  # Ajustamos márgenes: izquierdo más pequeño, derecho más grande
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",  # Cambiamos a "left" para que la leyenda se ancle a la izquierda
            x=1.05,         # Posición horizontal (1.05 la coloca justo a la derecha del gráfico)
            font=dict(size=12),
            bgcolor='rgba(255,255,255,0.5)'  # Fondo semitransparente para mejor legibilidad
        ),
        height=500,
        width=800,
        autosize=False,
        showlegend=True
    )


    # Distribución geográfica
    geo_counts = filtered_df['country'].value_counts().reset_index()
    geo_counts.columns = ['Country', 'Count']
    geo_fig = px.choropleth(
        geo_counts,
        locations='Country',
        locationmode='country names',
        color='Count',
        color_continuous_scale=px.colors.sequential.Purples,
        title='Distribución Geográfica',
        labels={'Count': 'Número de Influencers'}
    )

    # Ajustamos el tamaño y formato del gráfico geográfico
    geo_fig.update_layout(
      height=500,
      width=800,
      autosize=False,
      showlegend=True
    )

    # Gráfico de barras apiladas para las categorias
    # Agrupamos por categorías
    counts = filtered_df.groupby(['category', 'category_2']).size().reset_index(name='count')

    # Obtenemos todas las subcategorías únicas
    unique_subcategories = filtered_df['category_2'].unique()

    # Como existen muchas categorías, vamos a crear un mapeo de colores personalizado
    colors = pc.qualitative.Plotly + pc.qualitative.D3 + pc.qualitative.G10 + pc.qualitative.T10

    # Nos aseguraremos primero de que tenemos suficientes colores
    if len(unique_subcategories) > len(colors):
        # Creamos más colores usando una escala de colores continua
        more_colors = px.colors.sample_colorscale(
            px.colors.sequential.Viridis,
            [i/(len(unique_subcategories) - len(colors)) for i in range(len(unique_subcategories) - len(colors))]
        )
        colors.extend(more_colors)

    # Creamos ahora un diccionario que asigne a cada subcategoría un color específico
    color_map = {subcat: colors[i % len(colors)] for i, subcat in enumerate(unique_subcategories)}

    # Finalmente creamos el gráfico de barras apiladas usando la paleta
    fig_barras_apiladas = px.bar(counts,
                                 x='count',
                                 y='category',
                                 color='category_2',
                                 barmode='stack',
                                 color_discrete_map=color_map)


    # Calcular métricas resumen
    total_influencers = len(filtered_df)
    avg_followers = filtered_df['followers'].mean() if not filtered_df.empty else 0
    avg_engagement = filtered_df['engagement_rate'].mean() if not filtered_df.empty else 0
    max_followers = filtered_df['followers'].max() if not filtered_df.empty else 0
    top_influencer = filtered_df.loc[filtered_df['followers'].idxmax()]['name'] if not filtered_df.empty else 'N/A'

    summary_metrics = html.Div([
        html.Div([
            html.Div([
                html.H4(f"{total_influencers:,}"),
                html.P("Total de Influencers")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),

            html.Div([
                html.H4(f"{avg_followers/1_000_000:.2f}M"),
                html.P("Prom. Seguidores")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),

            html.Div([
                html.H4(f"{avg_engagement:.2f}%"),
                html.P("Prom. Tasa Engagement")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),

            html.Div([
                html.H4(f"{max_followers/1_000_000:.2f}M"),
                html.P("Máx. Seguidores")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),

            html.Div([
                html.H4(top_influencer),
                html.P("Top Influencer")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'})
        ])
    ])

    # Extraemos las características del instagramer

    influencer_row = df_ig[df_ig['name'] == name].iloc[0]

    stats = html.Ul([
        html.Li(f"Canal: {influencer_row['name']}"),
        html.Li(f"Nombre: {influencer_row['username']}"),
        html.Li(f"Categoría: {influencer_row['category']}"),
        html.Li(f"Seguidores: {influencer_row['followers']:,}"),
        html.Li(f"País: {influencer_row['country']}"),
        html.Li(f"Engagement Rate: {influencer_row['engagement_rate'] * 100:.2f}%"),
        html.Li(f"Categoría: {influencer_row['category']}"),
        html.Li(f"Rank: {influencer_row['rank']}")
    ])

    return summary_metrics, followers_fig, engagement_fig, category_fig, geo_fig, fig_barras_apiladas, stats

# Callbacks para TikTok
@callback(
    [Output('tt-top-rank-chart', 'figure'),
     Output('tt-views-likes-scatter', 'figure'),
     Output('tt-followers_engagement', 'figure'),
     Output('tt-shares-comments-analysis', 'figure'),
     Output('tt-summary-metrics', 'children'),
     Output('tt-radar-chart', 'figure'),
     Output('tt-channel-details', 'children')],
    [Input('tt-followers-slider', 'value'),
     Input('tt-top-n-slider', 'value'),
     Input('tt-channel-dropdown', 'value')],
    prevent_initial_call='initial_duplicate'
)

def update_tt_charts(min_followers, top_n, name):
    # Filtrar datos según las selecciones
    filtered_df = df_tt[df_tt['followers'] >= min_followers]

    # Gráfico de top seguidores con barras horizontales
    top_followers_df = filtered_df.sort_values('rank', ascending=False).head(top_n)
    followers_fig = px.bar(
    top_followers_df,
    y='name',
    x='followers',
    color='engagement_rate',
    hover_data=['username', 'views'],
    labels={'name': 'Nombre del TikToker', 'followers': 'Cantidad de Seguidores'},
    color_continuous_scale=px.colors.sequential.Turbo,
    title=f'Top {top_n} Influencers en TikTok por Relevancia'
    )

    # Gráfico de dispersión views vs likes
    views_likes_fig = px.scatter(
        filtered_df,
        x='views',
        y='likes',
        color='engagement_rate',
        size='followers',
        hover_name='name',
        log_x=True,
        log_y=True,
        size_max=50,
        opacity=0.7,
        title='Correlación entre Visualizaciones y Likes (escala log)',
        color_continuous_scale=px.colors.sequential.Reds
    )
    views_likes_fig.update_xaxes(title_text='Visualizaciones Promedio (escala log)')
    views_likes_fig.update_yaxes(title_text='Likes Promedio (escala log)')

    # Análisis 'Followers' Vs 'Engagement' Vs Likes'
    followers_engagement_fig = px.scatter(
      filtered_df,
      x='followers',
      y='engagement_rate',
      color='likes',  # color de los puntos en base a los likes
      hover_data=['name', 'views', 'likes'],
      labels={'followers': 'Cantidad de Seguidores', 'engagement_rate': 'Tasa de Engagement (%)', 'likes': 'Promedio de Likes'},
      color_continuous_scale=px.colors.sequential.Viridis,
      title='Comparación entre Seguidores, Tasa de Engagement y Promedio de Likes'
    )

    followers_engagement_fig.update_layout(
      xaxis_title='Cantidad de Seguidores',
      yaxis_title='Tasa de Engagement (%)',
      xaxis=dict(type='log'),  # Usar escala logarítmica para los seguidores
      legend_title="Promedio de Likes",  # Añadir un título a la leyenda para explicar el tamaño
      title='Comparación entre Seguidores, Tasa de Engagement y Promedio de Likes'
  )
    followers_engagement_fig.update_traces(marker=dict(size=12))  # Tamaño de los puntos del gráfico

    # Análisis de compartidos vs comentarios
    shares_comments_fig = px.scatter(
        filtered_df,
        x='comments',
        y='shares',
        size='followers',
        color='likes',
        hover_name='name',
        log_x=True,
        log_y=True,
        size_max=50,
        opacity=0.7,
        title='Análisis de Comentarios vs. Compartidos (escala log)',
        color_continuous_scale=px.colors.sequential.Plasma
    )
    shares_comments_fig.update_xaxes(title_text='Comentarios Promedio (escala log)')
    shares_comments_fig.update_yaxes(title_text='Compartidos Promedio (escala log)')

    # Calcular métricas resumen
    total_influencers = len(filtered_df)
    avg_followers = filtered_df['followers'].mean() if not filtered_df.empty else 0
    avg_views = filtered_df['views'].mean() if not filtered_df.empty else 0
    avg_likes = filtered_df['likes'].mean() if not filtered_df.empty else 0
    avg_engagement = filtered_df['engagement_rate'].mean() if not filtered_df.empty else 0

    summary_metrics = html.Div([
        html.Div([
            html.Div([
                html.H4(f"{total_influencers:,}"),
                html.P("Total de Influencers")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),

            html.Div([
                html.H4(f"{avg_followers/1_000_000:.2f}M"),
                html.P("Prom. Seguidores")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),

            html.Div([
                html.H4(f"{avg_views/1_000_000:.2f}M"),
                html.P("Prom. Visualizaciones")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),

            html.Div([
                html.H4(f"{avg_likes/1_000:.2f}K"),
                html.P("Prom. Likes")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),

            html.Div([
                html.H4(f"{avg_engagement:.2f}%"),
                html.P("Prom. Tasa Engagement")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'})
        ])
      ])

    # Gráfico Radar
    row = df_tt[df_tt['name'] == name].iloc[0]
    metrics = ['followers', 'views', 'likes', 'comments', 'shares']

    # Nombres más amigables para las métricas
    metrics_labels = {
      'followers': 'Seguidores',
      'views': 'Visualizaciones Prom.',
      'likes': 'Likes Prom.',
      'comments': 'Comentarios Prom.',
      'shares': 'Compartidos Prom.'
      }

    # Los valores para el gráfico radar
    values = [row['followers'],
              row['views'],
              row['likes'],
              row['comments'],
              row['shares']]

    # Crear el gráfico de radar
    radar_fig = go.Figure(data=[go.Scatterpolar(
      r=values,
      theta=metrics,
      fill='toself',
      name='Promedios de Métricas',
      line=dict(color='blue'),
      hovertemplate='%{theta}: %{r}<br>'  # Cambia lo que aparece en el hover
      )])

    # Ajustar las etiquetas del hovertemplate
    radar_fig.update_traces(
      hovertemplate=[
        f"{metrics_labels[metric]}: {row[metric]/1000}K" for metric in metrics_labels.keys()
      ]
    )


    radar_fig.update_layout(
      polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, max(values) * 1.2]  # Ajusta el rango del gráfico según las métricas
        )
    ),
        title=f"Gráfico de Radar Estadísticas de {name}",
        showlegend=False
      )

    stats = html.Ul([
        html.Li(f"Canal: {row['name']}"),
        html.Li(f"Username: {row['username']}"),
        html.Li(f"Seguidores: {row['followers']:,}"),
        html.Li(f"Engagement Rate: {row['engagement_rate'] * 100:.2f}%"),
        html.Li(f"Visualizaciones: {row['views']:,}"),
        html.Li(f"Likes: {row['likes']:,}"),
        html.Li(f"Comentarios: {row['comments']:,}"),
        html.Li(f"Compartidos: {row['shares']:,}"),
        html.Li(f"Rank: {row['rank']}")
    ])

    return followers_fig, views_likes_fig, followers_engagement_fig, shares_comments_fig, summary_metrics, radar_fig, stats


### Callbacks para Instagram ###
@callback(
    [Output('yt-top-followers-chart', 'figure'),
     Output('yt-followers-views-scatter', 'figure'),
     Output('yt-category-distribution', 'figure'),
     Output('yt-geo-distribution', 'figure'),
     Output('yt-summary-metrics', 'children'),
     Output('yt-barras-apiladas', 'figure'),
     Output('yt-channel-details', 'children')],
    [Input('yt-category-dropdown', 'value'),
     Input('yt-country-dropdown', 'value'),
     Input('yt-top-n-slider', 'value'),
     Input('yt-channel-dropdown', 'value')],
    prevent_initial_call='initial_duplicate'
)

def update_yt_charts(category, country, top_n, name):
    # Filtrar datos según las selecciones
    filtered_df = df_yt.copy()

    if category != 'All':
        filtered_df = filtered_df[filtered_df['category'] == category]

    if country != 'All':
        filtered_df = filtered_df[filtered_df['country'] == country]

    # Gráfico de top seguidores
    top_followers_df = filtered_df.sort_values('followers', ascending=False).head(top_n)
    followers_fig = px.bar(
      top_followers_df,
      y='name',
      x='followers',
      color='engagement_rate',
      hover_data=['username', 'username', 'category', 'country'],
      labels={'name': 'Nombre del Influencer', 'followers': 'Cantidad de Seguidores'},
      color_continuous_scale=px.colors.sequential.Purples,
      title=f'Top {top_n} youtubers por seguidores'
    )
    followers_fig.update_traces(
      hovertemplate='<b>%{y}</b><br>' +
                    'Seguidores: %{x}<br>' +
                    'Tasa de Engagement: %{marker.color:.2f}%<br>')
    followers_fig.update_layout(
      xaxis={'categoryorder': 'total descending'},  # Esto asegura que la barra con más seguidores esté arriba
      yaxis={'categoryorder': 'total ascending'}  # Asegura que los nombres estén ordenados correctamente
    )

    # Gráfico de puntos seguidores Vs Visitas
    engagement_fig = px.scatter(
        filtered_df,
        x='followers',
        y='views',
        size='followers',
        color='category',
        hover_name='username',
        size_max=60,
        title='Tasa de Seguidores vs. visitas'
    )
    engagement_fig.update_xaxes(title_text='Seguidores')
    engagement_fig.update_yaxes(title_text='Visitas')

    # Distribución por categoría
    category_counts = filtered_df['category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']
    category_fig = px.pie(
        category_counts,
        values='Count',
        names='Category',
        title='Distribución por Categoría',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    category_fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        insidetextorientation='radial',
        textfont_size=12,
        marker=dict(line=dict(color='#FFFFFF', width=1)))

    # En la parte donde creamos el category_fig (dentro de update_ig_charts), modificamos el update_layout así:
    category_fig.update_layout(
        margin=dict(l=50, r=250, t=40, b=20),  # Ajustamos márgenes: izquierdo más pequeño, derecho más grande
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",  # Cambiamos a "left" para que la leyenda se ancle a la izquierda
            x=1.05,         # Posición horizontal (1.05 la coloca justo a la derecha del gráfico)
            font=dict(size=12),
            bgcolor='rgba(255,255,255,0.5)'  # Fondo semitransparente para mejor legibilidad
        ),
        height=500,
        width=800,
        autosize=False,
        showlegend=True
    )


    # Distribución geográfica
    geo_counts = filtered_df['country'].value_counts().reset_index()
    geo_counts.columns = ['Country', 'Count']
    geo_fig = px.choropleth(
        geo_counts,
        locations='Country',
        locationmode='country names',
        color='Count',
        color_continuous_scale=px.colors.sequential.Purples,
        title='Distribución Geográfica',
        labels={'Count': 'Número de Influencers'}
    )

    # Ajustamos el tamaño y formato del gráfico geográfico
    geo_fig.update_layout(
      height=500,
      width=800,
      autosize=False,
      showlegend=True
    )

    # Calcular métricas resumen
    total_influencers = len(filtered_df)
    avg_followers = filtered_df['followers'].mean() if not filtered_df.empty else 0
    avg_engagement = filtered_df['engagement_rate'].mean() if not filtered_df.empty else 0
    max_followers = filtered_df['followers'].max() if not filtered_df.empty else 0
    top_influencer = filtered_df.loc[filtered_df['followers'].idxmax()]['username'] if not filtered_df.empty else 'N/A'

    summary_metrics = html.Div([
        html.Div([
            html.Div([
                html.H4(f"{total_influencers:,}"),
                html.P("Total de Influencers")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),

            html.Div([
                html.H4(f"{avg_followers/1_000_000:.2f}M"),
                html.P("Prom. Seguidores")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),

            html.Div([
                html.H4(f"{avg_engagement:.2f}%"),
                html.P("Prom. Tasa Engagement")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),

            html.Div([
                html.H4(f"{max_followers/1_000_000:.2f}M"),
                html.P("Máx. Seguidores")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),

            html.Div([
                html.H4(top_influencer),
                html.P("Top Influencer")
            ], style={'width': '20%', 'display': 'inline-block', 'textAlign': 'center'})
        ])
    ])

    # Gráfico barras apiladas
    # Para ello necesitamos adaptar el dataframe
    # Agrupar por categoría y sumar las visualizaciones
    category_country_views = filtered_df.groupby(['country', 'category']).sum()['views'].unstack(fill_value=0)

    # Crear un gráfico de barras apiladas
    fig_barras_apiladas = go.Figure()

    # Para no repetir colores, procedemos como hemos hecho en el gráfico
    # de barras apiladas de instagram
    unique_countries = category_country_views.index.unique()

    colors = pc.qualitative.Plotly + pc.qualitative.D3 + pc.qualitative.G10 + pc.qualitative.T10

    if len(unique_countries) > len(colors):
        more_colors = px.colors.sample_colorscale(
            px.colors.sequential.Viridis,
            [i/(len(unique_countries) - len(colors)) for i in range(len(unique_countries) - len(colors))]
        )
        colors.extend(more_colors)

    color_map = {country: colors[i % len(colors)] for i, country in enumerate(unique_countries)}

    for i, country in enumerate(category_country_views.index):
        fig_barras_apiladas.add_trace(go.Bar(
            x=category_country_views.columns,
            y=category_country_views.loc[country],
            name=country,
            marker_color=color_map[country]
        ))



    # Configurar el layout del gráfico
    fig_barras_apiladas.update_layout(
      barmode='stack',  # Establecer el modo de barras apiladas
      title='Gráfico de Barras Apiladas por País y Categoría',
      xaxis_title='Categoría',
      yaxis_title='Visualizaciones Totales',
      xaxis=dict(tickmode='array', tickvals=list(category_country_views.columns)),
      showlegend=True
      )

    row = df_yt[df_yt['name'] == name].iloc[0]
    stats = html.Ul([
        html.Li(f"Canal: {row['name']}"),
        html.Li(f"Username: {row['username']}"),
        html.Li(f"Seguidores: {row['followers']:,}"),
        html.Li(f"Engagement Rate: {row['engagement_rate'] * 100:.2f}%"),
        html.Li(f"Visualizaciones: {row['views']:,}"),
        html.Li(f"Likes: {row['likes']:,}"),
        html.Li(f"Comentarios: {row['comments']:,}")
    ])



    return followers_fig, engagement_fig, category_fig, geo_fig, summary_metrics, fig_barras_apiladas, stats



if __name__ == '__main__':
    app.run(debug=True, port=8050)

# Cuando ejecutemos este archivo, y se mantenga en suspensión
# deberemos introducir en un buscador --> http://127.0.0.1:8050/