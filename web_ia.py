import streamlit as st
from openai import OpenAI

# Configuración de la página
st.set_page_config(page_title="CBCHAT Pro", page_icon="💬", layout="centered")

# --- ESTILO IPHONE (iOS) ---
st.markdown("""
    <style>
    /* Fondo claro estilo Apple */
    .main { background-color: #ffffff; }
    
    /* Contenedor de mensajes */
    [data-testid="stChatMessage"] {
        padding: 10px 15px;
        border-radius: 20px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 16px;
        margin-bottom: 8px;
        width: fit-content;
        max-width: 75%;
    }

    /* MENSAJE DEL USUARIO (AZUL iMessage) */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        margin-left: auto;
        background-color: #007AFF !important; /* Azul iPhone */
        color: white !important;
        border-bottom-right-radius: 4px;
    }
    
    /* MENSAJE DEL ASISTENTE (GRIS Apple) */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        margin-right: auto;
        background-color: #E9E9EB !important; /* Gris claro iPhone */
        color: black !important;
        border-bottom-left-radius: 4px;
    }

    /* Esconder iconos y labels para que parezca chat real */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {
        display: none;
    }
    
    /* Estilo del input */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💬 CBCHAT")

# --- CONEXIÓN CON GROQ (Rápida y estable) ---
client = OpenAI(
    base_url="https://api.groq.com/openai/v1", 
    api_key="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"
)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📸 Multimedia")
    foto_subida = st.file_uploader("Subir foto", type=["png", "jpg", "jpeg"])
    if foto_subida:
        st.image(foto_subida)

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Escribe un mensaje..."):
    # 1. Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Efecto "Pensando..." estilo iPhone
    with st.chat_message("assistant"):
        with st.status("✨ Pensando...", expanded=False) as status:
            response_placeholder = st.empty()
            full_response = ""
            
            try:
                completion = client.chat.completions.create(
                    model="local-model",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    stream=True,
                )
                
                # Una vez que empieza a responder, el status cambia
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response)
                
                status.update(label="✅ Respuesta lista", state="complete", expanded=False)
                
            except Exception as e:
                status.update(label="❌ Error de conexión", state="error")
                st.error("Revisa que LM Studio y el Túnel estén abiertos.")
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
