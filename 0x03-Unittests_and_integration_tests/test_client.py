#!/usr/bin/env python3
"""Unit tests for client module.
"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ["google"],
        ["abc"],
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        # Create test payload
        test_payload = {
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
        }
        mock_get_json.return_value = test_payload

        # Create client and call org method
        client = GithubOrgClient(org_name)
        result = client.org

        # Verify the mock was called once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Verify the result
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url property"""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("google")

            # Test the property
            result = client._public_repos_url
            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos method"""
        # Test payload with repo names
        test_repos = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": None},
        ]
        mock_get_json.return_value = test_repos

        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = \
                "https://api.github.com/orgs/google/repos"

            client = GithubOrgClient("google")
            result = client.public_repos()

            # Verify all repo names are returned
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            # Verify mocks were called once
            mock_get_json.assert_called_once()
            mock_repos_url.assert_called_once()

    @parameterized.expand([
        [{"license": {"key": "my_license"}}, "my_license", True],
        [{"license": {"key": "other_license"}}, "my_license", False],
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license static method"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": ["episodes.dart", "cpp-netlib", "dagger",
                           "ios-webkit-debug-proxy", "google.github.io",
                           "kratu", "build-debian-cloud", "traceur-compiler",
                           "firmata.py"],
        "apache2_repos": ["dagger", "kratu", "traceur-compiler",
                          "firmata.py"]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up class fixtures before running tests"""
        # Mock requests.get to return example payloads
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Configure mock to return appropriate payloads based on URL
        def side_effect(url):
            mock_response = Mock()
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Remove the class fixtures after running all tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test: test public_repos method without license filter"""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test: test public_repos method with license filter"""
        client = GithubOrgClient("google")
        repos = client.public_repos("apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
