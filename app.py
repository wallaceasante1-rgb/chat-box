import streamlit as st
from chatbot.logic import get_response, reset_chat

st.title("🤖 AI Chatbot")

# Sidebar options
personality = st.sidebar.selectbox("Choose personality:", ["Friendly", "Professional", "Funny"])
model_choice = st.sidebar.selectbox("Choose model:", ["DialoGPT-small", "DialoGPT-medium"])

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("You:", "")

if user_input:
    response = get_response(user_input, personality=personality, model=model_choice)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", response))

# Display chat history
for speaker, text in st.session_state.history:
    st.write(f"**{speaker}:** {text}")

# Clear conversation button
if st.button("Clear Conversation"):
    st.session_state.history = []
    reset_chat()
    st.success("Conversation cleared!")
