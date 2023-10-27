"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""

from flask import jsonify, request, current_app, Blueprint

from gistapi.helpers import search_gist
from gistapi.schemas import SearchSchema

blueprint = Blueprint("main", __name__)


@blueprint.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"


@blueprint.route("/api/v1/users/<username>/gists")
def gists_for_user(username: str):
    """Provides the list of gist metadata for a given user.

    This abstracts the /users/:username/gist endpoint from the Github API.
    See https://developer.github.com/v3/gists/#list-a-users-gists for
    more information.

    Args:
        username (string): the user to query gists for

    Returns:
        The dict parsed from the json response from the Github API.  See
        the above URL for details of the expected structure.
    """
    gists_url = '/users/{username}/gists'.format(username=username)
    return current_app.config["http"].request(method="GET", url=gists_url)


@blueprint.route("/api/v1/gists/<gist_id>")
def get_gist(gist_id: str):
    """Provides the gist data for a given gist id.

    This abstracts the /gists/:gist_id endpoint from the Github API.
    See https://developer.github.com/v3/gists/#get-a-gist for
    more information.

    Args:
        gist_id (string): the unique identifier of the gist.

    Returns:
        The dict parsed from the json response from the Github API.  See
        the above URL for details of the expected structure.
    """
    # gist_url = 'https://api.github.com/gists/{gist_id}'.format(gist_id=gist_id)
    # response = http(method="GET", url=gist_url)
    gist_url = '/gists/{gist_id}'.format(gist_id=gist_id)
    return current_app.config["http"].request(method="GET", url=gist_url)


@blueprint.route("/api/v1/search", methods=['POST'])
def search():
    """Provides matches for a single pattern across a single users gists.

    Pulls down a list of all gists for a given user and then searches
    each gist for a given regular expression.

    Returns:
        A Flask Response object of type application/json.  The result
        object contains the list of matches along with a 'status' key
        indicating any failure conditions.
    """
    request_data = SearchSchema().load(request.get_json())
    username = request_data['username']
    pattern = request_data['pattern']

    result = {
        "status": "success",
        "username": username,
        "pattern": pattern,
        "matches": [],
    }
    gists = gists_for_user(username)

    for gist in gists:
        gist_id = gist.get("id")
        gist_object = get_gist(gist_id)
        if search_gist(pattern=pattern, gist_object=gist_object):
            result["matches"].append(gist.get("html_url"))

    return jsonify(result)
