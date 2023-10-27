"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""

from flask import Flask, jsonify, request, current_app, Blueprint

from .helpers import search_gist
from .client import GitHubClient

app = Blueprint("main", __name__)


def create_app():
    """
    Return basic Flask app factory
    """
    flask_app = Flask(__name__)
    flask_app.config["http"] = GitHubClient()
    flask_app.register_blueprint(app)
    return flask_app


@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "pong"


@app.route("/api/v1/users/<username>/gists")
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


@app.route("/api/v1/gists/<gist_id>")
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


@app.route("/api/v1/search", methods=['POST'])
def search():
    """Provides matches for a single pattern across a single users gists.

    Pulls down a list of all gists for a given user and then searches
    each gist for a given regular expression.

    Returns:
        A Flask Response object of type application/json.  The result
        object contains the list of matches along with a 'status' key
        indicating any failure conditions.
    """
    post_data = request.get_json()

    username = post_data['username']
    pattern = post_data['pattern']

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


if __name__ == '__main__':
    my_app = create_app()
    my_app.run(debug=True, host='0.0.0.0', port=9876)
