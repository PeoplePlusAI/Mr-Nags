import requests
import json

def bhashini_input(text, lang):
    language = {'hi': 'Hindi', 'en': 'English', 'pa': 'Punjabi'}
    lang_ = language.get(lang)
    print(lang_)
    data = {
        "inputText": text,
        "inputLanguage": lang_,
        "outputLanguage": "English"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post("https://tts.bhashini.ai/v1/translate", headers=headers, json=data)

    if response.status_code == 200:
        return response.text
    else:
        print("Error:", response.status_code, response.text)

def bhashini_output(text,lang):
    language = {'hi': 'Hindi', 'en': 'English', 'pa': 'Punjabi'}
    lang_ = language.get(lang)
    print(lang_)
    data = {
        "inputText": text,
        "inputLanguage": "English",
        "outputLanguage": lang_
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post("https://tts.bhashini.ai/v1/translate", headers=headers, json=data)

    if response.status_code == 200:
        return response.text
    else:
        print("Error:", response.status_code, response.text)

def bhashini_asr(audio_content, lang):
    
    data = {
    "pipelineTasks": [
        {
            "taskType": "asr",
            "config": {
                "language": {
                    "sourceLanguage": lang
                },
                "serviceId": "ai4bharat/conformer-hi-gpu--t4"
            }
        },
        {
            "taskType": "translation",
            "config": {
                "language": {
                    "sourceLanguage": lang,
                    "targetLanguage": "en"
                },
                "serviceId": "ai4bharat/indictrans-v2-all-gpu--t4"
            }
        }
    ],
    "inputData": {
        "audio": [
            {
                "audioContent":audio_content
            }
        ]
    }
    }
    headers = {'content-type': 'application/json','Authorization':'0ELDJvqbaDLzAGPIR1Dfv38ehE21HkMjxWkXYWq-Mk1bajlyyxXMyHGpwb3lD2cz'}
    response = requests.post("https://dhruva-api.bhashini.gov.in/services/inference/pipeline", headers=headers, json=data)

    if response.status_code == 200:
        response_asr = json.loads(response.content.decode('utf-8'))
        return response_asr['pipelineResponse'][1]['output'][0]['target']
        # return response_asr
    else:
        return "Error: {response.status_code}"

        #bhashini_asr(audio_content)