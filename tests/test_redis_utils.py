from unittest.mock import MagicMock, patch
from utils.redis_utils import (
    set_redis,
    get_redis_value,
    delete_redis
)

def test_set_redis():
    mock_redis_client = MagicMock()

    with patch('utils.redis_utils.redis_client', mock_redis_client):
        key = 'test_key'
        value = 'test_value'
        expire = 900

        set_redis(key, value, expire)

        mock_redis_client.set.assert_called_once_with(key, value, ex=expire)

def test_get_redis_value():
    mock_redis_client = MagicMock()

    with patch('utils.redis_utils.redis_client', mock_redis_client):
        key = 'test_key'
        mock_redis_client.get.return_value = 'test_value'

        result = get_redis_value(key)

        assert result == 'test_value'
        mock_redis_client.get.assert_called_once_with(key)

def test_delete_redis():
    mock_redis_client = MagicMock()

    with patch('utils.redis_utils.redis_client', mock_redis_client):
        key = 'test_key'

        delete_redis(key)

        mock_redis_client.delete.assert_called_once_with(key)