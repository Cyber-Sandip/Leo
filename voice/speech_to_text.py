import os
import speech_recognition as sr
from colorama import Style,Fore,init
from googletrans import Translator
# for vosk
import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
# 





init(autoreset=True)

def check_device_status():
    response = os.system("ping -n 1 8.8.8.8 > nul")
 
    
    if response == 0:
        print("Device is ONLINE")
    else:
        print("Device is OFFLINE")




def on_speech_recognized():
    r=sr.Recognizer()
    r.dynamic_energy_threshold=False
    r.energy_threshold = 33000
    r.dynamic_energy_adjustment_damping=0.0012
    r.dynamic_energy_ratio=1.0
    r.pause_threshold=0.4
    r.operation_timeout= None
    r.pause_threshold=0.4
    r.non_speaking_duration=0.4
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            print(Fore.LIGHTBLUE_EX + "Listning.......", end="", flush=True)
            try:
                audio=r.listen(source,timeout=None)
                print("\r"+Fore.LIGHTGREEN_EX+"Recognising........" ,end="", flush=True)
                query=r.recognize_google(audio).lower()
                if query:
                    # query=translate_hi_to_en(query)
                    print("\r"+Fore.GREEN+f"Query :{query}")
                    return query
                else:
                    return ""
            except sr.UnknownValueError:
                query=""
            finally:
                print("\r",end="",flush=True)
                os.system("cls" if os.name == "nt" else "clear")


# vosk offline speech recognition

model = Model("vosk-model-small-en-in-0.4")
q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def off_speech_recognized():
    recognizer = KaldiRecognizer(model, 16000)

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=callback
    ):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                return json.loads(recognizer.Result())["text"]
   


# if __name__ =="__main__":
#     while True:
#         command=off_speech_recognized()
#         print(command)