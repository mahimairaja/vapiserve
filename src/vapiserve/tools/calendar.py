"""Calendar tools for Vapi."""

from typing import Any, Dict, List, Optional

from ..core.tool import tool
from ..utils.security import require_api_key
from ..integrations.scheduling import GoogleCalendarProvider, OutlookCalendarProvider


@tool(
    name="calendar_create_event",
    description="Create a new event in a calendar",
    group="calendar"
)
async def create_calendar_event(
    provider: str,
    summary: str,
    start_time: str,
    end_time: str,
    timezone: str = "UTC",
    location: Optional[str] = None,
    description: Optional[str] = None,
    attendees: Optional[List[str]] = None,
    credentials_json: Optional[str] = None,
    credentials_path: Optional[str] = None,
    service_account_path: Optional[str] = None,
    impersonate_user: Optional[str] = None,
    calendar_id: str = "primary",
) -> Dict[str, Any]:
    """Create a new event in a calendar.
    
    Args:
        provider: Calendar provider type (google, microsoft)
        summary: Title of the event
        start_time: Start time in ISO format (e.g., "2023-09-15T09:00:00")
        end_time: End time in ISO format (e.g., "2023-09-15T10:00:00")
        timezone: Timezone for the event (default: UTC)
        location: Optional location for the event
        description: Optional description for the event
        attendees: Optional list of email addresses for attendees
        credentials_json: Optional JSON string with provider credentials
        credentials_path: Optional path to credentials JSON file
        service_account_path: Optional path to service account JSON file
        impersonate_user: Optional email to impersonate (for service accounts)
        calendar_id: Calendar ID to use (default: "primary")
        
    Returns:
        Dict with event ID and creation status
    """
    if provider.lower() == "google":
        # Determine which credentials to use
        if service_account_path:
            calendar = GoogleCalendarProvider(
                service_account_path, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        elif credentials_path:
            calendar = GoogleCalendarProvider(
                credentials_path, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        elif credentials_json:
            calendar = GoogleCalendarProvider(
                credentials_json, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        else:
            # Try to get from environment
            creds = require_api_key("GOOGLE_TOKEN_JSON")
            calendar = GoogleCalendarProvider(
                creds, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
    elif provider.lower() == "microsoft":
        if credentials_json:
            # Direct token mode
            calendar = OutlookCalendarProvider(token=credentials_json)
        else:
            # Try to get from environment
            token = require_api_key("MICROSOFT_TOKEN")
            calendar = OutlookCalendarProvider(token=token)
    else:
        raise ValueError(f"Unsupported calendar provider: {provider}")
        
    return calendar.create_event(
        summary=summary,
        start_time=start_time,
        end_time=end_time,
        timezone=timezone,
        location=location,
        description=description,
        attendees=attendees,
    )


@tool(
    name="calendar_list_events",
    description="List upcoming events from a calendar",
    group="calendar"
)
async def list_calendar_events(
    provider: str,
    max_results: int = 10,
    time_min: Optional[str] = None,
    time_max: Optional[str] = None,
    credentials_json: Optional[str] = None,
    credentials_path: Optional[str] = None,
    service_account_path: Optional[str] = None,
    impersonate_user: Optional[str] = None,
    calendar_id: str = "primary",
) -> List[Dict[str, Any]]:
    """List upcoming events from a calendar.
    
    Args:
        provider: Calendar provider type (google, microsoft)
        max_results: Maximum number of events to return
        time_min: Optional start time in ISO format (default: now)
        time_max: Optional end time in ISO format
        credentials_json: Optional JSON string with provider credentials
        credentials_path: Optional path to credentials JSON file
        service_account_path: Optional path to service account JSON file
        impersonate_user: Optional email to impersonate (for service accounts)
        calendar_id: Calendar ID to use (default: "primary")
        
    Returns:
        List of events with their details
    """
    if provider.lower() == "google":
        # Determine which credentials to use
        if service_account_path:
            calendar = GoogleCalendarProvider(
                service_account_path, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        elif credentials_path:
            calendar = GoogleCalendarProvider(
                credentials_path, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        elif credentials_json:
            calendar = GoogleCalendarProvider(
                credentials_json, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        else:
            # Try to get from environment
            creds = require_api_key("GOOGLE_TOKEN_JSON")
            calendar = GoogleCalendarProvider(
                creds, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
    elif provider.lower() == "microsoft":
        if credentials_json:
            # Direct token mode
            calendar = OutlookCalendarProvider(token=credentials_json)
        else:
            # Try to get from environment
            token = require_api_key("MICROSOFT_TOKEN")
            calendar = OutlookCalendarProvider(token=token)
    else:
        raise ValueError(f"Unsupported calendar provider: {provider}")
        
    return calendar.list_events(
        max_results=max_results,
        time_min=time_min,
        time_max=time_max,
    )


@tool(
    name="calendar_get_event",
    description="Get details of a specific event from a calendar",
    group="calendar"
)
async def get_calendar_event(
    provider: str,
    event_id: str,
    credentials_json: Optional[str] = None,
    credentials_path: Optional[str] = None,
    service_account_path: Optional[str] = None,
    impersonate_user: Optional[str] = None,
    calendar_id: str = "primary",
) -> Dict[str, Any]:
    """Get details of a specific event from a calendar.
    
    Args:
        provider: Calendar provider type (google, microsoft)
        event_id: ID of the event to retrieve
        credentials_json: Optional JSON string with provider credentials
        credentials_path: Optional path to credentials JSON file
        service_account_path: Optional path to service account JSON file
        impersonate_user: Optional email to impersonate (for service accounts)
        calendar_id: Calendar ID to use (default: "primary")
        
    Returns:
        Dict with event details
    """
    if provider.lower() == "google":
        # Determine which credentials to use
        if service_account_path:
            calendar = GoogleCalendarProvider(
                service_account_path, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        elif credentials_path:
            calendar = GoogleCalendarProvider(
                credentials_path, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        elif credentials_json:
            calendar = GoogleCalendarProvider(
                credentials_json, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        else:
            # Try to get from environment
            creds = require_api_key("GOOGLE_TOKEN_JSON")
            calendar = GoogleCalendarProvider(
                creds, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
    elif provider.lower() == "microsoft":
        if credentials_json:
            # Direct token mode
            calendar = OutlookCalendarProvider(token=credentials_json)
        else:
            # Try to get from environment
            token = require_api_key("MICROSOFT_TOKEN")
            calendar = OutlookCalendarProvider(token=token)
    else:
        raise ValueError(f"Unsupported calendar provider: {provider}")
        
    return calendar.get_event(event_id=event_id)


@tool(
    name="calendar_update_event",
    description="Update an existing event in a calendar",
    group="calendar"
)
async def update_calendar_event(
    provider: str,
    event_id: str,
    summary: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    timezone: Optional[str] = None,
    location: Optional[str] = None,
    description: Optional[str] = None,
    attendees: Optional[List[str]] = None,
    credentials_json: Optional[str] = None,
    credentials_path: Optional[str] = None,
    service_account_path: Optional[str] = None,
    impersonate_user: Optional[str] = None,
    calendar_id: str = "primary",
) -> Dict[str, Any]:
    """Update an existing event in a calendar.
    
    Args:
        provider: Calendar provider type (google, microsoft)
        event_id: ID of the event to update
        summary: Optional new title
        start_time: Optional new start time
        end_time: Optional new end time
        timezone: Optional new timezone
        location: Optional new location
        description: Optional new description
        attendees: Optional new list of attendees
        credentials_json: Optional JSON string with provider credentials
        credentials_path: Optional path to credentials JSON file
        service_account_path: Optional path to service account JSON file
        impersonate_user: Optional email to impersonate (for service accounts)
        calendar_id: Calendar ID to use (default: "primary")
        
    Returns:
        Dict with updated event details
    """
    if provider.lower() == "google":
        # Determine which credentials to use
        if service_account_path:
            calendar = GoogleCalendarProvider(
                service_account_path, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        elif credentials_path:
            calendar = GoogleCalendarProvider(
                credentials_path, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        elif credentials_json:
            calendar = GoogleCalendarProvider(
                credentials_json, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        else:
            # Try to get from environment
            creds = require_api_key("GOOGLE_TOKEN_JSON")
            calendar = GoogleCalendarProvider(
                creds, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
    elif provider.lower() == "microsoft":
        if credentials_json:
            # Direct token mode
            calendar = OutlookCalendarProvider(token=credentials_json)
        else:
            # Try to get from environment
            token = require_api_key("MICROSOFT_TOKEN")
            calendar = OutlookCalendarProvider(token=token)
    else:
        raise ValueError(f"Unsupported calendar provider: {provider}")
        
    return calendar.update_event(
        event_id=event_id,
        summary=summary,
        start_time=start_time,
        end_time=end_time,
        timezone=timezone,
        location=location,
        description=description,
        attendees=attendees,
    )


@tool(
    name="calendar_delete_event",
    description="Delete an event from a calendar",
    group="calendar"
)
async def delete_calendar_event(
    provider: str,
    event_id: str,
    credentials_json: Optional[str] = None,
    credentials_path: Optional[str] = None,
    service_account_path: Optional[str] = None,
    impersonate_user: Optional[str] = None,
    calendar_id: str = "primary",
) -> Dict[str, Any]:
    """Delete an event from a calendar.
    
    Args:
        provider: Calendar provider type (google, microsoft)
        event_id: ID of the event to delete
        credentials_json: Optional JSON string with provider credentials
        credentials_path: Optional path to credentials JSON file
        service_account_path: Optional path to service account JSON file
        impersonate_user: Optional email to impersonate (for service accounts)
        calendar_id: Calendar ID to use (default: "primary")
        
    Returns:
        Dict with deletion status
    """
    if provider.lower() == "google":
        # Determine which credentials to use
        if service_account_path:
            calendar = GoogleCalendarProvider(
                service_account_path, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        elif credentials_path:
            calendar = GoogleCalendarProvider(
                credentials_path, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        elif credentials_json:
            calendar = GoogleCalendarProvider(
                credentials_json, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        else:
            # Try to get from environment
            creds = require_api_key("GOOGLE_TOKEN_JSON")
            calendar = GoogleCalendarProvider(
                creds, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
    elif provider.lower() == "microsoft":
        if credentials_json:
            # Direct token mode
            calendar = OutlookCalendarProvider(token=credentials_json)
        else:
            # Try to get from environment
            token = require_api_key("MICROSOFT_TOKEN")
            calendar = OutlookCalendarProvider(token=token)
    else:
        raise ValueError(f"Unsupported calendar provider: {provider}")
        
    result = calendar.delete_event(event_id=event_id)
    
    # Handle the different return types (bool vs dict)
    if isinstance(result, bool):
        return {
            "event_id": event_id,
            "status": "deleted" if result else "failed"
        }
    return result


@tool(
    name="get_free_busy_times",
    description="Get free/busy information for a calendar",
    group="calendar"
)
async def get_free_busy_times(
    provider: str,
    time_min: str,
    time_max: str,
    credentials_json: Optional[str] = None,
    credentials_path: Optional[str] = None,
    service_account_path: Optional[str] = None,
    impersonate_user: Optional[str] = None,
    calendar_id: str = "primary",
) -> Dict[str, Any]:
    """Get free/busy information for a calendar.
    
    Args:
        provider: Calendar provider type (google, microsoft)
        time_min: Start time in ISO format (e.g., "2023-09-15T09:00:00")
        time_max: End time in ISO format (e.g., "2023-09-15T17:00:00")
        credentials_json: Optional JSON string with provider credentials
        credentials_path: Optional path to credentials JSON file
        service_account_path: Optional path to service account JSON file
        impersonate_user: Optional email to impersonate (for service accounts)
        calendar_id: Calendar ID to use (default: "primary")
        
    Returns:
        Dict with busy periods
    """
    if provider.lower() == "google":
        # Determine which credentials to use
        if service_account_path:
            calendar = GoogleCalendarProvider(
                service_account_path, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        elif credentials_path:
            calendar = GoogleCalendarProvider(
                credentials_path, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        elif credentials_json:
            calendar = GoogleCalendarProvider(
                credentials_json, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
        else:
            # Try to get from environment
            creds = require_api_key("GOOGLE_TOKEN_JSON")
            calendar = GoogleCalendarProvider(
                creds, 
                calendar_id=calendar_id,
                impersonate_user=impersonate_user
            )
    elif provider.lower() == "microsoft":
        if credentials_json:
            # Direct token mode
            calendar = OutlookCalendarProvider(token=credentials_json)
        else:
            # Try to get from environment
            token = require_api_key("MICROSOFT_TOKEN")
            calendar = OutlookCalendarProvider(token=token)
    else:
        raise ValueError(f"Unsupported calendar provider: {provider}")
        
    return calendar.get_free_busy(
        time_min=time_min,
        time_max=time_max,
    ) 