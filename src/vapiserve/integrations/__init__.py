"""Integrations for VapiServe.

This module includes ready-to-use tools for integrating with various services.
"""

__all__ = []

# Import from scheduling module
try:
    from .scheduling import (
        GoogleCalendarProvider,
        OutlookCalendarProvider,
        CalendarProvider
    )
    
    __all__.extend([
        "CalendarProvider",
        "GoogleCalendarProvider", 
        "OutlookCalendarProvider",
    ])
except ImportError:
    pass

# Import other integration modules as they are implemented 