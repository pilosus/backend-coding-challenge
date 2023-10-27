import marshmallow
from flask import Flask

import gistapi.errors as e
from gistapi.api import blueprint
from gistapi.client import GitHubClient


def create_app():
    """
    Return basic Flask app factory
    """
    app = Flask(__name__)

    # Clients in the app context
    app.config["http"] = GitHubClient()

    # Blueprints
    app.register_blueprint(blueprint)

    # Error handling
    app.register_error_handler(marshmallow.ValidationError, e.request_validation_error)
    app.register_error_handler(Exception, e.generic_error)

    return app


if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True, host="0.0.0.0", port=9876)
