import bleach
import json
from flask import Flask, jsonify
from unittest.mock import Mock
from powernap.decorators import safe

class TestDecoratorSafe(object):
    """Creates a sample app for testing"""
    app = Flask(__name__)

    def test_dict_is_sanitized_with_safe_false(self):
        """Should sanitize a dict correctly."""
        with self.app.app_context():
            func = Mock()
            func.return_value = jsonify({"value": "<script>evil();</script>"})
        decorated_func = safe(func)

        assert json.loads(decorated_func().data)['value'] == bleach.clean("<script>evil();</script>")

    def test_tuple_is_sanitized_with_safe_false(self):
        """Should sanitize a tuple correctly."""
        with self.app.app_context():
            func = Mock()
            func.return_value = jsonify(("<script>evil();</script>",))
        decorated_func = safe(func)

        assert json.loads(decorated_func().data)[0] == bleach.clean("<script>evil();</script>")

    def test_list_is_sanitized_with_safe_false(self):
        """Should sanitize a list correctly."""
        with self.app.app_context():
            func = Mock()
            func.return_value = jsonify(["<script>evil();</script>"])
        decorated_func = safe(func)

        assert json.loads(decorated_func().data)[0] == bleach.clean("<script>evil();</script>")

    def test_str_is_sanitized_with_safe_false(self):
        """Should sanitize a str correctly."""
        with self.app.app_context():
            func = Mock()
            func.return_value = jsonify("<script>evil();</script>")
        decorated_func = safe(func)

        assert json.loads(decorated_func().data) == bleach.clean("<script>evil();</script>")

    def test_data_passes_with_safe_true(self):
        """Should not sanitize data as safe is set to True."""
        func = Mock()
        func.data = "<b>This is safe</b>"
        func.return_value = func.data
        decorated_func = safe(func, safe=True)

        assert func.data == decorated_func()
