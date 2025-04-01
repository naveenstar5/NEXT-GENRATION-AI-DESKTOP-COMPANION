import pyttsx3
import speech_recognition as sr
import os
import subprocess as sp
import keyboard
import threading
import webbrowser
import wikipedia
import requests
import pywhatkit as kit
from datetime import datetime
from random import choice
import re
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, send_email

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.0)
engine.setProperty('rate', 200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

# User and Assistant Names
USER = "Naveen"
HOSTNAME = "CHITTI"

random_text = [
    "Cool, I'm on it, sir.",
    "Okay sir, I'm working on it.",
    "Just a second, sir."
]

# Speak function
def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

# Greeting function
def greet_me():
    """Greet the user based on the time of day."""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good morning, {USER}!")
    elif 12 <= hour < 16:
        speak(f"Good afternoon, {USER}!")
    elif 16 <= hour < 19:
        speak(f"Good evening, {USER}!")
    else:
        speak(f"Hello, {USER}!")

    speak(f"I am {HOSTNAME}. How may I assist you?")

# Start/Stop Listening Hotkeys
listening = False

def start_listening():
    global listening
    listening = True
    print("Started listening")

def pause_listening():
    global listening
    listening = False
    print("Stopped listening")

keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)
threading.Thread(target=lambda: keyboard.wait(), daemon=True).start()

# Take voice command
def take_command():
    """Listen to the user's command and recognize speech."""
    if not listening:
        return "None"

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")

        if "stop" in query or "exit" in query:
            speak("Goodbye sir, have a great day!")
            exit()

        speak(choice(random_text))
        return query.lower()

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Please say that again.")
        return "None"
    except sr.RequestError:
        print("Speech recognition service is down. Try again later.")
        return "None"

# Validate email address
def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email)

# Main execution
if __name__ == "__main__":
    greet_me()
    while True:
        if listening:
            query = take_command()

            if query and "how are you" in query:
                speak("I am absolutely fine, sir. What about you?")

            elif "open command prompt" in query:
                speak("Opening Command Prompt")
                os.system("start cmd")

            elif "open camera" in query:
                speak("Opening Camera, sir")
                sp.run("start microsoft.windows.camera:", shell=True)

            elif "open notepad" in query:
                speak("Opening Notepad, sir")
                os.system("notepad")

            elif "open brave" in query:
                speak("Opening Brave Browser")
                os.system("start brave")

            elif "open firefox" in query:
                speak("Opening Firefox")
                os.system("start firefox")

            elif "open facebook" in query:
                speak("Opening Facebook")
                webbrowser.open("https://www.facebook.com/")

            elif "ip address" in query:
                ip_address = find_my_ip()
                speak(f"Your IP address is {ip_address}")
                print(f"Your IP address is {ip_address}")

            elif "open youtube" in query:
                speak("What do you want to play on YouTube?")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak("What do you want to search on Google?")
                search_query = take_command().lower()
                search_on_google(search_query)

            elif "open wikipedia" in query:
                speak("What do you want to search on Wikipedia?")
                search_query = take_command().lower()
                result = search_on_wikipedia(search_query)
                speak(result)
                print(result)

            elif "send an email" in query:
                try:
                    speak("Whom should I send the email to?")
                    receiver_email = take_command().replace(" ", "").lower() + "@gmail.com"

                    if not is_valid_email(receiver_email):
                        speak("Invalid email address. Please try again.")
                        continue

                    speak("What is the subject?")
                    subject = take_command().capitalize()

                    speak("What is the message?")
                    message = take_command().capitalize()

                    if send_email(receiver_email, subject, message):
                        speak("I have sent the email, sir.")
                        print("✅ Email sent successfully!")
                    else:
                        speak("Something went wrong. Please check the error log.")
                        print("❌ Error sending email.")

                except Exception as e:
                    speak("Sorry, I couldn't send the email.")
                    print(f"❌ Email Error: {e}")
