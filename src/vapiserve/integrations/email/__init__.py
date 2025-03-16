"""Email service integrations for Vapi tools."""

from .base import EmailProvider
from .sendgrid import SendGridProvider

__all__ = [
    "EmailProvider",
    "SendGridProvider",
] 