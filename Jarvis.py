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
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from transformers import pipeline
import torch
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')






engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# Set voice properties for better clarity
engine.setProperty('rate', 150)    # Speed of speech
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
engine.setProperty('voice', voices[0].id)  # Use the first voice (usually male voice)

#text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


#to convert voice to text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source, duration=0.5)
        # Increase pause threshold for better sentence detection
        r.pause_threshold = 0.8
        # Energy threshold for detecting speech
        r.energy_threshold = 300
        # Adjust phrase threshold for better recognition
        r.phrase_threshold = 0.3
        audio = r.listen(source, timeout=7, phrase_time_limit=5)

    try:
        print("Recognizing.....")
        # Use generic English for better recognition
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}")

    except sr.UnknownValueError:
        speak("I couldn't understand what you said. Could you please repeat?")
        return "none"
    except sr.RequestError:
        speak("Sorry, there seems to be a problem with the speech recognition service.")
        return "none"
    except Exception as e:
        print(f"Error: {str(e)}")
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

# Initialize AI models
sentiment_analyzer = pipeline("sentiment-analysis")
question_answerer = pipeline("question-answering")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def analyze_sentiment(text):
    """Analyze the sentiment of user's speech"""
    analysis = sentiment_analyzer(text)
    return analysis[0]['label'], analysis[0]['score']

def smart_response(query):
    """Generate more contextual responses based on user's query"""
    blob = TextBlob(query)
    # Get the sentiment
    sentiment = blob.sentiment.polarity
    
    if sentiment > 0:
        return "I'm glad you're feeling positive! "
    elif sentiment < 0:
        return "I notice you might be feeling down. How can I help? "
    return ""

def enhance_face_detection():
    """Enhanced face detection with AI capabilities"""
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
        cv2.imshow('AI Enhanced Face Detection', frame)
        k = cv2.waitKey(50)
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

def process_natural_language(text):
    """Process text using NLP techniques"""
    tokens = word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    return pos_tags

if __name__== "__main__":
    wish()
    while True:
    # if 1:


        query = takecommand().lower()
        
        # AI-enhanced response
        if query != "none":
            # Analyze sentiment
            sentiment_label, confidence = analyze_sentiment(query)
            smart_reply = smart_response(query)
            if smart_reply:
                speak(smart_reply)
            
            # Process natural language
            pos_tags = process_natural_language(query)
            
        #logic building for task

        if "open notepad" in query:
            npath = "C:\\Windows.old\\Windows\\notepad.exe"
            os.startfile(npath)

        elif "Open whatsapp" in query:
            wpath = "C:\\Users\\Digital\\AppData\\Local\\WhatsApp\\whatsapp.exe"
            os.startfile(wpath)

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "open spotify" in query:
            spath = "C:\\Users\\Digital\\AppData\\Roaming\\Spotify\\spotify.exe"
            os.startfile(spath)


        elif "open camera" in query:
            speak("Opening camera with AI-enhanced face detection")
            enhance_face_detection()

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

        elif "No thanks" in query or "turn off jarvis" in query or "goodbye jarvis" in query:
            speak("Thanks for using me sir, have a good day! Turning off now.")
            sys.exit()

        speak("sir, do you have another work?")

        






        




    