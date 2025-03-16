"""Microsoft Outlook Calendar integration."""

import os
from typing import Any, Dict, List, Optional, Union

try:
    from msal import ConfidentialClientApplication
    HAS_MSAL = True
except ImportError:
    HAS_MSAL = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

from .base import CalendarProvider


class OutlookCalendarProvider(CalendarProvider):
    """Microsoft Outlook Calendar integration using Microsoft Graph API."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        tenant_id: Optional[str] = None,
        credentials_path: Optional[str] = None,
        token: Optional[str] = None,
    ):
        """Initialize the Outlook Calendar provider.
        
        Args:
            client_id: Microsoft application client ID
            client_secret: Microsoft application client secret
            tenant_id: Microsoft tenant ID
            credentials_path: Path to a JSON file containing credentials
            token: Direct access token for Microsoft Graph API
        """
        if not HAS_REQUESTS:
            raise ImportError(
                "Requests library not installed. "
                "Install with 'pip install requests'"
            )
        
        # Setup API base URL
        self.api_base = "https://graph.microsoft.com/v1.0"
        
        if token:
            # Direct token provided (legacy mode)
            self.token = token
            self.headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
            return
            
        if not HAS_MSAL:
            raise ImportError(
                "The 'msal' package is required for Outlook Calendar integration. "
                "Install it with 'pip install msal'."
            )
            
        # Read credentials from environment variables if not provided
        self.client_id = client_id or os.environ.get("OUTLOOK_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("OUTLOOK_CLIENT_SECRET")
        self.tenant_id = tenant_id or os.environ.get("OUTLOOK_TENANT_ID")
        
        if credentials_path:
            # TODO: Implement loading credentials from file
            pass
            
        if not self.client_id or not self.client_secret or not self.tenant_id:
            raise ValueError(
                "Missing required credentials for Outlook Calendar. "
                "Provide client_id, client_secret, and tenant_id or set "
                "OUTLOOK_CLIENT_ID, OUTLOOK_CLIENT_SECRET, and OUTLOOK_TENANT_ID "
                "environment variables."
            )
            
        # Initialize the MSAL client
        self.app = ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}"
        )
        
        # Token will be acquired by _ensure_token
        self.token = None 
        self._ensure_token()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        
    def _ensure_token(self):
        """Ensure a valid access token is available."""
        if not self.token:
            # TODO: Implement token acquisition and refresh logic
            # This is a placeholder
            scopes = ["https://graph.microsoft.com/.default"]
            result = self.app.acquire_token_for_client(scopes=scopes)
            if "access_token" in result:
                self.token = result["access_token"]
            else:
                raise ValueError(f"Failed to acquire token: {result.get('error_description', 'Unknown error')}")
        
    def create_event(
        self, 
        summary: str, 
        start_time: str, 
        end_time: str, 
        timezone: str = "UTC",
        location: Optional[str] = None,
        description: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a calendar event in Outlook.
        
        Args:
            summary: Event title/summary
            start_time: Start time in ISO format
            end_time: End time in ISO format
            timezone: Timezone for the event
            location: Optional location for the event
            description: Optional description for the event
            attendees: Optional list of email addresses for attendees
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the created event details
        """
        self._ensure_token()
        
        url = f"{self.api_base}/me/events"
        
        # Prepare the event
        event_data = {
            "subject": summary,
            "body": {
                "contentType": "text",
                "content": description or "",
            },
            "start": {
                "dateTime": start_time,
                "timeZone": timezone,
            },
            "end": {
                "dateTime": end_time,
                "timeZone": timezone,
            },
        }
        
        # Add location if provided
        if location:
            event_data["location"] = {
                "displayName": location,
            }
            
        # Add attendees if provided
        if attendees:
            event_data["attendees"] = [
                {
                    "emailAddress": {
                        "address": email,
                    },
                    "type": "required",
                }
                for email in attendees
            ]
            
        # Create the event
        response = requests.post(url, headers=self.headers, json=event_data)
        response.raise_for_status()
        event_result = response.json()
        
        return {
            "event_id": event_result["id"],
            "status": "created",
            "link": event_result.get("webLink", ""),
        }
    
    def list_events(
        self, 
        time_min: Optional[str] = None, 
        time_max: Optional[str] = None, 
        max_results: int = 10, 
        **kwargs
    ) -> List[Dict[str, Any]]:
        """List Outlook calendar events in a specified time range.
        
        Args:
            time_min: Start time for listing events (ISO format)
            time_max: End time for listing events (ISO format)
            max_results: Maximum number of events to return
            **kwargs: Additional parameters
            
        Returns:
            List of events matching the criteria
        """
        self._ensure_token()
        
        url = f"{self.api_base}/me/events"
        params = {"$top": max_results}
        
        # Add time filter if provided
        if time_min or time_max:
            filter_parts = []
            if time_min:
                filter_parts.append(f"start/dateTime ge '{time_min}'")
            if time_max:
                filter_parts.append(f"start/dateTime le '{time_max}'")
            
            if filter_parts:
                params["$filter"] = " and ".join(filter_parts)
                
        # Get events
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        events_result = response.json()
        
        events = events_result.get("value", [])
        
        # Format events for the response
        formatted_events = []
        for event in events:
            formatted_events.append({
                "id": event["id"],
                "summary": event.get("subject", "No Title"),
                "start": event["start"]["dateTime"],
                "end": event["end"]["dateTime"],
                "location": event.get("location", {}).get("displayName", ""),
                "description": event.get("body", {}).get("content", ""),
                "link": event.get("webLink", ""),
            })
        
        return formatted_events
    
    def get_event(self, event_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific Outlook calendar event by ID.
        
        Args:
            event_id: ID of the event to retrieve
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the event details
        """
        self._ensure_token()
        
        url = f"{self.api_base}/me/events/{event_id}"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        event = response.json()
        
        attendees = []
        for attendee in event.get("attendees", []):
            if "emailAddress" in attendee and "address" in attendee["emailAddress"]:
                attendees.append(attendee["emailAddress"]["address"])
        
        return {
            "id": event["id"],
            "summary": event.get("subject", "No Title"),
            "start": event["start"]["dateTime"],
            "end": event["end"]["dateTime"],
            "location": event.get("location", {}).get("displayName", ""),
            "description": event.get("body", {}).get("content", ""),
            "link": event.get("webLink", ""),
            "attendees": attendees,
        }
    
    def update_event(
        self, 
        event_id: str, 
        summary: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        timezone: Optional[str] = None,
        location: Optional[str] = None,
        description: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Update an existing Outlook calendar event.
        
        Args:
            event_id: ID of the event to update
            summary: Optional new title
            start_time: Optional new start time
            end_time: Optional new end time
            timezone: Optional new timezone
            location: Optional new location
            description: Optional new description
            attendees: Optional new list of attendees
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the updated event details
        """
        self._ensure_token()
        
        url = f"{self.api_base}/me/events/{event_id}"
        
        # Get current event to preserve existing values
        current_event = self.get_event(event_id)
        
        # Prepare the update data
        update_data = {}
        
        if summary:
            update_data["subject"] = summary
            
        if description:
            update_data["body"] = {
                "contentType": "text",
                "content": description,
            }
            
        if start_time:
            tz = timezone or "UTC"
            update_data["start"] = {
                "dateTime": start_time,
                "timeZone": tz,
            }
            
        if end_time:
            tz = timezone or "UTC"
            update_data["end"] = {
                "dateTime": end_time,
                "timeZone": tz,
            }
            
        if location:
            update_data["location"] = {
                "displayName": location,
            }
            
        if attendees:
            update_data["attendees"] = [
                {
                    "emailAddress": {
                        "address": email,
                    },
                    "type": "required",
                }
                for email in attendees
            ]
            
        # Update the event
        response = requests.patch(url, headers=self.headers, json=update_data)
        response.raise_for_status()
        
        return {
            "event_id": event_id,
            "status": "updated",
        }
    
    def delete_event(self, event_id: str, **kwargs) -> bool:
        """Delete an Outlook calendar event.
        
        Args:
            event_id: ID of the event to delete
            **kwargs: Additional parameters
            
        Returns:
            True if deletion was successful
        """
        self._ensure_token()
        
        url = f"{self.api_base}/me/events/{event_id}"
        
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        
        return True
    
    def get_free_busy(
        self, 
        time_min: str, 
        time_max: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Get free/busy information for an Outlook calendar.
        
        Args:
            time_min: Start time for checking free/busy (ISO format)
            time_max: End time for checking free/busy (ISO format)
            **kwargs: Additional parameters
            
        Returns:
            Dict containing busy periods
        """
        self._ensure_token()
        
        url = f"{self.api_base}/me/calendar/getSchedule"
        
        schedules = kwargs.get("schedules", ["me"])
        
        request_body = {
            "schedules": schedules,
            "startTime": {
                "dateTime": time_min,
                "timeZone": "UTC"
            },
            "endTime": {
                "dateTime": time_max,
                "timeZone": "UTC"
            },
            "availabilityViewInterval": 15  # 15-minute intervals
        }
        
        response = requests.post(url, headers=self.headers, json=request_body)
        response.raise_for_status()
        result = response.json()
        
        # Process the response to extract busy periods
        busy_periods = []
        
        schedule_items = result.get("value", [])
        for schedule in schedule_items:
            calendar_id = schedule.get("scheduleId", "primary")
            working_hours = schedule.get("workingHours", {})
            
            # Process schedule items
            for item in schedule.get("scheduleItems", []):
                if item.get("status", "") == "busy":
                    busy_periods.append({
                        "start": item.get("start", {}).get("dateTime", ""),
                        "end": item.get("end", {}).get("dateTime", "")
                    })
        
        return {
            "calendar_id": "primary",  # Outlook doesn't use calendar IDs like Google
            "time_range": {
                "start": time_min,
                "end": time_max
            },
            "busy_periods": busy_periods
        } 