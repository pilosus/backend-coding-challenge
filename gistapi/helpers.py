import re
from typing import Any


def search_file(pattern: str, content: str) -> bool:
    """
    Return True if given pattern produces a match for anywhere in a given content string, False otherwise
    """
    return bool(re.search(pattern, content))


def search_gist(pattern: str, gist_object: dict[str, Any]) -> bool:
    """
    Given a get_gist handler response and a pattern string,
    return True if the content of any file of the gist matches the pattern; return False otherwise
    """
    for file_name, file_data in gist_object.get("files", {}).items():
        content = file_data.get("content")
        if search_file(pattern=pattern, content=content):
            return True

    return False
