import os
import google.generativeai as genai
import streamlit as st

# Load API key from environment (ensure GEMINI_API_KEY is correctly set in your environment)
GEMINI_API_KEY = "***********************************" # Replace with your actual API key or ensure it's loaded from env
API_KEY = GEMINI_API_KEY
genai.configure(api_key=API_KEY)

def call_gemini(prompt: str, model_name: str = "gemini-2.5-flash") -> str:
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.set_page_config(page_title="Chatbot", layout="centered")
st.title("🧠 Chatbot Interface")

# Initialize session state for chat history and input
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

def submit():
    user_input = st.session_state.user_input
    if user_input:
        bot_reply = call_gemini(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", bot_reply))
        st.session_state.user_input = ""  # This is safe inside a callback

# Chat input with on_change callback
st.text_input("You:", key="user_input", on_change=submit)

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧍 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")
