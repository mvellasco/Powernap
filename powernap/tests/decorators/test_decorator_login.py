import pytest
from unittest.mock import Mock, patch
from powernap.decorators import login
from powernap.exceptions import UnauthorizedError


class TestLoginDecorator(object):
    @patch('flask_login.utils._get_user')
    def test_with_authenticated_user(self, current_user):
        """Should call the function using the decorator if a authenticated user is provided."""
        func = Mock()
        current_user.is_authenticated = True
        current_user.return_value = current_user
        decorated_func = login(func)

        assert decorated_func().is_called

    @patch('flask_login.utils._get_user')
    def test_with_unauthenticated_user(self, current_user):
        """Should raise UnauthorizedError because the user is not authenticated."""
        func = Mock()
        current_user.is_authenticated = False
        current_user.return_value = current_user
        decorated_func = login(func)

        with pytest.raises(UnauthorizedError):
            decorated_func()

    @patch('flask_login.utils._get_user')
    def test_with_unauthenticated_user_and_login_false(self, current_user):
        """Should call the function using the decorator because login is False."""
        func = Mock()
        current_user.is_authenticated = False
        current_user.return_value = current_user
        decorated_func = login(func, login=False)

        assert decorated_func().is_called
