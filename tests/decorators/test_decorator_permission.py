import pytest
from unittest.mock import Mock, patch
from powernap.decorators import permission
from powernap.exceptions import PermissionError

class TestPermissionDecorator(object):
    @patch('flask_login.utils._get_user')
    def test_user_has_permission(self, current_user):
        """Should call the function using the decorator when user has the permission."""
        func = Mock()
        current_user.has_permission.return_value = True
        current_user.return_value = current_user
        decorated_func = permission(func, permission="permission")

        assert decorated_func().is_called

    @patch('flask_login.utils._get_user')
    def test_user_is_admin(self, current_user):
        """Should call the function using the decorator when user is admin."""
        func = Mock()
        current_user.is_admin.return_value = True
        current_user.has_permission.return_value = False
        current_user.return_value = current_user
        decorated_func = permission(func, permission="permission")

        assert decorated_func().is_called

    @patch('flask_login.utils._get_user')
    def test_user_does_not_need_permission(self, current_user):
        """Should call the function using the decorator when permission is None."""
        func = Mock()
        current_user.return_value = current_user
        decorated_func = permission(func)

        assert decorated_func().is_called

    @patch('flask_login.utils._get_user')
    def test_it_should_raise_a_PermissionError_if_user_does_not_have_permission(self, current_user):
        """Should raise PermissionError when user does not have the permission."""
        func = Mock()
        current_user.has_permission.return_value = False
        current_user.is_admin = False
        current_user.return_value = current_user
        decorated_func = permission(func, permission="permission")

        with pytest.raises(PermissionError):
            decorated_func()
