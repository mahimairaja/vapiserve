"""Scheduling integrations for Vapi tools."""

from .base import CalendarProvider
from .google_calendar import GoogleCalendarProvider
from .outlook_calendar import OutlookCalendarProvider

# Import Cal.com provider if available
try:
    from .cal_com import CalComProvider
    __has_cal_com = True
except ImportError:
    __has_cal_com = False
    # Create a placeholder if needed for type hints
    CalComProvider = None

# Set up __all__ based on available modules
__all__ = [
    "CalendarProvider",
    "GoogleCalendarProvider", 
    "OutlookCalendarProvider",
]

# Add optional providers to __all__ if available
if __has_cal_com:
    __all__.append("CalComProvider") 