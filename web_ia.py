import streamlit as st
from openai import OpenAI
from datetime import date

# Configuración de la página
st.set_page_config(page_title="CBCHAT V2", page_icon="🤖", layout="wide")

# --- ESTILO VISUAL PERSONALIZADO ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stTitle { 
        font-family: 'Segoe UI', sans-serif; 
        font-weight: 800; 
        text-align: center;
        margin-top: -50px;
    }
    .cbchat-text { color: #007bff; } /* Color azul para CBCHAT, puedes cambiarlo a rojo si prefieres */
    .subtitle { text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 2rem; }
    
    /* Botones centrales estilo pastilla */
    .btn-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-bottom: 50px;
        flex-wrap: wrap;
    }
    .pill-btn {
        border: 1px solid #e0e0e0;
        padding: 10px 25px;
        border-radius: 25px;
        background: white;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("<h1 style='text-align: center;'>Presentamos <span class='cbchat-text'>CBCHAT</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Con búsqueda en la web e interacción de voz</p>", unsafe_allow_html=True)

# --- BOTONES EN ESPAÑOL ---
st.markdown("""
    <div class="btn-container">
        <div class="pill-btn">🌐 Buscar en la web</div>
        <div class="pill-btn">🖼️ Generar Imágenes</div>
        <div class="pill-btn">🧠 Persuasión</div>
        <div class="pill-btn">💻 Programar</div>
    </div>
""", unsafe_allow_html=True)

# --- CONEXIÓN CON TU IA (LM STUDIO) ---
client = OpenAI(base_url="https://shaky-beds-chew.loca.lt", api_key="lm-studio")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar el historial del chat
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- BARRA DE ENTRADA ---
if prompt := st.chat_input("Escribe tu búsqueda o pregunta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="local-model",
                messages=[
                    {"role": "system", "content": f"Eres CBCHAT, una IA creada por mxz. Hoy es {date.today()}"},
                    *st.session_state.messages
                ]
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except:
            st.error("❌ Error: ¿Olvidaste encender el botón 'Start Server' en LM Studio?")
