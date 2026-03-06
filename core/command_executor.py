import os
import webbrowser
import datetime

from voice.text_to_speech import speak


def execute_command(result, text):

    intent = result["intent"]
    entities = result["entities"]

    # OPEN APPLICATION
    if intent == "OPEN_APP":

        app = entities.get("app")

        if app == "chrome":
            speak("Opening Chrome")
            webbrowser.open("https://www.google.com")

        elif app == "notepad":
            speak("Opening Notepad")
            os.system("notepad")

        elif app == "calculator":
            speak("Opening Calculator")
            os.system("calc")

        else:
            speak("Application not supported")

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