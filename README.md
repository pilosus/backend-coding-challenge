# Documentation

## Requirements

- Python 3.11 or
- Docker (tested against v24.0.6) and optionally (testd against v2.21.0)
- (optionally) GNU Make (tested against v4.4.1)

## Usage

1. Clone the app:

```bash
git clone https://github.com/pilosus/backend-coding-challenge.git
cd backend-coding-challenge
```

2. The app can be run either locally or as a Docker container.

To run locally:

```bash
make install
make serve
```

To run as a docker container:

```bash
docker compose up
```

In case you prefer building and running Docker containers the hard way:

```bash
docker build . -t gistapi:latest
docker run -p 9876:9876 -e GITHUB_TOKEN=your-token -it --rm gistapi:latest
```

3. (optional) GitHub API requests are rate limited. In order to increase limits, 
get your [API token](https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api?apiVersion=2022-11-28). 
Then use as a environment variable `GITHUB_TOKEN` either locally:

```bash
GITHUB_TOKEN=your-bearer-token make serve
```

or add to an `.env` file in case of running the app as container.

4. Request the app API endpoints:

```bash
curl --request GET --url "http://127.0.0.1:9876/ping"

curl --request POST \
  --url "http://127.0.0.1:9876/api/v1/search" \
  --header 'Content-Type: application/json' \
  --data '{"username": "pilosus", "pattern": "(?i)clj-\\w{1}"}'
```

## Development

During the development process running code formatters and static analysis tools are mandatory:

```bash
# install all the deps needed
make install-dev

# lint, format, check type hints
make lint
make types

# run tests and generate code coverage report
make cov 
```

# Challenge

This challenge is divided between the main task and additional stretch goals. All of those stretch goals are optional, but we would love to see them implemented. It is expected that you should be able to finish the challenge in about 1.5 hours. If you feel you are not able to implement everything on time, please, try instead describing how you would solve the points you didn't finish.

And also, please do not hesitate to ask any questions. Good luck!

## gistapi

Gistapi is a simple HTTP API server implemented in Flask for searching a user's public Github Gists.
The existing code already implements most of the Flask boilerplate for you.
The main functionality is left for you to implement.
The goal is to implement an endpoint that searches a user's Gists with a regular expression.
For example, I'd like to know all Gists for user `justdionysus` that contain the pattern `import requests`.
The code in `gistapi.py` contains some comments to help you find your way.

To complete the challenge, you'll have to write some HTTP queries from `Gistapi` to the Github API to pull down each Gist for the target user.
Please don't use a github API client (i.e. using a basic HTTP library like requests or aiohttp or urllib3 is fine but not PyGithub or similar).


## Stretch goals

* Implement a few tests (using a testing framework of your choice)
* In all places where it makes sense, implement data validation, error handling, pagination
* Migrate from `requirements.txt` to `pyproject.toml` (e.g. using [poetry](https://python-poetry.org/))
* Implement a simple Dockerfile
* Implement handling of huge gists
* Set up the necessary tools to ensure code quality (feel free to pick up a set of tools you personally prefer)
* Document how to start the application, how to build the docker image, how to run tests, and (optionally) how to run code quality checkers
* Prepare a TODO.md file describing possible further improvements to the archtiecture:
    - Can we use a database? What for? SQL or NoSQL?
    - How can we protect the api from abusing it?
    - How can we deploy the application in a cloud environment?
    - How can we be sure the application is alive and works as expected when deployed into a cloud environment?
    - Any other topics you may find interesting and/or important to cover
