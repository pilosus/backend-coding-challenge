import pytest
from gistapi.api import create_app


def pytest_make_parametrize_id(config, val, argname):
    """
    Prettify output for parametrized tests
    """
    if isinstance(val, dict):
        return "{}({})".format(
            argname, ", ".join("{}={}".format(k, v) for k, v in val.items())
        )


@pytest.fixture
def application(request):
    """
    Flask app pushed into app context
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
        # TODO set up
        yield app
        # TODO tear down


@pytest.fixture
def client(request, application):
    """
    Werkzeug test client used primarily for GET/POST/etc requests

    Usage:
        client.get(url)
        client.post(url, data=dict(), follow_redirects=True)
    """
    return application.test_client()
