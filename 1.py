from streamlit_drawable_canvas import st_canvas
import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import datetime
import os
import math

# ------------ CONFIGURACIÓN BÁSICA ------------

st.set_page_config(
    page_title="Train Stations Map - Austria", # Título de la página
    page_icon="🚆",
    layout="wide",
)

# Página por defecto: mapa
if "page" not in st.session_state:
    st.session_state["page"] = "mapa"


# ------------ DATOS DE ESTACIONES (AUSTRIA) ------------

STATIONS_DATA = [
    {
        "estacion": "Wien Hauptbahnhof",
        "ciudad": "Viena",
        "lat": 48.186667,
        "lon": 16.38,
        "linea": "Nodo principal Este",
    },
    {
        "estacion": "Wien Mitte (Landstraße)",
        "ciudad": "Viena",
        "lat": 48.206389,
        "lon": 16.384722,
        "linea": "S-Bahn / CAT",
    },
    {
        "estacion": "Wien Floridsdorf",
        "ciudad": "Viena",
        "lat": 48.256389,
        "lon": 16.4,
        "linea": "Norte / S-Bahn",
    },
    {
        "estacion": "Wien Hetzendorf",
        "ciudad": "Viena",
        "lat": 48.147,
        "lon": 16.322,
        "linea": "S1 / S2 (S-Bahn)",
    },
    {
        "estacion": "Wien Liesing",
        "ciudad": "Viena",
        "lat": 48.1541,
        "lon": 16.2925,
        "linea": "S2 / S3 / S4",
    },
    {
        "estacion": "Wien Handelskai",
        "ciudad": "Viena",
        "lat": 48.2377,
        "lon": 16.3861,
        "linea": "S45 / S7",
    },
    {
        "estacion": "Wien Praterstern",
        "ciudad": "Viena",
        "lat": 48.2168,
        "lon": 16.3924,
        "linea": "S1 / S2 / S3 / S7",
    },
    {
        "estacion": "Wien Rennweg",
        "ciudad": "Viena",
        "lat": 48.2010,
        "lon": 16.3935,
        "linea": "S7",
    },
    {
        "estacion": "Wien Quartier Belvedere",
        "ciudad": "Viena",
        "lat": 48.1937,
        "lon": 16.3898,
        "linea": "S1 / S2 / S3",
    },
    {
        "estacion": "Wien Süßenbrunn",
        "ciudad": "Viena",
        "lat": 48.2250,
        "lon": 16.4525,
        "linea": "S1",
    },
    {
        "estacion": "Wien Leopoldau",
        "ciudad": "Viena",
        "lat": 48.2625,
        "lon": 16.4147,
        "linea": "S1 / S2 / S3 / S4",
    },
    {
        "estacion": "Wien Traisengasse",
        "ciudad": "Viena",
        "lat": 48.2358,  # según Czech‑Transport :contentReference[oaicite:0]{index=0}  
        "lon": 16.3826,
        "linea": "S Bahn / Stammstrecke",
    },
    {
        "estacion": "Wien Kaiserebersdorf",
        "ciudad": "Viena",
        "lat": 48.146039,  # según Wikipedia :contentReference[oaicite:1]{index=1}  
        "lon": 16.465389,
        "linea": "S7",
    },
    {
        "estacion": "Wien Süßenbrunn",
        "ciudad": "Viena",
        "lat": 48.28557,  # según Mapcarta / OSM :contentReference[oaicite:2]{index=2}  
        "lon": 16.48552,
        "linea": "S1",  # aproximado
    },
    {
        "estacion": "Wien Matzleinsdorfer Platz",
        "ciudad": "Viena",
        "lat": 48.1683,  # aproximado (según plano y posición del distrito Favoriten)
        "lon": 16.3721,  # aproximado
        "linea": "S Bahn / Verbindungsbahn",
    },
    {
        "estacion": "Wien Ottakring",
        "ciudad": "Viena",
        "lat": 48.1981,  # aproximado según su ubicación en el distrito Ottakring :contentReference[oaicite:3]{index=3}  
        "lon": 16.3317,
        "linea": "S Bahn",
    },
    {
        "estacion": "Wien Praterstern",
        "ciudad": "Viena",
        "lat": 48.2181,  # coordenadas aproximadas :contentReference[oaicite:4]{index=4}  
        "lon": 16.3919,
        "linea": "S1 / S2 / S3 / S7",
    },
    {
        "estacion": "Wien Rennweg",
        "ciudad": "Viena",
        "lat": 48.2010,  # ya lo teníamos, pero lo repito con más contexto :contentReference[oaicite:5]{index=5}  
        "lon": 16.3935,
        "linea": "S7 / Verbindungsbahn",
    },
    {
        "estacion": "Wien Hauptbahnhof",
        "ciudad": "Viena",
        "lat": 48.1851589,  # según Czech‑Transport :contentReference[oaicite:6]{index=6}  
        "lon": 16.3756792,
        "linea": "S Bahn / Internacional",
    },
    {
        "estacion": "Wien Mitte (Landstraße)",
        "ciudad": "Viena",
        "lat": 48.2061,  # según Czech‑Transport :contentReference[oaicite:7]{index=7}  
        "lon": 16.3852,
        "linea": "S Bahn / CAT",
    },
    {
        "estacion": "Wien Heiligenstadt",
        "ciudad": "Viena",
        "lat": 48.248785,  # según datos GPS :contentReference[oaicite:0]{index=0}  
        "lon": 16.365726,
        "linea": "S40 / S45",
    },
    {
        "estacion": "Wien Strebersdorf",
        "ciudad": "Viena",
        "lat": 48.285669,  # según lista S-Bahn Viena :contentReference[oaicite:1]{index=1}  
        "lon": 16.381470,
        "linea": "S3 / S4",
    },
    {
        "estacion": "Wien Matzleinsdorfer Platz",
        "ciudad": "Viena",
        "lat": 48.1801806,  # según lista estación S-Bahn :contentReference[oaicite:2]{index=2}  
        "lon": 16.3581194,
        "linea": "Stammstrecke / Verbindungsbahn",
    },
    {
        "estacion": "Wien Gersthof",
        "ciudad": "Viena",
        "lat": 48.23125,  # según lista S-Bahn :contentReference[oaicite:3]{index=3}  
        "lon": 16.329,
        "linea": "Vorortelinie",
    },
    {
        "estacion": "Wien Ottakring",
        "ciudad": "Viena",
        "lat": 48.2117111,  # según lista S-Bahn :contentReference[oaicite:4]{index=4}  
        "lon": 16.3112111,
        "linea": "Vorortelinie",
    },
    {
        "estacion": "Wien Nußdorf",
        "ciudad": "Viena",
        "lat": 48.25995,  # según lista S-Bahn :contentReference[oaicite:5]{index=5}  
        "lon": 16.36793,
        "linea": "Franz‑Josefs‑Bahn",
    },
    {
        "estacion": "Wien Spittelau",
        "ciudad": "Viena",
        "lat": 48.2354,  # según lista S-Bahn :contentReference[oaicite:6]{index=6}  
        "lon": 16.3581889,
        "linea": "S40 / S45",
    },
    {
        "estacion": "Wien Simmering",
        "ciudad": "Viena",
        "lat": 48.1701389,  # según lista S-Bahn :contentReference[oaicite:7]{index=7}  
        "lon": 16.41975,
        "linea": "Laaer Ostbahn / S‑Bahn",
    },
    {
        "estacion": "Wien Speising",
        "ciudad": "Viena",
        "lat": 48.17345,  # según lista S-Bahn :contentReference[oaicite:8]{index=8}  
        "lon": 16.2842111,
        "linea": "S‑Bahn / Lainzer Tunnel",
    },
    {
        "estacion": "Wien Nußdorf",
        "ciudad": "Viena",
        "lat": 48.25995,
        "lon": 16.36793,
        "linea": "S‑Bahn / Vorortelinie",
    },
    {
        "estacion": "Wien Leopoldau",
        "ciudad": "Viena",
        "lat": 48.2775,  # según la Wikipedia del Bahnhof Leopoldau :contentReference[oaicite:9]{index=9}  
        "lon": 16.452222,
        "linea": "S1 / S2 / S3 / U1",
    },
    {
        "estacion": "Wien Franz‑Josefs‑Bahnhof",
        "ciudad": "Viena",
        "lat": 48.226867,  # aproximado para Franz‑Josefs‑Bahnhof  
        "lon": 16.360852,  
        "linea": "S40 / Franz‑Josefs‑Bahn",
    },
]

