import json
import re
import random
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Load intents
try:
    with open('intents.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    messagebox.showerror("Error", "The file 'intents.json' was not found.")
    exit()
except json.JSONDecodeError:
    messagebox.showerror("Error", "The file 'intents.json' contains invalid JSON.")
    exit()

# Define the response function with partial matching
def get_response(user_input):
    user_words = re.findall(r'\b\w+\b', user_input.lower())  # Split user input into words
    
    max_matches = 0
    best_response = "Sorry, I didn't understand that. Can you rephrase?"

    for intent in data['intents']:
        for pattern in intent['patterns']:
            pattern_words = re.findall(r'\b\w+\b', pattern.lower())
            matches = len(set(user_words) & set(pattern_words))
            
            if matches > max_matches:
                max_matches = matches
                best_response = random.choice(intent['responses'])
                
    return best_response

# Function to send the user input to the chatbot and get a response
def send():
    user_input = user_entry.get()
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "You: " + user_input + "\n")
    chat_log.yview(tk.END)  # Scroll to the end of the chat log
    response = get_response(user_input)
    chat_log.insert(tk.END, "Bot: " + response + "\n")
    chat_log.yview(tk.END)  # Scroll to the end of the chat log
    chat_log.config(state=tk.DISABLED)
    user_entry.delete(0, tk.END)

# Function to handle the closing of the window
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# Set up the main application window
root = tk.Tk()
root.title("Chatbot")

# Create a scrollable text widget for the chat log
chat_log = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD)
chat_log.pack(padx=10, pady=10)

# Create an entry widget for the user input
user_entry = tk.Entry(root, width=50)
user_entry.pack(padx=10, pady=10)

# Create a send button
send_button = tk.Button(root, text="Send", command=send)
send_button.pack(padx=10, pady=10)

# Bind the return key to the send function
root.bind('<Return>', lambda event: send())

# Set the function to handle the window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main event loop
root.mainloop()
