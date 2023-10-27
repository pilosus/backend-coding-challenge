import pytest

from gistapi.helpers import search_file, search_gist


@pytest.mark.parametrize(
    "pattern, content, expected",
    [
        pytest.param(
            r"Python",
            "I love Python, you know!",
            True,
            id="found_simple",
        ),
        pytest.param(
            r"(?i)Python",
            "I love python, you know!",
            True,
            id="found_flags",
        ),
        pytest.param(
            r"(?i)clj-\w{1,3}",
            "Actually, Clojure is a nice language too\nTake at my Game of life implementation under pilosus/clj-gol",
            True,
            id="found_complex",
        ),
        pytest.param(
            r"^Python",
            "Gosh, I've watched all the 'Monthy Python Flying Circus' seasons, including the one for German TV",
            False,
            id="not_found",
        ),
        pytest.param(
            r"^Python",
            "",
            False,
            id="empty_content",
        ),
        pytest.param(
            r"",
            "Did you know that empty pattern matches any string?",
            True,
            id="empty_pattern",
        ),
        pytest.param(
            r"",
            "",
            True,
            id="empty_pattern_and_content",
        ),
    ],
)
def test_search_file(pattern, content, expected):
    actual = search_file(pattern=pattern, content=content)
    assert actual is expected


@pytest.mark.parametrize(
    "pattern, gist, expected",
    [
        pytest.param(
            r"(?i)python",
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
            True,
            id="found_simple",
        ),
        pytest.param(
            r"python",
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
            False,
            id="not_found",
        ),
    ],
)
def test_search_gist(pattern, gist, expected):
    actual = search_gist(pattern=pattern, gist_object=gist)
    assert actual is expected
