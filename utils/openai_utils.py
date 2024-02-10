from dotenv import load_dotenv
from utils.redis_utils import set_redis
import time
import os

from utils.bhashini import (
    bhashini_input,
    bhashini_output,
)

load_dotenv(
    dotenv_path="ops/.env",
)

openai_api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

#OPENAI FUNCTION CALLS

authenticate_user = {
    "name": "authenticate_user",
    "description": "Authenticate user",
    "parameters": {
        "type": "object",
        "properties": {
            "username": {
                "type": "string",
                "description": "Username"
            },
            "password": {
                "type": "string",
                "description": "Password"
            }
        },
        "required": ["username", "password"]
    }
}

raise_complaint = {
    "name": "raise_complaint",
    "description": "Raise complaint",
    "parameters": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "A brief description of complaint "
                               "e.g., Streetlight not working, "
                               "Garbage accumulating near my home, "
                               "People throwing garbage illegally etc."
            },
            "service_code": {
                "type": "string",
                "description": "service code of complaint extracted from the description",
                "enum": [
                    "GarbageNeedsTobeCleared",
                    "NoStreetLight",
                    "StreetLightNotWorking",
                    "BurningOfGarbage",
                    "OverflowingOrBlockedDrain",
                    "illegalDischargeOfSewage",
                    "BlockOrOverflowingSewage",
                    "ShortageOfWater",
                    "DirtyWaterSupply",
                    "BrokenWaterPipeOrLeakage",
                    "WaterPressureisVeryLess",
                    "HowToPayPT",
                    "WrongCalculationPT",
                    "ReceiptNotGenerated",
                    "DamagedRoad",
                    "WaterLoggedRoad",
                    "ManholeCoverMissingOrDamaged",
                    "DamagedOrBlockedFootpath",
                    "ConstructionMaterialLyingOntheRoad",
                    "RequestSprayingOrFoggingOperation",
                    "StrayAnimals",
                    "DeadAnimals",
                    "DirtyOrSmellyPublicToilets",
                    "PublicToiletIsDamaged",
                    "NoWaterOrElectricityinPublicToilet",
                    "IllegalShopsOnFootPath",
                    "IllegalConstructions",
                    "IllegalParking"
                ]
            },
            "city": {
                "type": "string",
                "description": "City of complaint"
            },
            "state": {
                "type": "string",
                "description": "State of complaint"
            },
            "district": {
                "type": "string",
                "description": "district of complaint"
            },
            "region": {
                "type": "string",
                "description": "region of complaint"
            },
            "locality": {
                "type": "string",
                "description": "locality of complaint"
            },
            "name": {
                "type": "string",
                "description": "name of the user"
            },
            "mobile_number": {
                "type": "string",
                "description": "mobile number of the user"
            },
        },
        "required": [
            "description",
            "service_code",
            "city",
            "state",
            "district",
            "region",
            "locality",
            "name",
            "mobile_number"
        ]
    },
}

search_complaint = {
    "name": "search_complaint",
    "description": "Search complaint",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "name of the user"
            },
            "mobile_number": {
                "type": "string",
                "description": "mobile number of the user"
            },
        },
        "required": [
            "name",
            "mobile_number"
        ]
    }
}

def create_assistant(client, assistant_id):
    try:
        assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)
        return assistant
    except Exception as e:
        assistant = client.beta.assistants.create(
        name="Complaint Assistant",
        instructions="You are an AI assistant specifically designed to assist Indian citizens with their complaint management needs. Your core functionalities include facilitating the lodging of new complaints and retrieving details of existing complaints. At the start of each interaction, clearly inform the user about these two capabilities. Your main goal is to accurately determine the user's intention, which will correspond to the function you need to execute: either to lodge a new complaint or to retrieve details of an existing one. Engage in a step-by-step conversation to ascertain this intention. Once the user's intention is clear, methodically request the necessary information for the identified function. You should do this in a sequential manner, asking for no more than two pieces of information at a time (e.g., name and mobile number, or city and state). Avoid requesting multiple details simultaneously and refrain from making assumptions about any information. It's crucial to gather all mandatory details before executing the selected function. Only proceed with the execution once you have received all the required information. If the user provides irrelevant information or strays from the topic, respond politely and guide the conversation back to obtaining the pertinent details. Your responses should be courteous and focused, aimed at facilitating an effective and efficient interaction.",
        #instructions="You are a helpful complaint assistant who will help in filing a complaint about urban civic issues. Ask for details whenever necessary and file the complaint using tools made available to you",
        model="gpt-4",
        tools=[
                #{
                #    "type": "function",
                #    "function": authenticate_user
                #},
                {
                    "type": "function",
                    "function": raise_complaint
                },
                {
                    "type": "function",
                    "function": search_complaint
                }
            ]
        )
        set_redis("assistant_id", assistant.id)
        return assistant

def create_thread(client):
    thread = client.beta.threads.create()
    return thread

def upload_message(client, thread_id, input_message, assistant_id):
    
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=input_message
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    
    return run

def get_run_status(run, client, thread):
    i = 0

    while run.status not in ["completed", "failed", "requires_action"]:
        if i>0:
            time.sleep(10)

        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        i += 1
    return run, run.status

def get_assistant_message(client, thread_id):
    messages = client.beta.threads.messages.list(
        thread_id=thread_id,
    )
    return messages.data[0].content[0].text.value

def transcribe_audio(audio_file, client):
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcript.text