import os
import requests
from requests.compat import urljoin


class GitHubClient:
    """
    Wrapper class to access GitHub API
    """

    def __init__(
            self,
            api_key: str = None,
            api_version: str = "2022-11-28",
            timeout: float = 10.0
    ):
        self.base_url = "https://api.github.com"
        self.api_key = api_key or os.environ.get("GITHUB_TOKEN")
        self.api_version = api_version
        self.timeout = timeout

    @property
    def bearer(self):
        """
        Return bearer token (API Key) for GitHub API access with higher rate limits
        """
        return "Bearer {api_key}".format(api_key=self.api_key)

    @property
    def headers(self):
        """
        Return default HTTP headers
        """
        return {"X-GitHub-Api-Version": self.api_version,
                "Authorization": self.bearer}

    def request(self, method: str, url: str, **kwargs) -> dict | list:
        """
        Return decoded JSON response from the GitHub API or raise error
        """
        uri = urljoin(self.base_url, url)
        resp = requests.request(method=method, url=uri, headers=self.headers, timeout=self.timeout, **kwargs)
        resp.raise_for_status()
        return resp.json()
