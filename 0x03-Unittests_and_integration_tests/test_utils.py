#!/usr/bin/env python3
"""Test module for utils functions."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test the access_nested_map utility function."""

    @parameterized.expand([
        [{"a": 1}, ("a",), 1],
        [{"a": {"b": 2}}, ("a",), {"b": 2}],
        [{"a": {"b": 2}}, ("a", "b"), 2],
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that it returns the correct value for valid keys."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        [{}, ("a",)],
        [{"a": 1}, ("a", "b")],
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that it raises KeyError for invalid keys."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        # Check that the exception message is as expected
        self.assertEqual(str(context.exception), f"'{path[-1]}'")


class TestGetJson(unittest.TestCase):
    """Test the get_json utility function."""

    @parameterized.expand([
        ["http://example.com", {"payload": True}],
        ["http://holberton.io", {"payload": False}],
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test that get_json returns expected result with mocked requests."""
        # Configure mock response
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function
        result = get_json(test_url)

        # Assert that requests.get was called exactly once with test_url
        mock_get.assert_called_once_with(test_url)

        # Assert that the result equals test_payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches method calls."""

        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Create an instance of TestClass
        test_obj = TestClass()

        # Mock the a_method
        with patch.object(test_obj, 'a_method',
                          return_value=42) as mock_method:
            # Call a_property twice
            result1 = test_obj.a_property
            result2 = test_obj.a_property

            # Assert that both calls return the correct result
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert that a_method was called only once due to memoization
            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
