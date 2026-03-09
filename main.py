# main.py

from voice.speech_to_text import off_speech_recognized as listen
from voice.text_to_speech import speak
from command.phase1_engine import phase1_engine
from core.command_executor import execute_command


def main():

    speak("Voice assistant started")

    while True:
        try:

            print("Listening...")
            user_text = listen()

            if not user_text:
                continue

            print("User:", user_text)

            result = phase1_engine(user_text)

            print("Intent:", result["intent"])
            print("Entities:", result["entities"])

            execute_command(result, user_text)

        except KeyboardInterrupt:

            speak("Stopping assistant")
            break

if __name__ == "__main__":
    main()