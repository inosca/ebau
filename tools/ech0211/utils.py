import json
import sys
from typing import Any, Generator
from xml.dom.minidom import parseString

import tomllib
from requests import HTTPError, Response, Session


def _get_config() -> dict[str, Any]:
    """Parse `config.toml` and return contents as dictionary."""

    try:
        with open("config.toml", "rb") as f:
            config = tomllib.load(f)
    except FileNotFoundError:
        print(
            "Config file 'config.toml' not found. Copy it from "
            "'config.example.toml' and adjust as needed, then try again."
        )
        sys.exit(1)

    return config


config = _get_config()
"""Config taken from `config.toml`."""


endpoint: str = config["ech0211"]["endpoint"]
"""Base endpoint URL for the eCH-0211 API."""


def login(session: Session, client_id: str, client_secret: str) -> Session:
    """Login a requests session for authorized requests.

    Gets an `access_token` for a client ID and secret from keycloak and adds the
    token to the default auth headers of the requests session.
    """

    print(f" > logging in as: {client_id} using secret {client_secret}")

    response = session.post(
        f"{config['auth']['endpoint']}/auth/realms/ebau/protocol/openid-connect/token",
        data={
            "grant_type": "client_credentials",
            "scope": "openid",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    response.raise_for_status()
    token = response.json()["access_token"]
    session.headers.update(
        {
            "authorization": f"Bearer {token}",
            "x-camac-group": str(config["auth"]["group_id"]),
        }
    )

    print(f" > token retrieved successfully for client_id: {client_id}")

    return session


def paginate(session: Session, page: int = 1, limit: int = 1) -> Session:
    """Add pagination params to a requests session."""

    session.params.update(
        {
            "page[number]": page,
            "page[size]": limit,
        }
    )

    return session


def each_client() -> Generator[tuple[Session, str], None, None]:
    """Yield a logged-in session and client ID for each configured client.

    Iterates over the clients defined in `config.toml`, logs in a requests
    session for each one and yields the session together with its client ID.
    """

    for client in config["auth"]["clients"]:
        client_id = client["id"]
        try:
            session = login(Session(), client_id, client["secret"])
        except (HTTPError, KeyError):
            print(f" > failed to retrieve token for client_id: {client_id}")
            continue

        yield session, client_id


def print_delimiter(length: int = 30):
    """Print a horizontal delimiter line of the given length."""

    print("-" * length)


def print_title(string: str):
    """Print a string wrapped in delimiter lines matching its length."""

    length = len(string)
    print_delimiter(length)
    print(string)
    print_delimiter(length)


def print_response(response: Response):
    """Pretty-print a response.

    If the response is JSON or XML, it will format it properly before printing.
    """

    if not response.ok and not str(response.status_code).startswith("4"):
        # Raise error if response is not OK, except for 4xx errors.
        response.raise_for_status()

    content_type = response.headers["content-type"]
    content = response.text

    if "json" in content_type:
        content = json.dumps(response.json(), indent=2)
    elif "xml" in content_type:
        content = parseString(response.text).toprettyxml(indent="  ")

    print_delimiter()
    print(f"{response.request.method} {response.request.url} {response.status_code}")
    print(content)
    print_delimiter()
