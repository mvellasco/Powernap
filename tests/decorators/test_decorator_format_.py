import json
import pytest
from unittest.mock import Mock, patch
from flask import Flask
from powernap.architect.responses import ApiResponse
from powernap.exceptions import RequestLimitError
from powernap.decorators import format_


@pytest.mark.usefixtures('mock_redis')
class TestDecoratorFormat_(object):
    """Patch redis_connection method to bypass it and setup a sample app for the tests."""

    app = Flask(__name__)
    app.config['AUTHENTICATED_REQUESTS_PER_HOUR'] = 1000

    @patch('powernap.architect.responses.ApiResponse')
    @patch('flask_login.utils._get_user')
    def test_response_is_an_ApiResponse(self, current_user, api_response):
        """Should return an ApiResponse."""

        with self.app.test_request_context():
            func = Mock()
            func.data = {"value": "<b>This is a test</b>"}
            func.status_code = 200
            current_user.return_value = current_user
            func.return_value = func.data, func.status_code
            decorated_func = format_(func)

            assert decorated_func() == api_response(func.data, func.status_code).response

    @patch('flask_login.utils._get_user')
    def test_ApiResponse_is_initialized_with_all_params(self, current_user):
        """Should initialize ApiResponse with all the required parameters."""

        with self.app.test_request_context():
            func = Mock()
            func.data = {"value": "<b>This is a test</b>"}
            func.status_code = 200
            current_user.return_value = current_user
            func.return_value = func.data, func.status_code
            decorated_func = format_(func)

            if decorated_func()[0].data is None or not decorated_func()[0].status_code or \
                len(decorated_func()[0].headers) <= 2:
                    pytest.fail("Incorrect initialization of ApiResponse")


    @pytest.mark.parametrize("headers", [
        'X-RateLimit-Limit',
        'X-RateLimit-Remaining',
        'X-RateLimit-Reset',
    ])
    @patch('flask_login.utils._get_user')
    def test_response_has_headers(self, current_user, headers):
        """Should return the correct headers in the response."""
        with self.app.test_request_context():
            func = Mock()
            func.data = {"value": "<b>This is a test</b>"}
            func.status_code = 200
            current_user.return_value = current_user
            func.return_value = func.data, func.status_code
            decorated_func = format_(func)

            assert decorated_func()[0].headers[headers]

    @patch('powernap.auth.rate_limit.RateLimiter', side_effect=RequestLimitError)
    @patch('flask_login.utils._get_user')
    def test_ensure_rate_limiter_functionality(self, current_user, rl):
        """Should make sure that RateLimiter is functional."""
        with self.app.test_request_context():
            func = Mock()
            func.data = {"value": "<b>This is a test</b>"}
            func.status_code = 200
            current_user.return_value = current_user
            func.return_value = func.data, func.status_code
            decorated_func = format_(func)

            with pytest.raises(RequestLimitError):
                decorated_func()

    @patch('flask_login.utils._get_user')
    def test_decorator_format_data(self, current_user):
        """Should return the correct data that is passed by the function."""
        with self.app.test_request_context():
            func = Mock()
            func.data = {"value": "<b>This is a test</b>"}
            func.status_code = 200
            current_user.return_value = current_user
            func.return_value = func.data, func.status_code
            decorated_func = format_(func)

            assert json.loads(decorated_func()[0].data) == func.data

    @patch('flask_login.utils._get_user')
    def test_decorator_format_status_code(self, current_user):
        """Should return the correct status_code that is passed by the function."""
        with self.app.test_request_context():
            func = Mock()
            func.data = {"value": "<b>This is a test</b>"}
            func.status_code = 200
            current_user.return_value = current_user
            func.return_value = func.data, func.status_code
            decorated_func = format_(func)

            assert decorated_func()[0].status_code == 200

    @patch('flask_login.utils._get_user')
    def test_decorator_format_without_data(self, current_user):
        """Should return the status_code even if no data is passed by the function."""
        with self.app.test_request_context():
            func = Mock()
            func.status_code = 200
            func.return_value = func.status_code
            current_user.return_value = current_user
            decorated_func = format_(func)

            assert decorated_func()[0].status_code == 200

    @patch('flask_login.utils._get_user')
    def test_decorator_format_without_status_code(self, current_user):
        """Should raise an Exception if no status_code is passed by the function."""
        with self.app.test_request_context():
            func = Mock()
            func.data = {"value": "<b>This is a test</b>"}
            func.return_value = func.data
            current_user.return_value = current_user
            decorated_func = format_(func)

            with pytest.raises(Exception):
                decorated_func()

    def test_response_passes_through_with_format_false(self):
        """Should pass the function through directly if format_ is False."""
        func = Mock()
        func.data = {"value": "<b>Passing through!</b>"}
        func.return_value = func.data
        decorated_func = format_(func, format_=False)

        assert decorated_func()['value'] == "<b>Passing through!</b>"
