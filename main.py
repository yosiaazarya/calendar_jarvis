from neuralintents import GenericAssistant
import speech_recognition
from os import path
from engine import *

# speech recognizer
recognizer = speech_recognition.Recognizer()

# mapping for the commands
mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_event": add_event,
    "show_agenda": show_agenda
}

# the brain
assistant = GenericAssistant('intents/intents.json', intent_methods=mappings)

# Using saved trained model if there is any
if path.exists('model/trained_model.h5'):
    assistant.load_model(model_name='model/trained_model')
else:
    assistant.train_model()
    assistant.save_model(model_name='model/trained_model')
print("Welcome to Jarvis Calendar!")
# running the program
while True:
    try:
        with speech_recognition.Microphone() as mic:
            # log
            print("speak")
            audio = recognizer.listen(mic)
            message = recognizer.recognize_google(audio)
            message = message.lower()
            # print our spoken command
            print(message)
            try: 
                assistant.request(message)
            except:
                print("try again")
            # re-listen our new command
            recognizer = speech_recognition.Recognizer()
    
    except speech_recognition.UnknownValueError:
        print("try again")
        # re-listen our new command
        recognizer = speech_recognition.Recognizer()

