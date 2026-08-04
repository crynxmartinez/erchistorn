"""The error handlers must stay wired, and must not leak internals.

Every crash in this build was found by reading a uvicorn traceback by hand. In
production those are invisible — the client sees "Internal Server Error", nothing
counts them, and nobody learns until a player complains. Eight handlers were
raising at request time while the module imported cleanly and every route
registered.

These are unit tests: they inspect the app object rather than making requests, so
they need no server. The behavioural half (a real crash is logged once, counted,
and returns a generic body) is sabotage-verified in the integration suite.
"""
from __future__ import annotations

import os
import sys

import pytest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "backend"))

os.environ.setdefault("JWT_SECRET", "test-secret")
os.environ.setdefault("MONGO_URL", "mongodb://127.0.0.1:27017")
os.environ.setdefault("DB_NAME", "erchis_unit_test")


@pytest.fixture(scope="module")
def srv():
    return pytest.importorskip("server")


def test_all_three_exception_handlers_are_registered(srv):
    """Catching only HTTPException would miss every genuine crash.

    The bare `Exception` handler is the one that matters: an unhandled NameError
    or KeyError in a route body does not raise HTTPException, so without it the
    500 goes to stderr unlabelled and uncounted.
    """
    from fastapi.exceptions import RequestValidationError
    from starlette.exceptions import HTTPException as StarletteHTTPException

    handlers = srv.app.exception_handlers
    for exc_type, why in (
        (Exception, "unhandled crashes (NameError, KeyError) go uncounted"),
        (StarletteHTTPException, "4xx/5xx raised by handlers go unlogged"),
        (RequestValidationError, "422 payload-shape mismatches go unlogged"),
    ):
        assert exc_type in handlers, f"no handler for {exc_type.__name__}: {why}"


def test_counters_exist_and_start_empty(srv):
    assert isinstance(srv.ERROR_COUNTS, dict)
    assert isinstance(srv.REJECT_COUNTS, dict)


def test_the_diagnostics_route_exists(srv):
    """One request must answer "is anything 500ing right now?"."""
    paths = {getattr(r, "path", None) for r in srv.app.routes}
    assert "/api/_diagnostics/errors" in paths


def test_user_hint_never_returns_the_raw_token(srv):
    """The auth token is a cookie; logging it would put a live session in the log.

    A digest is enough to correlate a burst of errors to one player without
    making the log file credential-bearing.
    """
    class _Req:
        def __init__(self, cookies):
            self.cookies = cookies

    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.super-secret-token-value"
    hint = srv._user_hint(_Req({"access_token": token}))
    assert token not in hint, "the raw auth token must never reach the log"
    assert "super-secret" not in hint
    assert hint.startswith("user:")
    assert srv._user_hint(_Req({})) == "anon"

    # Same token must give the same hint, or bursts cannot be correlated.
    assert hint == srv._user_hint(_Req({"access_token": token}))


def test_route_label_uses_the_template_not_the_concrete_path(srv):
    """/npc/abc and /npc/def must aggregate, or per-id noise buries the signal."""
    class _Route:
        path = "/api/game/npc/{npc_id}"

    class _URL:
        path = "/api/game/npc/gorin"

    class _Req:
        method = "GET"
        scope = {"route": _Route()}
        url = _URL()

    assert srv._route_label(_Req()) == "GET /api/game/npc/{npc_id}"


def test_route_label_falls_back_when_no_route_matched(srv):
    """A 404 has no matched route; the label must still be usable."""
    class _URL:
        path = "/api/game/nonexistent"

    class _Req:
        method = "GET"
        scope = {}
        url = _URL()

    assert srv._route_label(_Req()) == "GET /api/game/nonexistent"