FILE_OPINIONES = "opiniones_austria.csv"


# ------------ FUNCIONES DE DATOS ------------

def cargar_opiniones() -> pd.DataFrame:
    """Carga las opiniones desde CSV, si no existe regresa DataFrame vacío."""
    if not os.path.exists(FILE_OPINIONES):
        return pd.DataFrame(
            columns=["fecha", "estacion", "texto", "satisfaccion"]
        )

    df = pd.read_csv(FILE_OPINIONES, encoding="utf-8")

    # Asegurar columnas mínimas
    if "satisfaccion" not in df.columns:
        df["satisfaccion"] = None

    return df


def guardar_opinion(fecha: str, estacion: str, texto: str, satisfaccion: int):
    """Agrega una nueva opinión al CSV."""
    df = cargar_opiniones()
    nueva_fila = pd.DataFrame(
        [{
            "fecha": fecha,
            "estacion": estacion,
            "texto": texto,
            "satisfaccion": satisfaccion,
        }]
    )
    df = pd.concat([df, nueva_fila], ignore_index=True)
    df.to_csv(FILE_OPINIONES, index=False, encoding="utf-8")


def score_to_emoji_color(score):
    """
    Convierte un score numérico (1–5) en:
    - emoji
    - color [R,G,B,alpha] para el mapa
    """
    if score is None or (isinstance(score, float) and math.isnan(score)):
        return "🤔", [150, 150, 150, 180]

    if score >= 4:
        return "😄", [0, 200, 0, 200]       # verde
    if score >= 3:
        return "😐", [230, 180, 0, 200]     # amarillo
    return "😡", [220, 0, 0, 200]           # rojo

