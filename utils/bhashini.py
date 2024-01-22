import requests
import json

def bhashini_input(text):
    data = {
        "inputText": text,
        "inputLanguage": "Punjabi",
        "outputLanguage": "English"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post("https://tts.bhashini.ai/v1/translate", headers=headers, json=data)

    if response.status_code == 200:
        return response.text
    else:
        print("Error:", response.status_code, response.text)

def bhashini_output(text):
    data = {
        "inputText": text,
        "inputLanguage": "English",
        "outputLanguage": "Punjabi"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post("https://tts.bhashini.ai/v1/translate", headers=headers, json=data)

    if response.status_code == 200:
        return response.text
    else:
        print("Error:", response.status_code, response.text)

