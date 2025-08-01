import tkinter as tk
from tkinter import ttk, scrolledtext
import customtkinter as ctk
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
import threading
import pystray
from PIL import Image, ImageTk
import nltk
from nltk.chat.util import Chat, reflections
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import wave
import pyaudio

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis AI Assistant")
        self.root.geometry("800x600")
        
        # Initialize the speech engine
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        
        # Create GUI elements
        self.create_gui()
        
        # Initialize chat patterns
        self.initialize_chat_patterns()
        
        # Create system tray icon
        self.create_tray_icon()
        
        # Variable to track if listening
        self.is_listening = False
        
    def create_gui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create chat display
        self.chat_display = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=70, height=20)
        self.chat_display.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Create input field
        self.input_field = ttk.Entry(main_frame, width=60)
        self.input_field.grid(row=1, column=0, pady=10)
        
        # Create buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2)
        
        ttk.Button(buttons_frame, text="Send", command=self.send_message).pack(side=tk.LEFT, padx=5)
        self.voice_button = ttk.Button(buttons_frame, text="🎤 Voice", command=self.toggle_voice_input)
        self.voice_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Minimize to Tray", command=self.minimize_to_tray).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to send message
        self.input_field.bind("<Return>", lambda e: self.send_message())
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var)
        status_bar.grid(row=3, column=0, columnspan=2, pady=5)

    def initialize_chat_patterns(self):
        self.patterns = [
            (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey! How can I help you?']),
            (r'how are you', ['I am doing well, thank you!', 'I am functioning perfectly!']),
            (r'what is your name', ['I am Jarvis, your AI assistant.', 'My name is Jarvis!']),
            (r'bye|goodbye', ['Goodbye!', 'See you later!', 'Have a great day!']),
            (r'what can you do', ['I can help you with various tasks like:\n- Opening applications\n- Searching the web\n- Playing music\n- Getting information\n- Sending emails\nJust ask me what you need!']),
            # Add more patterns here
        ]
        self.chatbot = Chat(self.patterns, reflections)

    def create_tray_icon(self):
        # Load the Jarvis icon
        icon_image = Image.open('jarvis_icon.png')
        self.icon = pystray.Icon(
            "Jarvis",
            icon_image,
            menu=pystray.Menu(
                pystray.MenuItem("Show", self.show_window),
                pystray.MenuItem("Exit", self.exit_application)
            )
        )
        
    def show_window(self, icon=None):
        self.icon.stop()
        self.root.deiconify()
        
    def minimize_to_tray(self):
        self.root.withdraw()
        threading.Thread(target=self.icon.run, daemon=True).start()
        
    def exit_application(self, icon=None):
        if icon:
            icon.stop()
        self.root.quit()

    def speak(self, audio):
        self.chat_display.insert(tk.END, f"Jarvis: {audio}\n")
        self.chat_display.see(tk.END)
        self.engine.say(audio)
        self.engine.runAndWait()

    def send_message(self):
        user_input = self.input_field.get().strip()
        if user_input:
            self.chat_display.insert(tk.END, f"You: {user_input}\n")
            self.input_field.delete(0, tk.END)
            self.process_command(user_input.lower())
            self.chat_display.see(tk.END)

    def toggle_voice_input(self):
        if not self.is_listening:
            self.is_listening = True
            self.voice_button.configure(text="🔴 Stop")
            self.status_var.set("Listening...")
            threading.Thread(target=self.listen_voice, daemon=True).start()
        else:
            self.is_listening = False
            self.voice_button.configure(text="🎤 Voice")
            self.status_var.set("Ready")

    def listen_voice(self):
        while self.is_listening:
            try:
                with sr.Microphone() as source:
                    self.status_var.set("Listening...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    self.status_var.set("Processing...")
                    text = self.recognizer.recognize_google(audio, language='en-in')
                    self.chat_display.insert(tk.END, f"You: {text}\n")
                    self.process_command(text.lower())
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                print(f"Error: {str(e)}")
                continue

    def process_command(self, query):
        # First try to get a response from the chatbot
        try:
            response = self.chatbot.respond(query)
            if response:
                self.speak(response)
                return
        except:
            pass

        # Process existing commands
        if "open notepad" in query:
            npath = "C:\\Windows\\notepad.exe"
            os.startfile(npath)
            self.speak("Opening Notepad")

        elif "open whatsapp" in query:
            webbrowser.open("https://web.whatsapp.com")
            self.speak("Opening WhatsApp Web")

        elif "open command prompt" in query:
            os.system("start cmd")
            self.speak("Opening Command Prompt")

        elif "open camera" in query:
            self.speak("Opening camera")
            threading.Thread(target=self.open_camera, daemon=True).start()

        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            self.speak(f"Your IP address is {ip}")

        elif "wikipedia" in query:
            self.speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                self.speak("According to Wikipedia")
                self.speak(results)
            except:
                self.speak("Sorry, I couldn't find that on Wikipedia")

        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com")
            self.speak("Opening YouTube")

        elif "open google" in query:
            self.speak("What should I search on Google for you?")
            search_query = self.wait_for_voice_input()
            if search_query:
                url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(url)
                self.speak(f"Searching Google for {search_query}")

        elif "play song on youtube" in query:
            self.speak("What song would you like to play?")
            song = self.wait_for_voice_input()
            if song:
                self.speak(f"Playing {song} on YouTube")
                kit.playonyt(song)

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            self.speak(joke)

        elif "exit" in query or "quit" in query or "goodbye" in query:
            self.speak("Goodbye! Have a great day!")
            self.root.after(2000, self.exit_application)
        
        else:
            self.speak("I'm not sure how to help with that. Could you please rephrase or try another command?")

    def wait_for_voice_input(self):
        try:
            with sr.Microphone() as source:
                self.status_var.set("Listening for specific input...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio, language='en-in')
                return text.lower()
        except:
            return None

    def open_camera(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Jarvis Camera', frame)
                if cv2.waitKey(1) & 0xFF == 27:  # Press Esc to close
                    break
        cap.release()
        cv2.destroyAllWindows()

def main():
    root = tk.Tk()
    app = JarvisGUI(root)
    root.protocol("WM_DELETE_WINDOW", lambda: app.minimize_to_tray())
    root.mainloop()

if __name__ == "__main__":
    main()