# ------------ VISTA: MAPA PRINCIPAL MODIFICADA ------------
def vista_mapa():
    st.title("🚆 Train Station Map in Austria") # Título traducido
    st.write(
        "Visualize the satisfaction status per station. " # Texto traducido
        "Each dot represents a main station and its emoji reflects " # Texto traducido
        "how people perceive it based on surveys." # Texto traducido
    )

    estaciones_df = pd.DataFrame(STATIONS_DATA)
    opiniones_df = cargar_opiniones()


    # Agregar satisfacción media por estación
    if not opiniones_df.empty and "satisfaccion" in opiniones_df.columns:
        agg = (
            opiniones_df
            .dropna(subset=["satisfaccion"])
            .groupby("estacion")["satisfaccion"]
            .mean()
            .reset_index(name="satisfaccion_media")
        )
        estaciones_df = estaciones_df.merge(
            agg, on="estacion", how="left"
        )
    else:
        estaciones_df["satisfaccion_media"] = None


    # Calcular emoji y color
    results = estaciones_df["satisfaccion_media"].apply(score_to_emoji_color)
    estaciones_df["emoji"] = [r[0] for r in results]
    estaciones_df["color"] = [r[1] for r in results]

    # Mostrar mapa
    st.subheader("🗺️ Interactive Map of Austria") # Subtítulo traducido
    st.map(
        estaciones_df,
        latitude="lat",
        longitude="lon",
        zoom=10,
        width='stretch'
    )

# Mostrar tabla de estaciones
    st.subheader("📊 List of Stations") # Subtítulo traducido
    tabla_estaciones = estaciones_df[["estacion", "ciudad"]].copy()
    seleccion_estacion = st.selectbox("Select a station:", tabla_estaciones["estacion"]) # Etiqueta traducida

    # Filtrar la estación seleccionada
    estacion_seleccionada = estaciones_df[estaciones_df["estacion"] == seleccion_estacion].iloc[0]

# Mostrar la calificación con emoji solo si hay una estación seleccionada
    if not pd.isna(estacion_seleccionada["satisfaccion_media"]):
        st.write(f"📝 Satisfaction for station '{estacion_seleccionada['estacion']}':") # Texto traducido
        st.write(f"**Average Satisfaction:** {estacion_seleccionada['satisfaccion_media']}") # Texto traducido
        st.write(f"**Emoji:** {estacion_seleccionada['emoji']}")
    else:
        st.write(f"**No satisfaction data available for station '{estacion_seleccionada['estacion']}'**") # Texto traducido



    
# ------------ VISTA: ENCUESTA ------------

