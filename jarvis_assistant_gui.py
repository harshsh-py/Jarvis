import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import threading
import datetime
import os
import sys
from Jarvis import speak, takecommand, wish, analyze_sentiment, smart_response, process_natural_language
from Jarvis import enhance_face_detection, sendEmail
import webbrowser
import pywhatkit as kit

class JarvisAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JARVIS AI Assistant")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1E1E1E')
        
        # Initialize variables
        self.listening = False
        self.running = True
        
        # Create main container
        self.create_gui()
        
    def create_gui(self):
        # Create main frame with dark theme
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=10)
        
        title_label = ttk.Label(
            title_frame,
            text="J.A.R.V.I.S",
            font=("Arial", 24, "bold")
        )
        title_label.pack()
        
        # Create split view
        self.create_split_view()
        
    def create_split_view(self):
        # Left panel - Status and Controls
        left_frame = ttk.Frame(self.main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Status section
        status_frame = ttk.LabelFrame(left_frame, text="System Status")
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack(pady=5)
        
        # Controls section
        controls_frame = ttk.LabelFrame(left_frame, text="Controls")
        controls_frame.pack(fill=tk.X, pady=5)
        
        # Buttons
        ttk.Button(controls_frame, text="Start Listening", command=self.start_listening).pack(fill=tk.X, pady=2)
        ttk.Button(controls_frame, text="Stop Listening", command=self.stop_listening).pack(fill=tk.X, pady=2)
        ttk.Button(controls_frame, text="Clear Display", command=self.clear_display).pack(fill=tk.X, pady=2)
        ttk.Button(controls_frame, text="Exit", command=self.exit_program).pack(fill=tk.X, pady=2)
        
        # Right panel - Main Display
        right_frame = ttk.Frame(self.main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Output display
        self.output_display = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            height=25,
            font=("Consolas", 10)
        )
        self.output_display.pack(fill=tk.BOTH, expand=True)
        
        # Command entry
        self.command_entry = ttk.Entry(right_frame)
        self.command_entry.pack(fill=tk.X, pady=5)
        self.command_entry.bind("<Return>", self.process_text_command)
        
    def update_status(self, message):
        self.status_label.config(text=message)
        self.output_display.insert(tk.END, f"Status: {message}\n")
        self.output_display.see(tk.END)
        
    def display_message(self, message):
        self.output_display.insert(tk.END, f"{message}\n")
        self.output_display.see(tk.END)
        
    def start_listening(self):
        if not self.listening:
            self.listening = True
            self.update_status("Listening...")
            threading.Thread(target=self.listen_loop, daemon=True).start()
            
    def stop_listening(self):
        self.listening = False
        self.update_status("Stopped listening")
        
    def clear_display(self):
        self.output_display.delete(1.0, tk.END)
        
    def exit_program(self):
        self.running = False
        self.listening = False
        self.root.quit()
        
    def process_text_command(self, event=None):
        command = self.command_entry.get().lower()
        self.command_entry.delete(0, tk.END)
        self.process_command(command)
        
    def process_command(self, query):
        self.display_message(f"You: {query}")
        
        # AI-enhanced response
        if query != "none":
            # Analyze sentiment
            sentiment_label, confidence = analyze_sentiment(query)
            smart_reply = smart_response(query)
            if smart_reply:
                speak(smart_reply)
                self.display_message(f"JARVIS: {smart_reply}")
            
            # Process commands
            if "open notepad" in query:
                npath = "C:\\Windows.old\\Windows\\notepad.exe"
                os.startfile(npath)
                self.display_message("JARVIS: Opening Notepad")
                
            elif "open whatsapp" in query:
                wpath = "C:\\Users\\Digital\\AppData\\Local\\WhatsApp\\whatsapp.exe"
                os.startfile(wpath)
                self.display_message("JARVIS: Opening WhatsApp")
                
            elif "open command prompt" in query:
                os.system("start cmd")
                self.display_message("JARVIS: Opening Command Prompt")
                
            elif "open spotify" in query:
                spath = "C:\\Users\\Digital\\AppData\\Roaming\\Spotify\\spotify.exe"
                os.startfile(spath)
                self.display_message("JARVIS: Opening Spotify")
                
            elif "open camera" in query:
                self.display_message("JARVIS: Opening camera with AI-enhanced face detection")
                threading.Thread(target=enhance_face_detection).start()
                
            elif "play music" in query:
                music_dir = "D:\\music"
                songs = os.listdir(music_dir)
                for song in songs:
                    if song.endswith('.mp3'):
                        os.startfile(os.path.join(music_dir, song))
                        self.display_message(f"JARVIS: Playing {song}")
                        break
                        
            elif "ip address" in query:
                from requests import get
                ip = get('https://api.ipify.org').text
                msg = f"Your IP address is {ip}"
                speak(msg)
                self.display_message(f"JARVIS: {msg}")
                
            elif "wikipedia" in query:
                self.display_message("JARVIS: Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                import wikipedia
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
                self.display_message(f"JARVIS: {results}")
                
            elif "open youtube" in query:
                webbrowser.open("www.youtube.com")
                self.display_message("JARVIS: Opening YouTube")
                
            elif "open instagram" in query:
                webbrowser.open("www.instagram.com")
                self.display_message("JARVIS: Opening Instagram")
                
            elif "open facebook" in query:
                webbrowser.open("www.facebook.com")
                self.display_message("JARVIS: Opening Facebook")
                
            elif "open stack overflow" in query:
                webbrowser.open("www.stackoverflow.com")
                self.display_message("JARVIS: Opening Stack Overflow")
                
            elif "open google" in query:
                speak("Sir, what should I search on Google for you?")
                self.display_message("JARVIS: What should I search on Google?")
                self.listening = True
                search_query = takecommand().lower()
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
                
            elif "send message" in query:
                kit.sendwhatmsg("+919818691425", "This is a test message", 
                               datetime.datetime.now().hour,
                               datetime.datetime.now().minute + 2)
                self.display_message("JARVIS: Message will be sent in 2 minutes")
                
            elif "play song on youtube" in query:
                kit.playonyt("see you again")
                self.display_message("JARVIS: Playing song on YouTube")
                
            elif "email to harsh" in query:
                try:
                    speak("What should I say?")
                    self.display_message("JARVIS: What should I say in the email?")
                    content = takecommand().lower()
                    to = "hs08072002@gmail.com"
                    sendEmail(to, content)
                    self.display_message("JARVIS: Email has been sent to Harsh")
                except Exception as e:
                    print(e)
                    self.display_message("JARVIS: Sorry, I am not able to send the email")
                    
            elif "turn off jarvis" in query or "goodbye" in query or "exit" in query:
                speak("Thanks for using me sir, have a good day!")
                self.display_message("JARVIS: Goodbye!")
                self.exit_program()
                
    def listen_loop(self):
        while self.listening and self.running:
            query = takecommand().lower()
            if query != "none":
                self.process_command(query)

def main():
    root = tk.Tk()
    app = JarvisAssistantGUI(root)
    # Initial greeting
    wish()
    root.mainloop()

if __name__ == "__main__":
    main()
