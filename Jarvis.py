import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import time
import pyjokes






engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voices', voices[1].id)

#text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


#to covert voice to text
def  takecommand():
    r =sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source,timeout=5, phrase_time_limit=5)

    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")

    except Exception as e:
        speak("Say that again please.")
        return "none"
    return query

#to wish
def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0  and hour<=12:
        speak("good morning")
    elif hour>12  and hour<18:
        speak("good afternoon")
    else:
        speak("good evening")
    speak("I am Jarvis sir, please tell me, how can i help you")

#to send mail
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('sharmaharsh.08072002@gmail.com', 'Sharma@1425')
    server.sendmail('sharmaharsh.08072002@gmail.com', to, content)
    server.close()



if __name__== "__main__":
    wish()
    while True:
    # if 1:


        query = takecommand().lower()

        #logic building for task

        if "open notepad" in query:
            npath = "C:\\Windows.old\\Windows\\notepad.exe"
            os.startfile(npath)

        elif "Open whatsapp" in query:
            wpath = "C:\\Users\\Digital\\AppData\\Local\\WhatsApp\whatsapp.exe"
            os.startfile(wpath)

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "open spotify" in query:
            spath = "C:\\Users\\Digital\\AppData\\Roaming\\Spotify\spotify.exe"
            os.startfile(spath)


        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k==27:
                    break;
            cap.release()
            cv2.destroyAllWindows()

        elif "play music" in query:
            music_dir = "D:\\music"
            songs = os.listdir(music_dir)
            #rd = random.choice(songs)
            for song in songs:
                if song.endswith('.mp3'):
                    os.startfile(os.path.join(music_dir, song))

        elif "ip address" in query:
            ip = get ('https://api.ipify.org').text
            speak(f"your IP address is {ip}")

        elif "wikipedia" in query:
            speak("searching wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            speak(results)
            #print(results)

        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")

        elif "open instagram" in query:
            webbrowser.open("www.instagram.com")

        elif "open facebook" in query:
            webbrowser.open("www.facebook.com")

        elif "open stack overflow" in query:
            webbrowser.open("www.stackoverflow.com")

        elif "open google" in query:
            speak("sir, what should I search on google for you?")
            cm = takecommand().lower()
            webbrowser.open(f"{cm}")

        elif "send message" in query:
            kit.sendwhatmsg("+919818691425", "this is test msg",22,29)

        elif "play song on youtube" in query:
            kit.playonyt("see you again")

        elif " email to harsh" in query:
            try:
                speak("what should I say?")
                content = takecommand().lower()
                to = "hs08072002@gmail.com"
                sendEmail(to,content)
                speak("Email has been sent to harsh")

            except Exception as e:
                print(e)
                speak("sorry sir, I am not able to send the mail to harsh")

        elif "No thanks" in query:
            speak("thanks for using me sir, have a good day!")
            sys.exit()

        

        speak("sir, do you have another work?")

        






        




    