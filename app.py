import json
import re
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load intents from the JSON file
def load_intents(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: The file 'intents.json' was not found.")
        return None
    except json.JSONDecodeError:
        print("Error: The file 'intents.json' contains invalid JSON.")
        return None

# Function to get a response based on user input
def get_response(user_input, intents_data):
    for intent in intents_data.get('intents', []):
        for pattern in intent.get('patterns', []):
            if re.search(pattern, user_input, re.IGNORECASE):
                return intent.get('responses', ['Sorry, I did not understand that.'])[0]
    return 'Sorry, I did not understand that.'

# Log conversation to a file
def log_conversation(user_input, response):
    with open('chat_log.txt', 'a') as log_file:
        log_file.write(f"{datetime.datetime.now()} - User: {user_input}\n")
        log_file.write(f"{datetime.datetime.now()} - Bot: {response}\n\n")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'response': 'No message received.'})

    intents_data = load_intents('intents.json')
    if intents_data is None:
        return jsonify({'response': 'Error loading intents.'})

    response = get_response(user_input, intents_data)
    log_conversation(user_input, response)

    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(port=5000)
