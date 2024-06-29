import speech_recognition as sr
import pyttsx3
# import gTTS
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
                

def get_user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("I heard: " + text)
        return text
    except sr.UnknownValueError:
        print("Say it out clearly, I couldn't get that.")
        return input("Speak again or type your input: ")

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)
chat_session = model.start_chat(
  history=[
  ]
)
speak("Hello, I am Gemini. How can I help you today?")
INPUT = get_user_input()
response = chat_session.send_message(INPUT, stream=True)

for chunk in response:
  print(chunk.text)
  speak(chunk.text)