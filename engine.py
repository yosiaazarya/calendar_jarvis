import speech_recognition
import pyttsx3 as tts
from googleapiclient.discovery import build
import pickle
from datetime import datetime, timedelta
import datefinder
import dateutil.parser

# connect with google API service
credentials = pickle.load(open("creds/token.pkl", "rb"))
service = build("calendar", "v3", credentials=credentials)

# speech recognizer
recognizer = speech_recognition.Recognizer()

# speaker
speaker = tts.init()
speaker.setProperty('rate', 110)

# greeting
def hello():
    speaker.say("Hello Sir, what can I do for you?")
    speaker.runAndWait()

# function to create a note
def create_note():
    global recognizer

    speaker.say("what do you want to write on your note?")
    speaker.runAndWait()

    done = False
    
    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                # log
                print("What do you want to write on your note?")
                print("Speak")
                # capture the spoken command
                audio = recognizer.listen(mic)
                # translate into text
                note = recognizer.recognize_google(audio)
                note = note.lower()
                # print the note as a log
                print(note)
                speaker.say("Choose a filename!")
                speaker.runAndWait()

                # log
                print("What is your file name?")
                print("speak")
                # naming the note
                audio = recognizer.listen(mic)
                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
                print(filename)
                # saving the note
                with open(f"note/{filename}", "w") as f:
                    f.write(note)
                    
                    # the function finish here
                    done = True
                    speaker.say(f"I succesfully created the {filename} note")
                    speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            print("try again")
            recognizer = speech_recognition.Recognizer()
            speaker.say("I don't understand, please try again!")
            speaker.runAndWait()

# funtions to create an event on google calendar
def _create_event(start_time_str, summary, duration=1, description=None, location=None):
    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)
    
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Bangkok',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Bangkok',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return service.events().insert(calendarId='primary', body=event).execute()

def add_event():
    global recognizer

    speaker.say("What is the event name?")
    speaker.runAndWait()

    done = False
    
    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                # log
                print("What is the event's name?")
                print("speak")
                audio = recognizer.listen(mic)

                summary = recognizer.recognize_google(audio)
                summary = summary.lower()
                print(summary)
                speaker.say("When will the event started?")
                speaker.runAndWait()

                # log
                print("When will the event started?")
                print("speak")
                audio = recognizer.listen(mic)
                start = recognizer.recognize_google(audio)
                print(start)
                speaker.say(f"adding {summary} on {start} to google calendar")

                try:
                    _create_event(start, summary)
                    done = True
                    speaker.say(f"I succesfully created the event on Google Calendar")
                    speaker.runAndWait()
                except:
                    recognizer = speech_recognition.Recognizer()
                    print("try again")
                    speaker.say("Can not process your request, please try again")
                    speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            print("try again")
            speaker.say("I don't understand, please try again!")
            speaker.runAndWait()

# function to show agenda / events on google calendar
def show_agenda():
    speaker.say("The items on your google calendar agenda are the following")
    now = datetime.utcnow().isoformat() + 'Z'
    end = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,timeMax=end,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        speaker.say('No upcoming events found.')
    for num, event in enumerate(events):
        start = event['start'].get('dateTime', event['start'].get('date'))
        parsed_start = dateutil.parser.parse(start)
        end = event['end'].get('dateTime', event['end'].get('date'))
        parsed_end = dateutil.parser.parse(end)
        speaker.say(f"{num+1} {event['summary']} on {parsed_start.strftime('%#I %p')} until {parsed_end.strftime('%#I %p')}")
    speaker.runAndWait()





