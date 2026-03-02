import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer

model = Model("vosk-model-small-en-in-0.4")
q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def Off_recognizer():
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
                result = json.loads(recognizer.Result())["text"]
                print(result)
                return result


if __name__ =="__main__":
    while True:
       command= Off_recognizer()
       print(command)
