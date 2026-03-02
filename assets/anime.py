import pyttsx3
def say(text):
    engine=pyttsx3.init()
    engine.setProperty('rate',140)  # talk speed increase or decrease
    engine.say(text)
    engine.runAndWait()

