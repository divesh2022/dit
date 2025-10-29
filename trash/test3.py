import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import test1 as t1  # Your module storing the API key

# Optional: gTTS fallback
from gtts import gTTS
import playsound
import os

# 🔐 Configure Gemini API
genai.configure(api_key=t1.Api_key)
model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")

# 🔊 Initialize pyttsx3 (offline TTS)
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Try voices[1] or [2] if needed

# 🔁 Toggle between TTS engines
USE_GTTS = False  # Set to True to use gTTS instead of pyttsx3

def speak(text):
    """Speak and print the chatbot's response."""
    print("🤖 Chatbot:", text)
    if USE_GTTS:
        try:
            tts = gTTS(text=text, lang='en')
            tts.save("response.mp3")
            playsound.playsound("response.mp3")
            os.remove("response.mp3")
        except Exception as e:
            print("gTTS error:", e)
            print("Falling back to text only.")
    else:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("pyttsx3 error:", e)
            print("Falling back to text only.")

def listen():
    """Capture voice input and convert to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=20)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Let's try again.")
            return None
    try:
        command = recognizer.recognize_google(audio)
        print("🗣️ You said:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return None
    except sr.RequestError:
        speak("Speech service is unavailable.")
        return None

def chat_with_gemini(prompt):
    """Send prompt to Gemini and return response."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini error:", e)
        return "Sorry, I couldn't process that."

# 🚀 Main Loop
if __name__ == "__main__":
    speak("Hello! I'm your voice assistant. Say something or say 'exit' to quit.")
    while True:
        user_input = listen()
        if user_input:
            if user_input.lower() in ["exit", "quit", "stop"]:
                speak("Goodbye!")
                break
            reply = chat_with_gemini(user_input)
            speak(reply)