def vista_encuesta():
    st.title("📝 Station Experience Survey in Austria") # Título traducido
    st.write(
        "Tell us about your experience at a specific station. " # Texto traducido
        "We will use this data to update the satisfaction map." # Texto traducido
    )

    estaciones_df = pd.DataFrame(STATIONS_DATA)
    lista_estaciones = estaciones_df["estacion"].tolist()

    estacion = st.selectbox(
        "Which station was your experience at?", # Etiqueta traducida
        lista_estaciones,
    )

    satisfaccion = st.slider(
        "How would you rate your overall experience?", # Etiqueta traducida
        min_value=1,
        max_value=5,
        value=3,
        help="1 = very bad, 5 = excellent", # Texto de ayuda traducido
    )

    texto = st.text_area(
        "Describe what happened (delays, cleanliness, safety, comfort, etc.):", # Etiqueta traducida
        height=150,
        placeholder="Example: The train arrived 15 minutes late and the restrooms were dirty...", # Placeholder traducido
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Submit opinion"): # Botón traducido
            if texto.strip() == "":
                st.warning("Please write a comment before submitting.") # Mensaje traducido
            else:
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                guardar_opinion(fecha, estacion, texto, satisfaccion)
                st.success("✅ Thank you! Your opinion has been saved and will be reflected on the map.") # Mensaje traducido
                st.info("You can return to the map to see the impact of your opinion.") # Mensaje traducido
                st.rerun()

    with col2:
        if st.button("⬅️ Back to map"): # Botón traducido
            st.session_state["page"] = "mapa"
            st.rerun()

    st.markdown("---")

    st.subheader("📋 Recent Opinions") # Subtítulo traducido
    opiniones_df = cargar_opiniones()
    if opiniones_df.empty:
        st.info("No opinions saved yet.") # Mensaje traducido
    else:
        try:
            opiniones_df["fecha"] = pd.to_datetime(opiniones_df["fecha"])
            opiniones_df = opiniones_df.sort_values("fecha", ascending=False)
        except Exception:
            pass

        st.dataframe(opiniones_df, width='stretch')

# ------------ ROUTER DE PÁGINAS ------------

if st.session_state["page"] == "mapa":
    vista_mapa()
else:
    vista_encuesta()

# --- ENCUESTA ABAJO DE TODO ---
# --- ENCUESTA GLOBAL CON 3 EMOJIS ---
st.markdown("---")
st.subheader("😊 How do you feel about this station?") # Subtítulo traducido

colA, colB, colC = st.columns(3)

with colA:
    # Usamos claves para evitar problemas si Streamlit intenta crear otro botón similar
    if st.button("😡", width='stretch', key="btn_global_angry"):
        st.session_state["emoji_mode"] = "angry"
        st.rerun()

with colB:
    if st.button("😐", width='stretch', key="btn_global_neutral"):
        st.session_state["emoji_mode"] = "neutral"
        st.rerun()

with colC:
    if st.button("😄", width='stretch', key="btn_global_Happy"):
        st.session_state["emoji_mode"] = "Happy"
        st.rerun()

# --- Mostrar multiselect según el emoji global seleccionado ---
if "emoji_mode" in st.session_state and st.session_state["emoji_mode"]:
    emoji = st.session_state["emoji_mode"]

    # Palabras diferentes según el emoji
    palabras_por_emoji = {
        "angry": ["frustrated", "tense", "annoyed", "agitated", "irritated"],
        "neutral": ["calm", "normal", "stable", "indifferent", "relaxed"],
        "Happy":   ["happy", "lively", "positive", "enthusiastic", "cheerful"]
    }

    st.write(f"Select the words that best describe your {emoji} emotion:") # Texto traducido
    seleccion = st.multiselect(
        "Words for your mood:", # Etiqueta traducida
        palabras_por_emoji[emoji],
        key="global_multiselect" # Añadimos una clave para estabilidad
    )
    
    # -----------------------------------------------------------
    # NUEVA ADICIÓN: Campo de texto libre y Botón de Envío Final
    # Solo se muestra si ya se seleccionaron palabras clave.
    # -----------------------------------------------------------
    if seleccion:
        st.markdown("---")
        st.subheader("📝 Free Comment") # Subtítulo traducido
        st.write("Now, if you wish, you can write a detailed comment to accompany your emotion:") # Texto traducido
        
        comentario_libre = st.text_area(
            "Write your comment here:", # Etiqueta traducida
            height=100,
            placeholder="E.g.: I chose 'frustrado' because the air conditioning wasn't working in carriage 3.", # Placeholder traducido
            key="global_text_area" # Añadimos clave
        )
        
        # Botón para simular el envío final de los datos
        if st.button("Submit Comment and Quick Feedback", key="btn_final_feedback"): # Botón traducido
            # *************************************************************
            # AQUÍ DEBES AGREGAR LA LÓGICA REAL PARA GUARDAR ESTOS DATOS
            # (estación actual, palabras clave seleccionadas, comentario libre).
            # *************************************************************
            
            st.success(f"✅ Quick Feedback Submitted!") # Mensaje traducido
            st.info(f"Emotion: **{emoji}**\n\nSelected words: **{', '.join(seleccion)}**\n\nComment: **{comentario_libre or 'No free comment'}**") # Mensaje traducido
            
            # Opcional: Limpiar el estado después del envío
            del st.session_state["emoji_mode"]
            # st.rerun() # Si quieres recargar la página

            # --- PIZARRÓN INTERACTIVO ---
st.markdown("---")
st.subheader("🖍️ Interactive Whiteboard (Whiteboard / Sketchpad)") # Subtítulo traducido
st.write("Use this space to quickly sketch or take notes about your experience:") # Texto traducido

# Especifica las propiedades del lienzo (Canvas)
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Color de relleno predeterminado
    stroke_width=3, # Ancho del pincel
    stroke_color="#000000", # Color predeterminado (negro)
    background_color="#FFFFFF", # Fondo blanco para el pizarrón
    height=300, # Altura del área de dibujo
    drawing_mode="freedraw", # Modo de dibujo libre
    key="canvas_board",
)

