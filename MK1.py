import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import smtplib
import datetime
import wikipedia

from LoginCredentials import email, password

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

from DLC import get_response


def speak(sentence):

    engine.say(sentence)
    engine.runAndWait()
    

def greetings():

    hr = int(datetime.datetime.now().hour)

    if hr >= 5 and hr < 12:
        speak("Good Morning!")

    elif hr >= 12 and hr < 17:
        speak("Good Afternoon!")

    else :
        speak("Good Evening!")

    speak("I am Aiva. How may I help you?")


def takeCommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
    
        r.pause_threshold = 1

        print("Listening....")
        audio = r.listen(source)

    try:
        
        print("Recognizing....")
        query = r.recognize_google(audio, language = 'en-in')
        print(f"User said: {query} \n")

    except Exception as e:

        print("Couldn't get that. Please try again!")
        return "None"

    return query


def sendEmail(to, content):

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(email, password)
    server.sendmail(email, to, content)
    server.close()

if __name__ == "__main__":

    greetings()
    end = False

    while not end:

        query = takeCommand().lower()

        if query == "None":
            continue

        response, tag = get_response(query)

        if tag == "wikipedia":
            print("Seaching Wikipedia...")

            speak("What do you want to search about?")
            searchQuery = takeCommand().lower()
            
            try:
                response += wikipedia.summary(searchQuery, sentences = 2)
            except:
                response = "Couldn't find any matches."

        elif tag == "open youtube":
            webbrowser.open("youtube.com")

        elif tag == "open google":
            webbrowser.open("google.com")

        elif tag == "play music":
            musicDir = "D:\\Arpan\\Songs"
            songs = os.listdir(musicDir)
            #print(songs)
            os.startfile(os.path.join(musicDir, songs[0]))

        elif tag == "time":
            timeResponse = datetime.datetime.now().strftime("%H:%M:%S")
            
            response += timeResponse

        elif tag == "open steam":
            path = "C:\\Program Files (x86)\\Steam\\Steam.exe"
            os.startfile(path)

        elif tag == "send email":
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "arpsin29@gmail.com"
                sendEmail(to, content)
                response += "Email has been sent."

            except Exception as e:
                print(e)
                response += "Sorry, your email could not be sent."

        elif tag == "goodbye":
            end = True

        speak(response)
        print(f"Aiva: {response}")