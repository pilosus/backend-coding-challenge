import json
from unittest import mock

import pytest


def test_ping(client):
    resp = client.get("/ping")
    assert resp.status_code == 200
    assert resp.data == b"pong"


@pytest.mark.parametrize(
    "request_data, gists, content, expected_status, expected_resp",
    [
        pytest.param(
            {"username": "test", "pattern": "(?i)python"},
            [{"id": 1, "html_url": "https://gist.example.com/1"}],
            {
                "files": {
                    "README.md": {
                        "content": "This is a tiny tech interview Python project"
                    },
                    "test_client.py": {
                        "content": "import pytest\n\ndef add(a, b): return a + b"
                    },
                }
            },
            200,
            {
                "matches": ["https://gist.example.com/1"],
                "pattern": "(?i)python",
                "status": "success",
                "username": "test",
            },
            id="found_simple",
        ),
        pytest.param(
            {"username": "test", "pattern": "python"},
            [{"id": 1, "html_url": "https://gist.example.com/1"}],
            {
                "files": {
                    "README.md": {
                        "content": "This is a tiny tech interview Python project"
                    },
                    "test_client.py": {
                        "content": "import pytest\n\ndef add(a, b): return a + b"
                    },
                }
            },
            200,
            {
                "matches": [],
                "pattern": "python",
                "status": "success",
                "username": "test",
            },
            id="not_found",
        ),
        pytest.param(
            {"username": "", "pattern": "python"},
            [{"id": 1, "html_url": "https://gist.example.com/1"}],
            {
                "files": {
                    "README.md": {
                        "content": "This is a tiny tech interview Python project"
                    },
                    "test_client.py": {
                        "content": "import pytest\n\ndef add(a, b): return a + b"
                    },
                }
            },
            400,
            {
                "code": 400,
                "error": "Request validation errors",
                "message": {"username": ["Length must be between 1 and 64."]},
            },
            id="validation_error_username",
        ),
        pytest.param(
            {"username": "pilosus", "pattern": ""},
            [{"id": 1, "html_url": "https://gist.example.com/1"}],
            {
                "files": {
                    "README.md": {
                        "content": "This is a tiny tech interview Python project"
                    },
                    "test_client.py": {
                        "content": "import pytest\n\ndef add(a, b): return a + b"
                    },
                }
            },
            400,
            {
                "code": 400,
                "error": "Request validation errors",
                "message": {"pattern": ["Shorter than minimum length 1."]},
            },
            id="validation_error_pattern",
        ),
    ],
)
@mock.patch("gistapi.api.gists_for_user")
@mock.patch("gistapi.client.GitHubClient.request")
def test_search(
    github_mock,
    gists_mock,
    request_data,
    gists,
    content,
    expected_status,
    expected_resp,
    application,
    client,
):
    gists_mock.return_value = gists
    github_mock.return_value = content
    resp = client.post("/api/v1/search", json=request_data)

    assert resp.status_code == expected_status
    assert json.loads(resp.data) == expected_resp


@pytest.mark.parametrize(
    "github_resp, pages, expected",
    [
        pytest.param(
            [],
            20,
            [],
            id="empty",
        ),
        pytest.param(
            [1, 2, 3],
            3,
            [1, 2, 3, 1, 2, 3],
            id="non-empty",
        ),
    ],
)
@mock.patch("gistapi.api.get_max_page")
@mock.patch("gistapi.client.GitHubClient.request")
def test_gists(
    github_mock, pages_mock, github_resp, pages, expected, application, client
):
    pages_mock.return_value = pages
    github_mock.return_value = github_resp
    resp = client.get("/api/v1/users/pilosus/gists")
    assert json.loads(resp.data) == expected


def test_generic_error(client):
    resp = client.put("/ping")
    assert resp.status_code == 500
    resp_data = json.loads(resp.data)
    expected = {
        "code": 500,
        "error": "Server error",
        "message": "405 Method Not Allowed: The method is not allowed for the requested URL.",
    }
    assert resp_data == expected