# Opcional: Mostrar los datos del dibujo si el usuario garabatea algo
if canvas_result.image_data is not None:
    # Muestra el botón de descarga solo si hay algo dibujado
    if st.button("Download Sketch"): # Botón traducido
        # En una aplicación real, usarías la imagen_data para guardarla
        st.info("The drawing data has been registered.") # Mensaje traducido
        # Aquí podrías agregar la lógica para guardar canvas_result.image_data (p. ej., a un archivo PNG)
        # --- INICIO DE CÓDIGO A AGREGAR ---
st.markdown(
    """
    <style>
    /* Estilo para usar blanco como fondo principal
    y un color rojo/vino para el texto o elementos importantes, 
    simulando la combinación 'rojo con blanco'.
    */
    .stApp {
        background-color: #FFFFFF; /* Fondo completamente blanco */
    }
    
    /* Cambiar el color del texto de los títulos a un color rojo */
    h1, h2, h3, h4, h5, h6 {
        color: #CC0000; /* Rojo vibrante */
    }
    
    /* Cambiar el color de los botones principales a un estilo rojo */
    div.stButton > button {
        background-color: #CC0000;
        color: white;
        border-radius: 5px;
    }
    
    /* Puedes cambiar otros elementos si lo deseas, como la barra lateral */
    /* .stSidebar {
        background-color: #F0F0F0; 
    } */

    </style>
    """,
    unsafe_allow_html=True
)
# --- FIN DE CÓDIGO A AGREGAR ---
# --- AÑADE ESTE BLOQUE AQUÍ PARA INYECTAR EL CSS ---
st.markdown(
    """
    <style>
    /* 1. Fondo de la aplicación (la página) completamente blanco */
    .stApp {
        background-color: #FFFFFF;
        /* Asegura que el texto general del cuerpo sea negro */
        color: #000000;
    }
    
    /* 2. Asegura que todos los títulos (h1, h2, h3, etc.) sean negros */
    h1, h2, h3, h4, h5, h6 {
        color: #000000;
    }
    
    /* 3. Estilo para los botones: fondo rojo y letras blancas */
    div.stButton > button {
        background-color: #CC0000; /* Rojo vibrante */
        color: white; /* Letras blancas para contraste */
        border: none; /* Sin borde */
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
    }

    /* 4. Estilo para el texto dentro de widgets (para asegurar el negro) */
    div[data-testid="stText"], 
    div[data-testid="stMarkdownContainer"], 
    div[data-testid="stSidebar"] {
        color: #000000 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)
# --------------------------------------------------
st.markdown(
    """
    <style>
    /* 1. Fondo y Texto General */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* Títulos negros */
    h1, h2, h3, h4, h5, h6 {
        color: #000000;
    }
    
    /* 2. Estilo para los botones (Fondo Rojo y Letras Blancas) */
    div.stButton > button {
        background-color: #CC0000; /* Rojo vibrante */
        color: white; /* Letras blancas para contraste */
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        
        /* --- PROPIEDAD CLAVE PARA AGRANDAR EL EMOJI --- */
        font-size: 32px; /* Ajusta este valor (ej: 32px, 40px, 50px) para cambiar el tamaño */
        /* ----------------------------------------------- */
        
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
        height: auto; /* Permite que el botón se ajuste al tamaño de la fuente */
    }

    /* 3. Estilo para el texto dentro de widgets */
    div[data-testid="stText"], 
    div[data-testid="stMarkdownContainer"], 
    div[data-testid="stSidebar"] {
        color: #000000 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* 1. Fondo de la aplicación (la página) completamente blanco */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* 2. Color Rojo para la Franja Superior (Cabecera) */
    /* Apuntamos al contenedor principal del contenido (el que tiene el padding superior) */
    .st-emotion-cache-vk3wpk { /* Este selector puede variar, pero es común para el main-container */
        background-color: #CC0000; 
        color: white; /* Letras blancas para el texto dentro de la cabecera (si lo hay) */
    }
    
    /* 3. Asegura que todos los títulos (h1, h2, h3, etc.) sean negros */
    h1, h2, h3, h4, h5, h6 {
        color: #000000;
    }
    
    /* 4. Estilo para los botones (Fondo Rojo y Emojis Grandes) */
    div.stButton > button {
        background-color: #CC0000; 
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 32px; /* Tamaño grande para los emojis */
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
        height: auto;
    }

    /* 5. Estilo para el texto general (para asegurar el negro) */
    div[data-testid="stText"], 
    div[data-testid="stMarkdownContainer"], 
    div[data-testid="stSidebar"],
    div[data-testid="stHeader"] { /* Incluir el header */
        color: #000000 !important;
    }
    
    /* Selector alternativo para la barra superior de cabecera/header */
    [data-testid="stHeader"] {
        background-color: #CC0000; /* Fondo rojo para la barra de cabecera de Streamlit */
    }

    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* 1. Fondo y Texto General */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* 2. Color Rojo para la Franja Superior (Header) y texto blanco dentro de ella */
    [data-testid="stHeader"] {
        background-color: #CC0000; /* Fondo rojo para la barra de cabecera de Streamlit */
    }
    
    /* Asegura que el texto en la barra de cabecera sea blanco */
    [data-testid="stHeader"] h1 {
        color: white !important; 
        padding-top: 5px;
        padding-bottom: 5px;
        margin-top: 0;
        margin-bottom: 0;
    }
    
    /* 3. Títulos principales y texto negro (excepto el header) */
    h1:not([data-testid="stHeader"] h1), 
    h2, h3, h4, h5, h6 {
        color: #000000;
    }
    
    /* 4. Estilo para los botones (Fondo Rojo y Emojis Grandes) */
    div.stButton > button {
        background-color: #CC0000; 
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 32px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
        height: auto;
    }

    /* 5. Estilo para el texto general (para asegurar el negro) */
    div[data-testid="stText"], 
    div[data-testid="stMarkdownContainer"], 
    div[data-testid="stSidebar"] {
        color: #000000 !important;
    }
    
    /* Ocultar el texto de 'deploy' si existe para que solo se vea 'OBB' */
    .st-emotion-cache-1wmy99x { 
        display: none;
    }

    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* 1. Fondo y Texto General */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* 2. Color Rojo para la Franja Superior (Header) y texto blanco dentro de ella */
    [data-testid="stHeader"] {
        background-color: #CC0000;
    }
    [data-testid="stHeader"] h1 {
        color: white !important; 
        padding-top: 5px;
        padding-bottom: 5px;
        margin-top: 0;
        margin-bottom: 0;
    }
    
    /* 3. Títulos principales y texto negro (excepto el header) */
    h1:not([data-testid="stHeader"] h1), 
    h2, h3, h4, h5, h6 {
        color: #000000;
    }
    
    /* 4. Estilo para los botones (Fondo Rojo) */
    div.stButton > button {
        background-color: #CC0000; 
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px; /* Tamaño de fuente normal para los botones de la Encuesta */
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
        height: auto;
    }

    /* 5. Agrandar específicamente los Emojis de los botones globales */
    /* Apuntamos a los botones usando sus claves para ser específicos: btn_global_... */
    /* Este selector ajusta el tamaño del emoji para el feedback rápido al final de la app */
    button[key="btn_global_angry"], 
    button[key="btn_global_neutral"], 
    button[key="btn_global_Happy"] {
        font-size: 60px !important; /* ¡Nuevo tamaño! Ajusta 60px si quieres que sean más grandes o pequeños */
        height: 80px; /* Asegura que el botón se ajuste al emoji grande */
    }
    
    /* 6. Estilo para el texto general (para asegurar el negro) */
    div[data-testid="stText"], 
    div[data-testid="stMarkdownContainer"], 
    div[data-testid="stSidebar"] {
        color: #000000 !important;
    }
    
    /* Ocultar el texto de 'deploy' si existe */
    .st-emotion-cache-1wmy99x { 
        display: none;
    }

    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* 1. Fondo y Texto General */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* 2. Color Rojo para la Franja Superior (Header) y texto blanco dentro de ella */
    [data-testid="stHeader"] {
        background-color: #CC0000;
    }
    [data-testid="stHeader"] h1 {
        color: white !important; 
        padding-top: 5px;
        padding-bottom: 5px;
        margin-top: 0;
        margin-bottom: 0;
    }
    
    /* 3. Títulos principales y texto negro (excepto el header) */
    h1:not([data-testid="stHeader"] h1), 
    h2, h3, h4, h5, h6 {
        color: #000000;
    }
    
    /* 4. Estilo para los botones ESTÁNDAR (Fondo Rojo) */
    div.stButton > button {
        background-color: #CC0000; 
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px; 
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
        height: auto;
    }

    /* 5. Agrandar Emojis de los botones globales */
    button[key="btn_global_angry"], 
    button[key="btn_global_neutral"], 
    button[key="btn_global_Happy"] {
        font-size: 60px !important; 
        height: 80px;
    }
    
    /* 6. ESTILO PARA SELECT/MULTISELECT (Fondo Gris Claro) */
    /* Este selector apunta a los contenedores de st.selectbox y st.multiselect */
    div[data-testid="stSelectbox"] div[data-testid="stCaret"],
    div[data-testid="stMultiSelect"] div[data-testid="stCaret"],
    div[data-testid="stSelectbox"] div[data-testid="stInput"],
    div[data-testid="stMultiSelect"] div[data-testid="stInput"] {
        background-color: #F0F0F0 !important; /* Gris Claro */
        color: #000000 !important; /* Asegura el texto negro dentro */
    }

    /* 7. Estilo para el texto general (para asegurar el negro) */
    div[data-testid="stText"], 
    div[data-testid="stMarkdownContainer"], 
    div[data-testid="stSidebar"] {
        color: #000000 !important;
    }
    
    /* Ocultar el texto de 'deploy' si existe */
    .st-emotion-cache-1wmy99x { 
        display: none;
    }

    </style>
    """,
    unsafe_allow_html=True
)
# APLICACIÓN DE ESTILOS PERSONALIZADOS (CSS Injection)
st.markdown("""
            /* 2. Aumentar el tamaño de los emojis en los botones */
[data-testid="stButton"] p {
    font-size: 3.5em !important;
    line-height: 1;
    /* Anulamos el estilo de cuadro rojo que se aplicó al 'p' interno del botón para que no se vea mal */
    border: none !important;
    background-color: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
}
            </style>
""", unsafe_allow_html=True)
# APLICACIÓN DE ESTILOS PERSONALIZADOS (CSS Injection)
st.markdown("""
<style>
/* ... (otros estilos de texto) ... */

/* 2. Aumentar el tamaño de los emojis en los botones */
/* Targets the paragraph element inside the button, which holds the emoji */
[data-testid="stButton"] p {
    font-size: 3.5em !important; /* <--- ESTA LÍNEA AUMENTA EL TAMAÑO */
    line-height: 1;
    /* Anulamos el estilo de cuadro rojo que se aplicó al 'p' interno del botón para que no se vea mal */
    border: none !important;
    background-color: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* ... (otros estilos en negrita) ... */

</style>
""", unsafe_allow_html=True)