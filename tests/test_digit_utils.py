import pytest
import requests_mock
from utils.digit_utils import (
    file_complaint,
    get_auth_token,
    search_complaint
)  

def test_get_auth_token_success():
    with requests_mock.Mocker() as m:
        m.post("https://staging.digit.org/user/oauth/token", 
               text='{"access_token": "valid_token"}')

        result = get_auth_token({'username': 'test', 'password': 'test'})
        assert result == 'valid_token'

def test_get_auth_token_failure():
    with requests_mock.Mocker() as m:
        m.post("https://staging.digit.org/user/oauth/token", status_code=400)

        result = get_auth_token({'username': 'test', 'password': 'test'})
        assert result is None
        


def test_file_complaint_success():
    data = {
        "city": "Test City",
        "district": "Test District",
        "region": "Test Region",
        "state": "Test State",
        "locality": "Test Locality",
        "auth_token": "test_token",
        "username": "test_user",
        "name": "Test User"
    }

    with requests_mock.Mocker() as m:
        m.post("https://staging.digit.org/pgr-services/v2/request/_create", 
               text='{"serviceRequestId": "12345"}')

        result = file_complaint(data)
        assert result == {"serviceRequestId": "12345"}

def test_file_complaint_failure():
    data = {
        "city": "Test City",
        "district": "Test District",
        "region": "Test Region",
        "state": "Test State",
        "locality": "Test Locality",
        "auth_token": "test_token",
        "username": "test_user",
        "name": "Test User"
    }

    with requests_mock.Mocker() as m:
        m.post("https://staging.digit.org/pgr-services/v2/request/_create", status_code=400)

        result = file_complaint(data)
        assert result is None


def test_search_complaint_success():
    data = {
            "username": "test_user",
            "name": "Test User",
            "auth_token": "test_token",
            "mobile_number": "1234567890"
    }

    with requests_mock.Mocker() as m:
        m.post(f"https://staging.digit.org/pgr-services/v2/request/_search?tenantId=pg.cityb&mobileNumber={data['username']}&_=1704443852959", 
                       text='{"complaints": [{"id": "12345"}]}')

        result = search_complaint(data)
        assert result == {"complaints": [{"id": "12345"}]}

def test_search_complaint_failure():
    data = {
            "username": "test_user",
            "name": "Test User",
            "auth_token": "test_token",
            "mobile_number": "1234567890"
        }

    with requests_mock.Mocker() as m:
        m.post(f"https://staging.digit.org/pgr-services/v2/request/_search?tenantId=pg.cityb&mobileNumber={data['username']}&_=1704443852959", status_code=400)

        result = search_complaint(data)
        assert result is None