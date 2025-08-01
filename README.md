# JARVIS AI Assistant

An AI-powered virtual assistant with voice recognition, natural language processing, and a modern GUI interface.

## Features

- Voice recognition and text-to-speech capabilities
- Sentiment analysis for understanding user emotions
- Natural Language Processing for better command understanding
- Face detection with AI capabilities
- Modern graphical user interface
- System automation (opening applications, web browsing)
- Web searches and information retrieval
- Email sending capabilities
- YouTube and music playback control

## Requirements

- Python 3.x
- Required packages:
  - pyttsx3
  - speech_recognition
  - opencv-python
  - wikipedia
  - pywhatkit
  - textblob
  - nltk
  - transformers
  - torch
  - scikit-learn
  - PIL (Pillow)
  - requests

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/Jarvis.git
cd Jarvis
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the GUI version:
```bash
python jarvis_gui.py
```

2. Run the command-line version:
```bash
python Jarvis.py
```

## Available Commands

- "open [application]" - Opens specified application (notepad, whatsapp, spotify, etc.)
- "open camera" - Opens camera with AI-enhanced face detection
- "play music" - Plays music from specified directory
- "wikipedia [query]" - Searches Wikipedia for information
- "open [website]" - Opens specified website (youtube, instagram, facebook, etc.)
- "send message" - Sends WhatsApp message
- "play song on youtube" - Plays specified song on YouTube
- "email to [person]" - Sends email to specified person
- "turn off jarvis" - Exits the program

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
