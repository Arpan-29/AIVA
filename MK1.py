import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import smtplib
import datetime
import wikipedia
import time

from LoginCredentials import email, password
from keyboard_mouse import click, rightClick, move, press, release, pressOnce, write
import keyboard_mouse

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

from DLC import get_response

typing = False
writeLog = ""

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

        volume = engine.getProperty('volume')
        print(volume)

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

        response, tag = get_response(query)

        if tag == "start writing":
            typing = True

            speak(response)
            print(f"Aiva: {response}")
            
            continue

        elif tag == "stop writing":
            typing = False

            speak(response)
            print(f"Aiva: {response}")

            continue

        if typing:

            if tag == "delete": 
        
                pressOnce('backspace')
                writeLog = writeLog[:-1]

                while len(writeLog) > 0 and writeLog[-1] != ' ':
                    pressOnce('backspace')
                    writeLog = writeLog[:-1]

            elif query.lower() != "none":
                writeLog += query + ". "
                write(query + ". ")

            continue

        elif tag == "wikipedia":
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

        elif tag == "shut down":
            end = True

            speak(response)
            print(f"Aiva: {response}")

            # pressOnce('win')
            # move(20, 1079)
            click(20, 1079)
            click(725, 954)
            click(730, 873)

        elif tag == "open word":
            speak(response)
            print(f"Aiva: {response}")

            move(20, 1079)
            click(20, 1079)

            write('word')

            pressOnce('enter')
            time.sleep(2)
            # move(21, 1079)
            rightClick(425, 1051)
            click(430, 909)
            pressOnce('enter')

            continue

        speak(response)
        print(f"Aiva: {response}")