"""OAuth 2.0 provider configs and helpers for Google, Microsoft, Facebook."""
from __future__ import annotations

import os
import secrets
import urllib.parse

import httpx


# ============================================================
# Provider configurations
# ============================================================
PROVIDERS: dict[str, dict] = {
    "google": {
        "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "userinfo_url": "https://www.googleapis.com/oauth2/v3/userinfo",
        "scope": "openid email profile",
        "client_id": os.environ.get("GOOGLE_CLIENT_ID", ""),
        "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET", ""),
    },
    "microsoft": {
        "auth_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
        "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        "userinfo_url": "https://graph.microsoft.com/oidc/userinfo",
        "scope": "openid email profile User.Read",
        "client_id": os.environ.get("MICROSOFT_CLIENT_ID", ""),
        "client_secret": os.environ.get("MICROSOFT_CLIENT_SECRET", ""),
    },
    "facebook": {
        "auth_url": "https://www.facebook.com/v18.0/dialog/oauth",
        "token_url": "https://graph.facebook.com/v18.0/oauth/access_token",
        "userinfo_url": "https://graph.facebook.com/me",
        "scope": "email public_profile",
        "client_id": os.environ.get("FACEBOOK_CLIENT_ID", ""),
        "client_secret": os.environ.get("FACEBOOK_CLIENT_SECRET", ""),
    },
}


def get_redirect_base() -> str:
    return os.environ.get("OAUTH_REDIRECT_BASE", "http://localhost:8000/api").rstrip("/")


def get_provider(provider: str) -> dict | None:
    return PROVIDERS.get(provider)


def is_provider_configured(provider: str) -> bool:
    cfg = PROVIDERS.get(provider)
    return bool(cfg and cfg["client_id"] and cfg["client_secret"])


def build_auth_url(provider: str, state: str) -> str:
    cfg = PROVIDERS[provider]
    redirect_uri = f"{get_redirect_base()}/auth/oauth/{provider}/callback"
    params = {
        "client_id": cfg["client_id"],
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": cfg["scope"],
        "state": state,
    }
    return f"{cfg['auth_url']}?{urllib.parse.urlencode(params)}"


def generate_state() -> str:
    return secrets.token_urlsafe(32)


async def exchange_code(provider: str, code: str) -> dict:
    cfg = PROVIDERS[provider]
    redirect_uri = f"{get_redirect_base()}/auth/oauth/{provider}/callback"
    data = {
        "client_id": cfg["client_id"],
        "client_secret": cfg["client_secret"],
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(cfg["token_url"], data=data, timeout=15)
        resp.raise_for_status()
        return resp.json()


async def get_user_info(provider: str, access_token: str) -> dict:
    cfg = PROVIDERS[provider]
    async with httpx.AsyncClient() as client:
        if provider == "facebook":
            resp = await client.get(
                cfg["userinfo_url"],
                params={"fields": "id,name,email,picture", "access_token": access_token},
                timeout=15,
            )
        else:
            resp = await client.get(
                cfg["userinfo_url"],
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=15,
            )
        resp.raise_for_status()
        data = resp.json()

    if provider == "google":
        return {
            "email": data.get("email", "").lower(),
            "name": data.get("name", ""),
            "provider_id": data.get("sub", ""),
            "avatar": data.get("picture", ""),
        }
    elif provider == "microsoft":
        return {
            "email": data.get("email", "").lower(),
            "name": data.get("name", ""),
            "provider_id": data.get("sub", ""),
            "avatar": "",
        }
    elif provider == "facebook":
        return {
            "email": data.get("email", "").lower(),
            "name": data.get("name", ""),
            "provider_id": data.get("id", ""),
            "avatar": data.get("picture", {}).get("data", {}).get("url", ""),
        }
    return data
