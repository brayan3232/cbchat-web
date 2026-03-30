import streamlit as st
from openai import OpenAI

# Configuración de la página
st.set_page_config(page_title="CBCHAT V2", page_icon="🤖", layout="centered")

# --- ESTILO CSS AVANZADO ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stChatFloatingInputContainer { bottom: 20px; }
    
    /* Burbujas de chat redondas */
    [data-testid="stChatMessage"] {
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    
    /* Estilo para los botones de arriba */
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #e0e0e0;
        background-color: white;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        border-color: #007bff;
        color: #007bff;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 CBCHAT")
st.markdown("<p style='text-align: center; color: #666;'>Inteligencia Artificial con soporte visual</p>", unsafe_allow_html=True)

# --- CONEXIÓN CON TU PC ---
# RECUERDA: Si el link de localtunnel cambia, actualízalo aquí abajo.
client = OpenAI(base_url="https://fruity-hotels-warn.loca.lt/v1", api_key="lm-studio")

# --- SOPORTE PARA FOTOS ---
with st.sidebar:
    st.header("Multimedia")
    foto_subida = st.file_uploader("Subir una imagen", type=["png", "jpg", "jpeg"])
    if foto_subida:
        st.image(foto_subida, caption="Imagen cargada", use_container_width=True)
        st.success("Imagen lista para procesar (necesitas un modelo Vision en LM Studio)")

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input de usuario
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            completion = client.chat.completions.create(
                model="local-model", # LM Studio usa el que esté cargado
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        except Exception as e:
            st.error("Error: ¿El túnel sigue abierto?")
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
