#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected value"""
        payload = {"login": org_name}
        mock_get_json.return_value = payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, payload)
        url = "https://api.github.com/orgs/{}".format(org_name)
        mock_get_json.assert_called_once_with(url)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected value"""
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = payload

            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns list of repo names"""
        payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = payload

        client = GithubOrgClient("google")
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = "http://some_url.com/repos"

            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "http://some_url.com/repos"
            )


if __name__ == "__main__":
    unittest.main()
 