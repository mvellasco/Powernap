import pytest
from redis import Redis
from unittest.mock import Mock, patch


@pytest.yield_fixture(scope='class')
def mock_redis():
    mocked_redis = Mock(Redis)
    mocked_redis.get.return_value = None
    redis_con = patch('powernap.helpers.redis_connection', return_value=mocked_redis).start()
    redis_con.assert_not_called()
    yield redis_con
    redis_con.stop()
    redis_con.stop.assert_called_once()
