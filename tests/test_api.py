import json
import pytest
from unittest import mock


def test_ping(client):
    resp = client.get("/ping")
    assert resp.status_code == 200
    assert resp.data == b"pong"


@pytest.mark.parametrize("request_data, gists, content, expected", [
    pytest.param(
{"username": "test", "pattern": "(?i)python"},
        [{"id": 1, "html_url": "https://gist.example.com/1"}],
        {"files": {
            "README.md": {"content": "This is a tiny tech interview Python project"},
            "test_client.py": {"content": "import pytest\n\ndef add(a, b): return a + b"},
        }},
        {"matches": ["https://gist.example.com/1"], "pattern": "(?i)python", "status": "success", "username": "test"},
        id="found_simple",
    ),
    pytest.param(
{"username": "test", "pattern": "python"},
        [{"id": 1, "html_url": "https://gist.example.com/1"}],
        {"files": {
            "README.md": {"content": "This is a tiny tech interview Python project"},
            "test_client.py": {"content": "import pytest\n\ndef add(a, b): return a + b"},
            }},
        {"matches": [], "pattern": "python", "status": "success", "username": "test"},
        id="not_found",
    ),
])
@mock.patch("gistapi.gistapi.gists_for_user")
@mock.patch("gistapi.client.GitHubClient.request")
def test_search(github_mock, gists_mock, request_data, gists, content, expected, application, client):
    gists_mock.return_value = gists
    github_mock.return_value = content
    resp = client.post("/api/v1/search", json=request_data)
    actual = json.loads(resp.data)
    assert actual == expected
