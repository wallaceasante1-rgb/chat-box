import streamlit as st
from chatbot.logic import get_response

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("Chatbox App")

user_input = st.text_input("You:", "")

if user_input:
    st.session_state["messages"].append(("You", user_input))
    bot_response = get_response(user_input)
    st.session_state["messages"].append(("Bot", bot_response))

for sender, msg in st.session_state["messages"]:
    st.write(f"**{sender}:** {msg}")

