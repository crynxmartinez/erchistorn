"""Async email service for transactional emails (password reset, etc.)."""
from __future__ import annotations

import logging
import os

import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger("erchis")


def _smtp_config() -> dict:
    return {
        "host": os.environ.get("SMTP_HOST", ""),
        "port": int(os.environ.get("SMTP_PORT", "587")),
        "user": os.environ.get("SMTP_USER", ""),
        "pass": os.environ.get("SMTP_PASS", ""),
        "from": os.environ.get("FROM_EMAIL", "noreply@erchis.online"),
    }


def is_email_configured() -> bool:
    cfg = _smtp_config()
    return bool(cfg["host"] and cfg["user"] and cfg["pass"])


async def send_email(to: str, subject: str, html_body: str, text_body: str = "") -> bool:
    """Send a transactional email. Returns True on success, False on failure."""
    cfg = _smtp_config()
    if not is_email_configured():
        logger.warning("SMTP not configured — email to %s not sent", to)
        return False

    msg = MIMEMultipart("alternative")
    msg["From"] = cfg["from"]
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(text_body or subject, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        await aiosmtplib.send(
            msg,
            hostname=cfg["host"],
            port=cfg["port"],
            username=cfg["user"],
            password=cfg["pass"],
            start_tls=True,
        )
        logger.info("Email sent to %s: %s", to, subject)
        return True
    except Exception as e:
        logger.error("Failed to send email to %s: %s", to, e)
        return False


async def send_password_reset_email(to: str, reset_url: str) -> bool:
    """Send a password reset email with a styled HTML template."""
    html = f"""\
<div style="font-family: 'JetBrains Mono', monospace; max-width: 480px; margin: 0 auto; padding: 24px; background: #1a1a2e; color: #e0e0e0; border: 1px solid #444;">
  <h2 style="color: #d4af37; text-transform: uppercase; letter-spacing: 0.1em; font-size: 20px; margin-bottom: 16px;">Erchis — Password Reset</h2>
  <p style="font-size: 14px; line-height: 1.6; color: #b0b0b0;">
    A password reset was requested for your Erchis account. If this was you, click the link below to choose a new password. The link expires in 15 minutes.
  </p>
  <p style="margin: 24px 0;">
    <a href="{reset_url}" style="display: inline-block; padding: 12px 24px; background: #d4af37; color: #1a1a2e; text-decoration: none; font-weight: bold; text-transform: uppercase; letter-spacing: 0.05em; border: 2px solid #d4af37;">
      Reset Password
    </a>
  </p>
  <p style="font-size: 12px; color: #777; line-height: 1.5;">
    If you did not request a password reset, you can safely ignore this email. Your password has not been changed.
  </p>
  <hr style="border: none; border-top: 1px solid #333; margin: 24px 0;">
  <p style="font-size: 11px; color: #555;">Erchis Fantasy Dice RPG — erchis.online</p>
</div>"""
    text = f"Erchis — Password Reset\n\nA password reset was requested for your account. Visit this link to reset your password (expires in 15 minutes):\n{reset_url}\n\nIf you did not request this, ignore this email."
    return await send_email(to, "Erchis — Password Reset", html, text)
