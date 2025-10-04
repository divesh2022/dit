import os
import google.generativeai as genai
import streamlit as st

# Configure Gemini API
API_KEY = "AIzaSyDFUN1Mb0BOiawDREOim3M8S25RonQFxOM"
if not API_KEY:
    st.error("API key not found. Please set GEMINI_API_KEY in your environment.")
    st.stop()
genai.configure(api_key=API_KEY)

# Gemini call function
def call_gemini(prompt: str, model_name: str = "gemini-2.5-flash") -> str:
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Triage classification logic
def categorize(symptoms: str) -> str:
    symptoms_lower = symptoms.lower()
    severe_keywords = [
        "chest pain", "shortness of breath", "severe bleeding", "loss of consciousness",
        "stroke", "seizure", "blue lips", "confusion", "high fever", "severe abdominal pain"
    ]
    moderate_keywords = [
        "fever", "cough", "headache", "fatigue", "sore throat", "body ache",
        "nausea", "vomiting", "diarrhea", "mild abdominal pain"
    ]
    if any(word in symptoms_lower for word in severe_keywords):
        return "🔴 Severe"
    elif any(word in symptoms_lower for word in moderate_keywords):
        return "🟡 Moderate"
    else:
        return "🔵 Safe"

# Streamlit UI setup
st.set_page_config(page_title="Medical Triage Chatbot", layout="centered")
st.title("🚑 Medical Triage Chatbot")

# Session state initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "user_data" not in st.session_state:
    st.session_state.user_data = {"name": "", "phone": "", "address": "", "symptoms": "", "category": ""}

# Chat submission logic
def submit():
    user_input = st.session_state.user_input
    if user_input:
        bot_prompt = f"""You're a medical triage assistant. Cross-question the user based on these symptoms: "{user_input}".
        Ask follow-up questions to clarify severity, duration, and any red-flag indicators. Be concise and medically focused."""
        bot_reply = call_gemini(bot_prompt)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", bot_reply))
        st.session_state.user_input = ""

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧍 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")

# Input bar at bottom
st.text_input("Type your message here:", key="user_input", on_change=submit)

# Collect final user details
st.subheader("📝 Final Details")
st.session_state.user_data["name"] = st.text_input("Name")
st.session_state.user_data["phone"] = st.text_input("Phone Number")
st.session_state.user_data["address"] = st.text_area("Address")
st.session_state.user_data["symptoms"] = st.text_area("Describe your symptoms")

# Submit and categorize
if st.button("Submit Details"):
    category = categorize(st.session_state.user_data["symptoms"])
    st.session_state.user_data["category"] = category

    st.success("✅ Final Summary")
    st.write({
        "Name": st.session_state.user_data["name"],
        "Phone": st.session_state.user_data["phone"],
        "Address": st.session_state.user_data["address"],
        "Urgency Category": category
    })
