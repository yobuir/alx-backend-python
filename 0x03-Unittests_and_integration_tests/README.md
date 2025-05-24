# Unit Testing & Integration Testing Project

This project implements comprehensive unit testing and integration testing for utility functions and GitHub organization client using Python's `unittest` framework. It is part of the `0x03-Unittests_and_integration_tests` module of the ALX Backend Python curriculum.

## 📁 Project Structure

```
0x03-Unittests_and_integration_tests/
├── utils.py                 # Utility functions (access_nested_map, get_json, memoize)
├── client.py               # GithubOrgClient class
├── fixtures.py             # Test payload data for integration tests
├── test_utils.py           # Unit tests for utils.py
├── test_client.py          # Unit and integration tests for client.py
└── README.md              # This file
```

## 🎯 Project Objectives

Implement comprehensive testing covering:
1. **Unit Testing**: Individual function/method testing with mocking
2. **Integration Testing**: End-to-end testing with fixtures
3. **Parameterized Testing**: Data-driven test cases
4. **Mocking**: External dependency isolation
5. **Property Testing**: Testing class properties and decorators

## ✅ Completed Tasks

### Task 1: Parameterized Unit Tests for `utils.access_nested_map`
- **File**: `test_utils.py` - `TestAccessNestedMap` class
- **Tests**: Valid key access and KeyError exceptions
- **Features**: `@parameterized.expand` decorator usage

### Task 2: Mock HTTP Calls for `utils.get_json`
- **File**: `test_utils.py` - `TestGetJson` class  
- **Tests**: HTTP request mocking with `@patch('utils.requests.get')`
- **Features**: Mock return values and call verification

### Task 3: Memoization Decorator Testing
- **File**: `test_utils.py` - `TestMemoize` class
- **Tests**: Decorator functionality with method call counting
- **Features**: `patch.object()` context manager usage

### Task 4: Client Organization Method Testing
- **File**: `test_client.py` - `TestGithubOrgClient.test_org`
- **Tests**: `GithubOrgClient.org` method with parameterized org names
- **Features**: `@patch('client.get_json')` and URL verification

### Task 5: Property Mocking
- **File**: `test_client.py` - `TestGithubOrgClient.test_public_repos_url`
- **Tests**: `_public_repos_url` property using `PropertyMock`
- **Features**: Property-specific mocking techniques

### Task 6: Multiple Patches Testing
- **File**: `test_client.py` - `TestGithubOrgClient.test_public_repos`
- **Tests**: `public_repos` method with multiple mock patches
- **Features**: Combined `@patch` and `PropertyMock` usage

### Task 7: Parameterized License Testing
- **File**: `test_client.py` - `TestGithubOrgClient.test_has_license`
- **Tests**: Static method with various license scenarios
- **Features**: Boolean return value testing

### Task 8: Integration Testing with Fixtures
- **File**: `test_client.py` - `TestIntegrationGithubOrgClient`
- **Tests**: End-to-end testing with real-like data from `fixtures.py`
- **Features**: `@parameterized_class`, `setUpClass`/`tearDownClass` methods

## 🧪 Test Coverage Summary

| Module | Test Class | Methods Tested | Test Count | Status |
|--------|------------|----------------|------------|--------|
| utils.py | TestAccessNestedMap | access_nested_map | 5 | ✅ |
| utils.py | TestGetJson | get_json | 2 | ✅ |
| utils.py | TestMemoize | memoize decorator | 1 | ✅ |
| client.py | TestGithubOrgClient | org, _public_repos_url, public_repos, has_license | 6 | ✅ |
| client.py | TestIntegrationGithubOrgClient | Integration tests | 2 | ✅ |

**Total Tests**: 16 tests ✅ **All Passing**

## 🧰 How to Run Tests

### Run All Tests
```bash
cd 0x03-Unittests_and_integration_tests
python -m unittest discover -v
```

### Run Specific Test Files
```bash
# Utils tests only
python -m unittest test_utils.py -v

# Client tests only  
python -m unittest test_client.py -v
```

### Run Individual Test Classes
```bash
# Test specific class
python -m unittest test_utils.TestAccessNestedMap -v
python -m unittest test_client.TestGithubOrgClient -v
```

## 🔧 Key Testing Techniques Demonstrated

### 1. Parameterized Testing
```python
@parameterized.expand([
    [{"a": 1}, ("a",), 1],
    [{"a": {"b": 2}}, ("a", "b"), 2],
])
def test_access_nested_map(self, nested_map, path, expected):
    self.assertEqual(access_nested_map(nested_map, path), expected)
```

### 2. Mock Patching
```python
@patch('utils.requests.get')
def test_get_json(self, mock_get):
    mock_get.return_value.json.return_value = test_payload
    result = get_json("http://example.com")
    mock_get.assert_called_once_with("http://example.com")
```

### 3. Property Mocking
```python
with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
    mock_org.return_value = test_payload
    result = client._public_repos_url
```

### 4. Integration Testing with Fixtures
```python
@parameterized_class([{"org_payload": TEST_PAYLOAD[0][0], ...}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('requests.get')
        # ... setup mocks
```

## 🧩 Dependencies

- **Python 3.7+**
- **parameterized**: For data-driven tests
- **unittest.mock**: For mocking (built-in)
- **requests**: For HTTP requests (mocked in tests)

```bash
pip install parameterized requests
```

## 📊 Test Results

```
Ran 16 tests in 0.024s
OK
```

All tests pass successfully, demonstrating comprehensive coverage of:
- ✅ Utility function edge cases
- ✅ HTTP request mocking
- ✅ Decorator functionality  
- ✅ Class method and property testing
- ✅ Integration scenarios with realistic data
- ✅ Error handling and exception testing

## 📎 Related Files

- **`utils.py`**: Core utility functions
- **`client.py`**: GitHub organization client implementation  
- **`fixtures.py`**: Test data payloads for integration testing
- **`test_utils.py`**: Comprehensive utility function tests
- **`test_client.py`**: Client class unit and integration tests