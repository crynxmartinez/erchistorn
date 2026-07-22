"""CORS bug-fix regression suite (iteration_8).

Verifies the production CORS fix in /app/backend/server.py lines 2131-2148:
- comma-separated FRONTEND_URL env var
- explicit safelist (localhost:3000 + erchis.online)
- allow_origin_regex fallback for *.emergent.host / *.emergentagent.com /
  *.erchis.online subdomains
- allow_credentials still true, no wildcard

We hit http://localhost:8001 directly (bypassing Cloudflare) to observe the
actual FastAPI CORSMiddleware behaviour. The preview URL is used only for
end-to-end auth regression (goes through Cloudflare which strips/rewrites
some CORS headers).
"""
import os
import secrets
import pytest
import requests

BASE_LOCAL = "http://localhost:8001"
BASE_PREVIEW = os.environ.get("REACT_APP_BACKEND_URL", "").rstrip("/")
if not BASE_PREVIEW:
    # fallback: read from frontend .env
    try:
        with open("/app/frontend/.env") as fh:
            for line in fh:
                if line.startswith("REACT_APP_BACKEND_URL="):
                    BASE_PREVIEW = line.split("=", 1)[1].strip().strip('"').rstrip("/")
                    break
    except Exception:
        pass

PROD_ORIGIN = "https://fantasy-torn-dice.emergent.host"
EVIL_ORIGIN = "https://evil.example.org"


def _preflight(base, path, origin, method="POST"):
    return requests.options(
        f"{base}{path}",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": method,
            "Access-Control-Request-Headers": "content-type",
        },
        timeout=10,
    )


# ---------------- BUG-1: preflight LOGIN from prod origin ----------------
class TestBug1LoginPreflight:
    def test_prod_origin_login_preflight_local(self):
        r = _preflight(BASE_LOCAL, "/api/auth/login", PROD_ORIGIN)
        assert r.status_code in (200, 204), f"got {r.status_code}: {r.text}"
        assert r.headers.get("access-control-allow-origin") == PROD_ORIGIN, \
            f"ACAO must echo exact origin (no wildcard). got={r.headers.get('access-control-allow-origin')!r}"
        assert r.headers.get("access-control-allow-credentials", "").lower() == "true"
        # explicit no-wildcard check
        assert r.headers.get("access-control-allow-origin") != "*"


# ---------------- BUG-2: preflight REGISTER from prod origin ------------
class TestBug2RegisterPreflight:
    def test_prod_origin_register_preflight_local(self):
        r = _preflight(BASE_LOCAL, "/api/auth/register", PROD_ORIGIN)
        assert r.status_code in (200, 204)
        assert r.headers.get("access-control-allow-origin") == PROD_ORIGIN
        assert r.headers.get("access-control-allow-credentials", "").lower() == "true"


# ---------------- BUG-3: real register+me flow from prod origin ---------
class TestBug3RealRegisterFromProdOrigin:
    def test_register_then_me_from_prod_origin_local(self):
        email = f"test_cors_{secrets.token_hex(4)}@erchis.io"
        s = requests.Session()
        r = s.post(
            f"{BASE_LOCAL}/api/auth/register",
            json={"email": email, "password": "password123", "display_name": "CorsTester"},
            headers={"Origin": PROD_ORIGIN},
            timeout=10,
        )
        assert r.status_code == 200, f"register failed: {r.status_code} {r.text}"
        # CORS headers on the actual (non-preflight) response
        assert r.headers.get("access-control-allow-origin") == PROD_ORIGIN
        assert r.headers.get("access-control-allow-credentials", "").lower() == "true"
        # cookies set?
        cookie_names = {c.name for c in s.cookies}
        assert "access_token" in cookie_names, f"access_token cookie not set. got={cookie_names}"
        # follow-up /me should work
        me = s.get(f"{BASE_LOCAL}/api/auth/me", headers={"Origin": PROD_ORIGIN}, timeout=10)
        assert me.status_code == 200, f"/me failed: {me.status_code} {me.text}"
        body = me.json()
        assert body.get("user", {}).get("email") == email
        assert me.headers.get("access-control-allow-origin") == PROD_ORIGIN


# ---------------- BUG-4: reject unknown origins -------------------------
class TestBug4RejectEvilOrigin:
    def test_evil_origin_login_preflight_local(self):
        r = _preflight(BASE_LOCAL, "/api/auth/login", EVIL_ORIGIN)
        # Starlette CORSMiddleware returns 400 for disallowed preflights
        assert r.status_code == 400, f"expected 400, got {r.status_code}"
        # crucial: no ACAO header for evil origin
        acao = r.headers.get("access-control-allow-origin")
        assert acao is None or acao == "", f"evil origin got ACAO={acao!r}"

    def test_evil_origin_actual_post_no_acao_local(self):
        # actual POST from evil origin — browser would already have blocked, but
        # the API should not echo the origin.
        r = requests.post(
            f"{BASE_LOCAL}/api/auth/login",
            json={"email": "x@x.com", "password": "x"},
            headers={"Origin": EVIL_ORIGIN},
            timeout=10,
        )
        acao = r.headers.get("access-control-allow-origin")
        assert acao != EVIL_ORIGIN, f"evil origin was echoed: {acao!r}"
        assert acao != "*"


