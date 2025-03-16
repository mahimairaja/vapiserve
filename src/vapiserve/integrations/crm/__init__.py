"""CRM integrations for Vapi tools."""

from .base import CrmProvider
from .hubspot import HubspotProvider

__all__ = [
    "CrmProvider",
    "HubspotProvider",
] 