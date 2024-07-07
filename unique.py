import speech_recognition as sr
import google.generativeai as genai
from gtts import gTTS
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def speak(text):
    tts = gTTS(text=text, lang="en")
    tts.save("output.mp3")
    os.system("output.mp3")

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
        speak("Say it out clearly, I couldn't get that.")
        return input("what's your input: ")

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
   history=[]
)

while True:
    INPUT = get_user_input()
    if "exit chat" in INPUT:
        print("Goodbye!")
        speak("Goodbye!")
        break
    response = chat_session.send_message(INPUT, stream=True)
    for chunk in response:
        print(chunk.text)
    speak(chunk.text)
    