# ---------------- BUG-5: regex allow for emergent subdomains ------------
class TestBug5RegexAllow:
    @pytest.mark.parametrize(
        "origin",
        [
            "https://foo-bar.emergent.host",
            "https://baz.emergentagent.com",
            "https://erchis.online",
            "https://sub.erchis.online",
            "https://a-b-c.emergent.host",
        ],
    )
    def test_regex_allows_origin(self, origin):
        r = _preflight(BASE_LOCAL, "/api/auth/login", origin)
        assert r.status_code in (200, 204), f"{origin} preflight failed: {r.status_code}"
        assert r.headers.get("access-control-allow-origin") == origin, \
            f"{origin} not echoed. got={r.headers.get('access-control-allow-origin')!r}"
        assert r.headers.get("access-control-allow-credentials", "").lower() == "true"


# ---------------- BUG-6: explicit safelist ------------------------------
class TestBug6Safelist:
    @pytest.mark.parametrize(
        "origin",
        [
            "http://localhost:3000",
            "https://erchis.online",
        ],
    )
    def test_safelist_origin(self, origin):
        r = _preflight(BASE_LOCAL, "/api/auth/login", origin)
        assert r.status_code in (200, 204)
        assert r.headers.get("access-control-allow-origin") == origin

    def test_frontend_url_env_origin(self):
        # FRONTEND_URL env value must also be allowed
        fu = os.environ.get("FRONTEND_URL")
        if not fu:
            # read from backend/.env
            try:
                with open("/app/backend/.env") as fh:
                    for line in fh:
                        if line.startswith("FRONTEND_URL="):
                            fu = line.split("=", 1)[1].strip().strip('"')
                            break
            except Exception:
                pass
        if not fu:
            pytest.skip("FRONTEND_URL not set")
        for origin in [o.strip() for o in fu.split(",") if o.strip()]:
            r = _preflight(BASE_LOCAL, "/api/auth/login", origin)
            assert r.status_code in (200, 204), f"{origin}: {r.status_code}"
            assert r.headers.get("access-control-allow-origin") == origin, \
                f"env origin {origin} not echoed"


# ---------------- REGRESSION 1: preview URL end-to-end ------------------
class TestRegressionPreviewURL:
    def test_preview_register_and_me(self):
        if not BASE_PREVIEW:
            pytest.skip("REACT_APP_BACKEND_URL not set")
        email = f"test_reg1_{secrets.token_hex(4)}@erchis.io"
        s = requests.Session()
        r = s.post(
            f"{BASE_PREVIEW}/api/auth/register",
            json={"email": email, "password": "password123", "display_name": "RegTester"},
            timeout=20,
        )
        assert r.status_code == 200, f"preview register failed: {r.status_code} {r.text}"
        cookie_names = {c.name for c in s.cookies}
        assert "access_token" in cookie_names, f"cookies not set: {cookie_names}"
        me = s.get(f"{BASE_PREVIEW}/api/auth/me", timeout=20)
        assert me.status_code == 200
        assert me.json().get("user", {}).get("email") == email


# ---------------- REGRESSION 2: rest of app still works ------------------
class TestRegressionAppEndpoints:
    @pytest.fixture(scope="class")
    def auth_session(self):
        if not BASE_PREVIEW:
            pytest.skip("REACT_APP_BACKEND_URL not set")
        email = f"test_reg2_{secrets.token_hex(4)}@erchis.io"
        s = requests.Session()
        r = s.post(
            f"{BASE_PREVIEW}/api/auth/register",
            json={"email": email, "password": "password123", "display_name": "R2"},
            timeout=20,
        )
        assert r.status_code == 200
        # create a character so /game/character returns real data
        r2 = s.post(
            f"{BASE_PREVIEW}/api/game/character",
            json={"name": "TestRegChar", "race": "human", "class_id": "fighter"},
            timeout=20,
        )
        assert r2.status_code in (200, 201), f"char create: {r2.status_code} {r2.text}"
        return s

    def test_game_character(self, auth_session):
        r = auth_session.get(f"{BASE_PREVIEW}/api/game/character", timeout=20)
        assert r.status_code == 200
        assert "character" in r.json()

    def test_game_leaderboard(self, auth_session):
        r = auth_session.get(f"{BASE_PREVIEW}/api/game/leaderboard", timeout=20)
        assert r.status_code == 200

    def test_game_events(self, auth_session):
        r = auth_session.get(f"{BASE_PREVIEW}/api/game/events", timeout=20)
        assert r.status_code == 200
