import tkinter as tk
from tkinter import ttk, scrolledtext
import pyttsx3
from PIL import Image, ImageTk
import threading
import Jarvis
import os
from datetime import datetime
import time

class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JARVIS AI Assistant")
        self.root.geometry("1000x600")
        self.root.configure(bg='#1E1E1E')
        
        # Configure styles
        self.configure_styles()
        
        # Create main container
        self.main_frame = ttk.Frame(self.root, padding="10", style='Dark.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create left panel for status
        self.create_left_panel()
        
        # Create right panel for interaction
        self.create_right_panel()
        
        # Initialize variables
        self.listening = False
        self.running = True
        
    def configure_styles(self):
        # Configure ttk styles
        style = ttk.Style()
        style.configure('Dark.TFrame', background='#1E1E1E')
        style.configure('Status.TLabel', 
                       background='#2D2D2D',
                       foreground='#FFFFFF',
                       font=('Arial', 10))
        style.configure('Title.TLabel',
                       background='#1E1E1E',
                       foreground='#00A6E4',
                       font=('Arial', 24, 'bold'))
        
    def create_left_panel(self):
        left_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Title
        title_label = ttk.Label(left_frame, 
                               text="J.A.R.V.I.S",
                               style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Status indicators
        self.create_status_indicators(left_frame)
        
        # Time and date display
        self.time_label = ttk.Label(left_frame,
                                  text="",
                                  style='Status.TLabel')
        self.time_label.pack(pady=10)
        self.update_time()
        
    def create_status_indicators(self, parent):
        # System Status
        status_frame = ttk.Frame(parent, style='Dark.TFrame')
        status_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(status_frame,
                 text="System Status:",
                 style='Status.TLabel').pack()
        
        self.status_canvas = tk.Canvas(status_frame,
                                     width=15,
                                     height=15,
                                     bg='#1E1E1E',
                                     highlightthickness=0)
        self.status_canvas.pack(pady=5)
        self.status_indicator = self.status_canvas.create_oval(2, 2, 13, 13,
                                                             fill='green')
        
        # Voice Status
        voice_frame = ttk.Frame(parent, style='Dark.TFrame')
        voice_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(voice_frame,
                 text="Voice Status:",
                 style='Status.TLabel').pack()
        
        self.voice_canvas = tk.Canvas(voice_frame,
                                    width=15,
                                    height=15,
                                    bg='#1E1E1E',
                                    highlightthickness=0)
        self.voice_canvas.pack(pady=5)
        self.voice_indicator = self.voice_canvas.create_oval(2, 2, 13, 13,
                                                           fill='red')
        
    def create_right_panel(self):
        right_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create output display
        self.output_display = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            width=50,
            height=20,
            font=('Consolas', 10),
            bg='#2D2D2D',
            fg='#FFFFFF')
        self.output_display.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create command entry
        self.command_entry = ttk.Entry(right_frame)
        self.command_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Create buttons
        buttons_frame = ttk.Frame(right_frame, style='Dark.TFrame')
        buttons_frame.pack(fill=tk.X)
        
        start_button = ttk.Button(buttons_frame,
                                text="Start Listening",
                                command=self.toggle_listening)
        start_button.pack(side=tk.LEFT, padx=5)
        
        stop_button = ttk.Button(buttons_frame,
                               text="Stop Listening",
                               command=self.stop_listening)
        stop_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(buttons_frame,
                                text="Clear Display",
                                command=self.clear_display)
        clear_button.pack(side=tk.RIGHT, padx=5)
        
    def update_time(self):
        current_time = datetime.now().strftime("%I:%M:%S %p\n%B %d, %Y")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    def toggle_listening(self):
        if not self.listening:
            self.listening = True
            self.voice_canvas.itemconfig(self.voice_indicator, fill='green')
            self.output_display.insert(tk.END, "Listening...\n")
            self.output_display.see(tk.END)
            threading.Thread(target=self.listen_thread, daemon=True).start()
            
    def stop_listening(self):
        self.listening = False
        self.voice_canvas.itemconfig(self.voice_indicator, fill='red')
        self.output_display.insert(tk.END, "Stopped listening.\n")
        self.output_display.see(tk.END)
        
    def listen_thread(self):
        while self.listening:
            query = Jarvis.takecommand().lower()
            if query != "none":
                self.output_display.insert(tk.END, f"You: {query}\n")
                self.output_display.see(tk.END)
                
                # Process query using existing Jarvis functionality
                # Redirect Jarvis output to GUI
                original_speak = Jarvis.speak
                Jarvis.speak = self.gui_speak
                
                # Handle the query
                if "turn off jarvis" in query or "goodbye jarvis" in query:
                    self.stop_listening()
                    break
                
                # Process the query with Jarvis's AI capabilities
                sentiment_label, confidence = Jarvis.analyze_sentiment(query)
                smart_reply = Jarvis.smart_response(query)
                if smart_reply:
                    self.gui_speak(smart_reply)
                
                # Restore original speak function
                Jarvis.speak = original_speak
                
    def gui_speak(self, text):
        self.output_display.insert(tk.END, f"JARVIS: {text}\n")
        self.output_display.see(tk.END)
        # Also perform actual speech
        Jarvis.engine.say(text)
        Jarvis.engine.runAndWait()
        
    def clear_display(self):
        self.output_display.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
