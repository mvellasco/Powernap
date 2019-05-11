import pytest
from unittest.mock import Mock, patch
from powernap.decorators import public

class TestPublicDecorator(object):
    """Imports Flask and creates a sample app for testing"""
    from flask import Flask
    from werkzeug.exceptions import NotFound, ServiceUnavailable


    app = Flask(__name__)

    def test_it_should_raise_a_404_error_if_no_user_and_DEBUG_is_False(self):
        """Should raise a 404 error if no user is provided and DEBUG is False."""
        with self.app.app_context():
            func = Mock()
            decorated_func = public(func)

            with pytest.raises(self.NotFound):
                decorated_func()

    def test_it_should_raise_a_503_error_if_no_user_and_DEBUG_is_True(self):
        """Should raise a 503 error if no user is provided and DEBUG is True."""
        self.app.config['DEBUG'] = True
        with self.app.app_context():
            func = Mock()
            decorated_func = public(func)

            with pytest.raises(self.ServiceUnavailable):
                decorated_func()

    @patch('flask_login.utils._get_user')
    def test_it_should_raise_a_503_error_if_no_admin_user_and_DEBUG_is_True(self, current_user):
        """Should raise a 503 error if no admin user is provided and public is False and DEBUG is True."""
        self.app.config['DEBUG'] = True
        with self.app.app_context():
            func = Mock()
            current_user.is_admin = False
            current_user.return_value = current_user
            decorated_func = public(func)

            with pytest.raises(self.ServiceUnavailable):
                decorated_func()

    @patch('flask_login.utils._get_user')
    def test_it_should_raise_a_404_error_if_no_admin_user_and_DEBUG_is_True(self, current_user):
        """Should raise a 404 error if no admin user is provided and public is False and DEBUG is False."""
        self.app.config['DEBUG'] = False
        with self.app.app_context():
            func = Mock()
            current_user.is_admin = False
            current_user.return_value = current_user
            decorated_func = public(func)

            with pytest.raises(self.NotFound):
                decorated_func()

    def test_without_admin_user_and_public_true(self):
        """Should accept access without admin user because public is set to True."""
        func = Mock()
        decorated_func = public(func, public=True)

        assert decorated_func().is_called

    @patch('flask_login.utils._get_user')
    def test_with_admin_user(self, current_user):
        """Should call the function using the decorator when user is admin."""
        func = Mock()
        current_user.is_admin = True
        current_user.return_value = current_user
        decorated_func = public(func)

        assert decorated_func().is_called
