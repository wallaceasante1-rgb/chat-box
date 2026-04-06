import streamlit as st
from chatbot.logic import get_response
import pyttsx3

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar options
st.sidebar.title("Chatbot Settings")
personality = st.sidebar.selectbox("Choose Bot Personality", ["Friendly", "Professional", "Funny"])
model_choice = st.sidebar.selectbox("Choose Model", ["DialoGPT-small", "DialoGPT-medium"])
voice_enabled = st.sidebar.checkbox("Enable Voice Output")

st.title("🤖 Chatbot App")

# User input
user_input = st.text_input("You:", "")

if user_input:
    response = get_response(user_input, personality=personality, model=model_choice)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", response))

    # Voice output
    if voice_enabled:
        engine = pyttsx3.init()
        engine.say(response)
        engine.runAndWait()

# Display chat history with styled bubbles
for speaker, text in st.session_state.history:
    if speaker == "You":
        st.markdown(f"<div style='background-color:#d1e7dd;padding:10px;border-radius:10px;margin:5px;'>**You:** {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background-color:#f8d7da;padding:10px;border-radius:10px;margin:5px;'>**Bot:** {text}</div>", unsafe_allow_html=True)

# Download chat
if st.session_state.history:
    chat_text = "\n".join([f"{s}: {t}" for s, t in st.session_state.history])
    st.download_button("Download Chat", chat_text, "chat.txt")

