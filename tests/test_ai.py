from unittest.mock import MagicMock, patch
from core.ai import (
    chat,
    audio_chat, 
    bhashini_text_chat,
    bhashini_audio_chat
)

def test_audio_chat():
    mock_client = MagicMock()
    mock_transcribe_audio = MagicMock()
    mock_chat = MagicMock()
    mock_generate_audio = MagicMock()

    chat_id = 'test_chat_id'
    audio_file = 'test_audio_file'
    input_message = 'test_input_message'
    assistant_message = 'test_assistant_message'
    history = 'test_history'
    response_audio = 'test_response_audio'

    with patch('core.ai.transcribe_audio', mock_transcribe_audio), \
         patch('core.ai.chat', mock_chat), \
         patch('core.ai.generate_audio', mock_generate_audio), \
         patch('core.ai.client', return_value=mock_client):

        mock_transcribe_audio.return_value = input_message
        mock_chat.return_value = (assistant_message, history)
        mock_generate_audio.return_value = response_audio

        result = audio_chat(chat_id, audio_file, mock_client)

    assert result == (response_audio, history)
    mock_transcribe_audio.assert_called_once_with(audio_file, mock_client)
    mock_chat.assert_called_once_with(chat_id, input_message)
    mock_generate_audio.assert_called_once_with(assistant_message, mock_client)


def test_bhashini_text_chat():
    mock_bhashini_translate = MagicMock()
    mock_chat = MagicMock()
    mock_client = MagicMock()

    chat_id = 'test_chat_id'
    text = 'test_text'
    lang = 'test_lang'
    input_message = 'test_input_message'
    assistant_message = 'test_assistant_message'
    history = 'test_history'
    response = 'test_response'

    with patch('core.ai.bhashini_translate', mock_bhashini_translate), \
         patch('core.ai.chat', mock_chat):

        mock_bhashini_translate.side_effect = [input_message, response]
        mock_chat.return_value = (assistant_message, history)

        result = bhashini_text_chat(chat_id, text, lang, mock_client)

    assert result == (response, history)
    mock_bhashini_translate.assert_any_call(text, lang, "en")
    mock_bhashini_translate.assert_any_call(assistant_message, "en", lang)
    mock_chat.assert_called_once_with(chat_id, input_message, mock_client)


def test_bhashini_audio_chat():
    mock_bhashini_asr = MagicMock()
    mock_client = MagicMock()
    mock_chat = MagicMock()
    mock_bhashini_translate = MagicMock()

    chat_id = 'test_chat_id'
    audio_file = 'test_audio_file'
    lang = 'test_lang'
    input_message = 'test_input_message'
    assistant_message = 'test_assistant_message'
    history = 'test_history'
    response = 'test_response'

    with patch('core.ai.bhashini_asr', mock_bhashini_asr), \
         patch('core.ai.chat', mock_chat), \
         patch('core.ai.bhashini_translate', mock_bhashini_translate):

        mock_bhashini_asr.return_value = input_message
        mock_chat.return_value = (assistant_message, history)
        mock_bhashini_translate.return_value = response

        result = bhashini_audio_chat(chat_id, audio_file, lang, mock_client)

    assert result == (response, history)
    mock_bhashini_asr.assert_called_once_with(audio_file, lang)
    mock_chat.assert_called_once_with(chat_id, input_message, mock_client)
    mock_bhashini_translate.assert_called_once_with(assistant_message, "en", lang)