import os
import webbrowser
import datetime
import pyautogui

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

        elif app == "notepad":
            speak("Opening Notepad")
            os.system("notepad")

        elif app == "calculator":
            speak("Opening Calculator")
            os.system("calc")

        else:
            speak("Application not found")

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