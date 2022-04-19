# Calendar Jarvis
Welcome to Calendar Jarvis project, where we could create our own "Jarvis" or "S!RI" , "AL3XA" , or "0K GOOGL3"

## **Prerequisites**
Before starting to contribute, make sure you are familiar with these tools:
  - Python

## Folders and files glossary:
  - `creds`: folder that contains token for google calendar API connection and credentials needed to generate the token
  - `.gitignore`: file that contains all file names that should not pushed to the remote repository (e.g :cache files, files that is being generated after runing the program, files that contains sensitive information like .env)
  - `main.py`: file that need to be executed/called to run this program
  - `engine.py`: file that contains all function needed to run the program 
  - `credmaker.py`: file that need to be run first to generate token
  - `intents`: folder that contains the dictionary of intents
  - `model`: folder that stores the pre-trained model and model saved from training
  - `note`: folder to store text file needed to create a note
  - `requirements.txt`: all library names that is being used in this web app


## How to Re-Create This Project

0. Clone this repo
1. Create new virtual environtment needed for the project. Use the library stored in `requirements.txt`
2. Get Google Calendar API credentials (usually stored in `.json` file)
3. Create new folder named **creds** and store the credentials there
4. Run the `cred_maker` and don't forget to adjust the credentials files naming or location
5. Adjust your intents/command (if needed)

## Commands used

0. **misheard** : to tell you that he didn't understand what you said
1. **Greeting** : to greet you (yeah of course); you can say Hi, Hello, or Good Morning and he (or she if you want to) will reply
2. **Create Note** : write a note based on what you say, can be useful if your hands is full
3. **Add Event** : create an event and connect it with your google calendar
4. **Show Agenda** : tell your today's agenda