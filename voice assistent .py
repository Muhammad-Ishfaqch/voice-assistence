import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import playsound
import os

# Text-to-Speech Function (using both pyttsx3 and gTTS options)
# Using pyttsx3
def speak_pyttsx3(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Using gTTS
def speak_gtts(text):
    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

# Speech recognition function (only for voice input)
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...", fg="blue")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        status_label.config(text="Recognizing...", fg="blue")
        command = recognizer.recognize_google(audio)
        recognized_text.set(f"User said: {command}")
        return command
    except sr.UnknownValueError:
        recognized_text.set("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        recognized_text.set("Could not request results from Google Speech Recognition.")
        return None

# Function to handle both voice and text input
def handle_command(input_type='voice'):
    if input_type == 'voice':
        command = take_command()
    else:
        command = command_entry.get()  # Get typed command from the text entry field
        recognized_text.set(f"User typed: {command}")  # Display typed command

    if command:  # Check if the command is not empty
        command = command.lower()
        if 'hello' in command:
            speak_gtts("Hello! How can I assist you today?")
        elif 'time' in command:
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M")
            speak_gtts(f"The current time is {current_time}")
        elif 'goodbye' in command or 'stop' in command:
            speak_gtts("Goodbye!")
            window.quit()
        else:
            speak_gtts("Sorry, I didn't catch that. Could you repeat?")
    else:
        recognized_text.set("Please provide a command.")

# GUI Setup using Tkinter
# Create the main window
window = tk.Tk()
window.title("Voice/Text-Controlled Assistant")
window.geometry("400x400")

# Text label to show recognized speech or typed text
recognized_text = tk.StringVar()
recognized_text.set("Press 'Start' to begin voice recognition or type a command below.")

recognized_label = tk.Label(window, textvariable=recognized_text, wraplength=300, font=("Arial", 12))
recognized_label.pack(pady=20)

# Status label to show listening status for voice input
status_label = tk.Label(window, text="Ready", font=("Arial", 10), fg="green")
status_label.pack(pady=10)

# Entry field for typing commands (for text input)
command_entry = tk.Entry(window, font=("Arial", 14), width=30)
command_entry.pack(pady=10)

# Button to submit the typed command
submit_button = tk.Button(window, text="Submit Text Command", command=lambda: handle_command(input_type='text'), font=("Arial", 14), bg="lightgreen")
submit_button.pack(pady=10)

# Button to start the voice recognition
start_button = tk.Button(window, text="Start Voice Recognition", command=lambda: handle_command(input_type='voice'), font=("Arial", 14), bg="lightblue")
start_button.pack(pady=10)

# Button to quit the assistant
exit_button = tk.Button(window, text="Quit", command=window.quit, font=("Arial", 14), bg="lightcoral")
exit_button.pack(pady=10)

# Run the main loop of the GUI
window.mainloop()
