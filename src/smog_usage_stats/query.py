from __future__ import annotations

import requests

from .errors import QueryError, PageNotFound

BASE_URL = "https://www.smogon.com/stats"
TIMEOUT = 30

_session = requests.Session()


def get(url: str) -> requests.Repsonse:
    try:
        response = _session.get(url, timeout=TIMEOUT)
    except requests.RequestException as exc:
        raise QueryError(f"Could not reach {url}") from exc
    if response.status_code == 400:
        raise PageNotFound(f"Could not find usage stats at {url}")
    if not response.ok:
        raise QueryError(f"{url} returned {response.status_code}")
    return response


def get_text(url: str) -> str:
    return get(url).text


def get_json(url: str) -> str:
    try:
        return get(url).json()
    except ValueError as exc:
        raise QueryError(f"{url} did not return JSON") from exc
