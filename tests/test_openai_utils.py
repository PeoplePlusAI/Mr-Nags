import pytest
from openai import OpenAI
from unittest.mock import MagicMock, patch
from utils.openai_utils import (
    create_assistant,
    create_thread,
    upload_message, 
    get_run_status,
    get_assistant_message,
    generate_audio,
    get_duration_pydub,
    get_random_wait_messages 
)

client = OpenAI()

def test_create_assistant_retrieve_success():
    mock_client = MagicMock()
    mock_assistant = MagicMock()
    assistant_id = 'existing_assistant_id'
    
    # Simulate successful retrieval
    mock_client.beta.assistants.retrieve.return_value = mock_assistant

    result = create_assistant(mock_client, assistant_id)

    # Verify the result is the retrieved assistant
    assert result == mock_assistant
    # Verify retrieve was called correctly
    mock_client.beta.assistants.retrieve.assert_called_once_with(assistant_id=assistant_id)
    # Verify create was not called
    mock_client.beta.assistants.create.assert_not_called()

def test_create_assistant_retrieve_fail_and_create():
    mock_client = MagicMock()
    mock_new_assistant = MagicMock()
    assistant_id = 'nonexistent_assistant_id'
    
    # Simulate retrieval failure by raising an Exception
    mock_client.beta.assistants.retrieve.side_effect = Exception("Retrieval failed")
    # Simulate successful creation
    mock_client.beta.assistants.create.return_value = mock_new_assistant

    result = create_assistant(mock_client, assistant_id)

    # Verify the result is the newly created assistant
    assert result == mock_new_assistant
    # Verify retrieve was called correctly
    mock_client.beta.assistants.retrieve.assert_called_once_with(assistant_id=assistant_id)
    

def test_create_thread():
    mock_client = MagicMock()
    mock_thread = MagicMock()
    mock_client.beta.threads.create.return_value = mock_thread

    result = create_thread(mock_client)

    assert result == mock_thread
    mock_client.beta.threads.create.assert_called_once()


def test_upload_message():
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_run = MagicMock()
    thread_id = 'test_thread_id'
    input_message = 'test_message'
    assistant_id = 'test_assistant_id'

    mock_client.beta.threads.messages.create.return_value = mock_message
    mock_client.beta.threads.runs.create.return_value = mock_run

    result = upload_message(mock_client, thread_id, input_message, assistant_id)

    assert result == mock_run
    mock_client.beta.threads.messages.create.assert_called_once_with(
        thread_id=thread_id, role="user", content=input_message
    )
    mock_client.beta.threads.runs.create.assert_called_once_with(
        thread_id=thread_id, assistant_id=assistant_id
    )

def test_get_run_status_completed():
    mock_client = MagicMock()
    mock_run = MagicMock()
    mock_run.status = 'completed'
    mock_thread = MagicMock()
    mock_thread.id = 'test_thread_id'
    mock_run.id = 'test_run_id'

    with patch('utils.openai_utils.time.sleep', return_value=None) as mock_sleep:
        result_run, result_status = get_run_status(mock_run, mock_client, mock_thread)

    assert result_run == mock_run
    assert result_status == 'completed'
    mock_client.beta.threads.runs.retrieve.assert_not_called()


def test_get_assistant_message():
    # Set up mock client
    mock_client = MagicMock()

    # Mock the nested structure as expected by get_assistant_message
    mock_message = MagicMock()
    mock_message.text.value = 'test message'

    mock_content = MagicMock()
    mock_content.content = [mock_message]  # Simulate list with one message object

    mock_data = MagicMock()
    mock_data.data = [mock_content]  # Simulate list with one content object

    # Assign mock_data as the return value of the list method
    mock_client.beta.threads.messages.list.return_value = mock_data

    # Use the mock in your test
    thread_id = 'thread_id'  # Example thread_id
    result = get_assistant_message(mock_client, thread_id)
    
    # Assert that the result matches expected output
    assert result == 'test message', "The message retrieved does not match the expected output."
    

def test_generate_audio():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_client.audio.speech.create.return_value = mock_response
    text = 'test text'

    result = generate_audio(text, mock_client)

    assert result == mock_response
    mock_client.audio.speech.create.assert_called_once_with(
        model="tts-1",
        voice="alloy",
        input=text
    )

def test_get_duration_pydub():
    mock_audio_segment = MagicMock()
    mock_audio_file = MagicMock()
    mock_audio_file.duration_seconds = 10.0
    mock_audio_segment.from_file.return_value = mock_audio_file
    file_path = 'test_file_path'

    with patch('utils.openai_utils.AudioSegment', mock_audio_segment):
        result = get_duration_pydub(file_path)

    assert result == 10.0
    mock_audio_segment.from_file.assert_called_once_with(file_path)


import random
from utils.openai_utils import get_random_wait_messages

def test_get_random_wait_messages():
    messages = [
        "I am thinking",
        "I am processing your request",
        "Hold on",
        "I am on it",
        "I am working on it",
    ]

    # Test when always is False
    result = get_random_wait_messages(False)
    assert result in messages, "The message returned is not in the predefined list."

    # Test when always is True
    results = [get_random_wait_messages(True) for _ in range(100)]
    for result in results:
        assert result in messages or result == "", "The message returned is not in the predefined list or an empty string."