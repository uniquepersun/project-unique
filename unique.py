import speech_recognition as sr
import google.generativeai as genai
from gtts import gTTS
from dotenv import load_dotenv
import os
import asyncio
import sounddevice as sd
from scipy.io.wavfile import read as wav_read
import numpy as np
from pydub import AudioSegment

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

async def convert_and_speak(text):
    try:
        language = 'en'
        myobj = gTTS(text=text, lang=language)
        with open("temp.mp3", "wb") as fp:
            myobj.write_to_fp(fp)
        with open("temp.mp3", "rb") as mp3_file:
            mp3_data = mp3_file.read()
        audio_segment = AudioSegment.from_mp3(mp3_data)
        with open("temp.wav", "wb") as wav_file:
            audio_segment.export(wav_file, format="wav")
        if os.path.exists("temp.wav"): 
            sample_rate, data = wav_read("temp.wav")
            data = np.asarray(data, dtype=np.float32)
            sd.play(data, samplerate=sample_rate)
            sd.wait()
        os.remove("temp.mp3")
        if os.path.exists("temp.wav"):
            os.remove("temp.wav")

    except Exception as e:
        print(f"Error during text-to-speech or audio playback: {e}")
    

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
        #("Say it out clearly, I couldn't get that.")
        return input("what's your input: ")

async def chatbot_logic(user_input):
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
            break
        response = chat_session.send_message(INPUT, stream=True)
        for chunk in response:
            await convert_and_speak(chunk.text)
            print(chunk.text)
async def main():
    await chatbot_logic("")

if __name__ == "__main__":
    asyncio.run(main())