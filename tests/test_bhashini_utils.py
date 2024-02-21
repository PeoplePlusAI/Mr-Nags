import pytest
from unittest.mock import patch
import requests_mock
from utils import bhashini_utils  # assuming your function is in this module

def test_bhashini_translate_success():
    with requests_mock.Mocker() as m:
        m.post("https://dhruva-api.bhashini.gov.in/services/inference/pipeline", 
               text='{"pipelineResponse": [{"output": [{"target": "translated text"}]}]}')

        result = bhashini_utils.bhashini_translate('text', 'en', 'hi')
        assert result == 'translated text'

def test_bhashini_translate_failure():
    with requests_mock.Mocker() as m:
        m.post("https://dhruva-api.bhashini.gov.in/services/inference/pipeline", status_code=400)

        result = bhashini_utils.bhashini_translate('text', 'en', 'hi')
        assert result == 'text'

def test_bhashini_translate_invalid_lang(mocker):
    mocker.patch('utils.bhashini_utils.validate_lang', return_value=False)

    result = bhashini_utils.bhashini_translate('text', 'en', 'hi')
    assert result == 'text'

def test_bhashini_asr_success():
    with requests_mock.Mocker() as m:
        m.post("https://dhruva-api.bhashini.gov.in/services/inference/pipeline", 
               text='{"pipelineResponse": [{"output": []}, {"output": [{"target": "translated text"}]}]}')

        result = bhashini_utils.bhashini_asr('audio_content', 'en', 'hi')
        assert result == 'translated text'

def test_bhashini_asr_failure():
    with requests_mock.Mocker() as m:
        m.post("https://dhruva-api.bhashini.gov.in/services/inference/pipeline", status_code=400)

        result = bhashini_utils.bhashini_asr('audio_content', 'en', 'hi')
        assert result == 'audio_content'


@patch('utils.bhashini_utils.config')
def test_validate_lang_success(mock_config):
    mock_config.get.return_value = ['en', 'hi', 'fr']
    
    result = bhashini_utils.validate_lang('en', 'hi')
    assert result == True

@patch('utils.bhashini_utils.config')
def test_validate_lang_same_languages(mock_config):
    mock_config.get.return_value = ['en', 'hi', 'fr']

    result = bhashini_utils.validate_lang('en', 'en')
    assert result == False

@patch('utils.bhashini_utils.config')
def test_validate_lang_invalid_source_language(mock_config):
    mock_config.get.return_value = ['en', 'hi', 'fr']

    result = bhashini_utils.validate_lang('de', 'hi')
    assert result == False

@patch('utils.bhashini_utils.config')
def test_validate_lang_invalid_target_language(mock_config):
    mock_config.get.return_value = ['en', 'hi', 'fr']

    result = bhashini_utils.validate_lang('en', 'de')
    assert result == False