import os
import webbrowser
import datetime
import pyautogui
import psutil


from voice.text_to_speech import speak
from core.app_launcher import open_app


def execute_command(result, text):

    intent = result["intent"]
    entities = result["entities"]

    # OPEN APPLICATION
    if intent == "OPEN_APP":

        app = entities.get("app")

        # First try automatic app launcher
        if open_app(app):
            speak(f"Opening {app}")
            return

        # Web apps fallback
        if app == "youtube":
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif app == "whatsapp":
            speak("Opening WhatsApp Web")
            webbrowser.open("https://web.whatsapp.com")

        elif app == "google":
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
                 
        else:
            speak("Application not found")


    

    elif intent == "OPEN_CAMERA":
        speak("Opening camera")
        os.system("start microsoft.windows.camera:")

    elif intent == "VOLUME_UP":
        speak("Increasing volume")

        for _ in range(5):
            pyautogui.press("volumeup")

    elif intent == "VOLUME_DOWN":
        speak("Decreasing volume")
        for _ in range(5):
            pyautogui.press("volumedown")


    elif intent == "RESTART":
        speak("Restarting computer")
        os.system("shutdown /r /t 1")


    elif intent == "SHUTDOWN":
        speak("Shutting down system")
        os.system("shutdown /s /t 1")


    elif intent == "SCREENSHOT":
        speak("Taking screenshot")
        img = pyautogui.screenshot()
        img.save("screenshot.png")

    # GET TIME
    elif intent == "GET_TIME":
        time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {time}")

    # EXIT
    elif intent == "EXIT":

        speak("Goodbye")
        exit()

    else:
        speak("Sorry, I did not understand")