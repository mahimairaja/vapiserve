"""Google Calendar integration."""

import os
import json
import datetime
from typing import Any, Dict, List, Optional, Union
import logging

logger = logging.getLogger(__name__)

try:
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google.oauth2.service_account import Credentials as ServiceAccountCredentials
    HAS_GOOGLE_CALENDAR = True
except ImportError:
    HAS_GOOGLE_CALENDAR = False

from .base import CalendarProvider


class GoogleCalendarProvider(CalendarProvider):
    """Google Calendar integration."""
    
    def __init__(
        self,
        credentials_json_or_path: str,
        calendar_id: str = "primary",
        impersonate_user: Optional[str] = None,
    ):
        """Initialize the Google Calendar provider.
        
        Args:
            credentials_json_or_path: JSON string with Google credentials or path to a JSON file.
                Can be either OAuth2 user credentials or service account credentials.
            calendar_id: Calendar ID to use (default: "primary")
            impersonate_user: Email of user to impersonate (for service accounts only)
        """
        if not HAS_GOOGLE_CALENDAR:
            raise ImportError(
                "Google Calendar dependencies not installed. "
                "Install with 'pip install vapiserve[google]'"
            )
        
        # Parse credentials
        try:
            # Try to load credentials from a file path first
            if os.path.exists(credentials_json_or_path):
                with open(credentials_json_or_path, 'r') as f:
                    creds_dict = json.load(f)
                logger.info(f"Loaded credentials from file: {credentials_json_or_path}")
                is_file_path = True
            else:
                # If not a file path, try to parse as a JSON string
                try:
                    creds_dict = json.loads(credentials_json_or_path)
                    is_file_path = False
                except json.JSONDecodeError:
                    # Final attempt: check if it's an environment variable name
                    if credentials_json_or_path in os.environ:
                        creds_dict = json.loads(os.environ[credentials_json_or_path])
                        is_file_path = False
                    else:
                        raise ValueError(f"Could not parse credentials: {credentials_json_or_path[:20]}...")
            
            # Determine if the credentials are for a service account
            is_service_account = self._is_service_account_credentials(creds_dict)
            
            if is_service_account:
                logger.info("Using service account authentication")
                
                # For service accounts, we can use the file directly or create from dict
                if is_file_path:
                    self.credentials = ServiceAccountCredentials.from_service_account_file(
                        credentials_json_or_path,
                        scopes=["https://www.googleapis.com/auth/calendar"]
                    )
                else:
                    self.credentials = ServiceAccountCredentials.from_service_account_info(
                        creds_dict,
                        scopes=["https://www.googleapis.com/auth/calendar"]
                    )
                
                # If impersonation is needed
                if impersonate_user:
                    self.credentials = self.credentials.with_subject(impersonate_user)
                    logger.info(f"Impersonating user: {impersonate_user}")
            else:
                logger.info("Using OAuth2 user authentication")
                self.credentials = Credentials.from_authorized_user_info(info=creds_dict)
            
            self.service = build("calendar", "v3", credentials=self.credentials)
            self.calendar_id = calendar_id
        except Exception as e:
            raise ValueError(f"Failed to initialize Google Calendar: {str(e)}")
    
    def _is_service_account_credentials(self, creds_dict: Dict[str, Any]) -> bool:
        """Determine if the credentials are for a service account.
        
        Args:
            creds_dict: Credentials dictionary
            
        Returns:
            bool: True if credentials are for a service account
        """
        # Service account credentials typically have these fields
        service_account_fields = [
            "type", "project_id", "private_key_id", "private_key", 
            "client_email", "client_id", "auth_uri", "token_uri"
        ]
        
        # OAuth2 user credentials typically have these fields
        oauth2_fields = ["token", "refresh_token", "client_id", "client_secret"]
        
        # Check which type of credentials we have based on the fields
        service_account_match = all(field in creds_dict for field in ["type", "private_key"])
        
        # Additional check for the explicit type of service account
        if service_account_match and creds_dict.get("type") == "service_account":
            return True
        
        return False
    
    def create_event(
        self,
        summary: str,
        start_time: str,
        end_time: str,
        timezone: str = "UTC",
        location: Optional[str] = None,
        description: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        calendar_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a new event in Google Calendar.
        
        Args:
            summary: Title of the event
            start_time: Start time in ISO format
            end_time: End time in ISO format
            timezone: Timezone for the event
            location: Optional location for the event
            description: Optional description for the event
            attendees: Optional list of email addresses for attendees
            calendar_id: Optional calendar ID to use (overrides the default)
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the created event details
        """
        # Prepare the event
        event = {
            "summary": summary,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_time,
                "timeZone": timezone,
            },
            "end": {
                "dateTime": end_time,
                "timeZone": timezone,
            },
        }
        
        # Add attendees if provided
        if attendees:
            event["attendees"] = [{"email": email} for email in attendees]
        
        # Use provided calendar_id or fall back to default
        cal_id = calendar_id or self.calendar_id
        
        # Insert the event
        event_result = self.service.events().insert(
            calendarId=cal_id, 
            body=event
        ).execute()
        
        return {
            "event_id": event_result["id"],
            "status": "created",
            "link": event_result.get("htmlLink", ""),
            "calendar_id": cal_id,
        }
    
    def list_events(
        self,
        time_min: Optional[str] = None,
        time_max: Optional[str] = None,
        max_results: int = 10,
        calendar_id: Optional[str] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """List upcoming events from Google Calendar.
        
        Args:
            time_min: Optional start time in ISO format
            time_max: Optional end time in ISO format
            max_results: Maximum number of events to return
            calendar_id: Optional calendar ID to use (overrides the default)
            **kwargs: Additional parameters
            
        Returns:
            List of events matching the criteria
        """
        # Set default time_min to now if not provided
        if not time_min:
            time_min = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        
        # Use provided calendar_id or fall back to default
        cal_id = calendar_id or self.calendar_id
        
        # Get events
        events_result = self.service.events().list(
            calendarId=cal_id,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        
        events = events_result.get("items", [])
        
        # Format events for the response
        formatted_events = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            
            formatted_events.append({
                "id": event["id"],
                "summary": event.get("summary", "No Title"),
                "start": start,
                "end": end,
                "location": event.get("location", ""),
                "description": event.get("description", ""),
                "link": event.get("htmlLink", ""),
                "calendar_id": cal_id,
            })
        
        return formatted_events
    
    def get_event(
        self, 
        event_id: str, 
        calendar_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Get details of a specific event from Google Calendar.
        
        Args:
            event_id: ID of the event to retrieve
            calendar_id: Optional calendar ID to use (overrides the default)
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the event details
        """
        # Use provided calendar_id or fall back to default
        cal_id = calendar_id or self.calendar_id
        
        event = self.service.events().get(
            calendarId=cal_id,
            eventId=event_id
        ).execute()
        
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        
        return {
            "id": event["id"],
            "summary": event.get("summary", "No Title"),
            "start": start,
            "end": end,
            "location": event.get("location", ""),
            "description": event.get("description", ""),
            "link": event.get("htmlLink", ""),
            "calendar_id": cal_id,
            "attendees": [
                attendee.get("email", "")
                for attendee in event.get("attendees", [])
            ],
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
        calendar_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Update an existing event in Google Calendar.
        
        Args:
            event_id: ID of the event to update
            summary: Optional new title
            start_time: Optional new start time
            end_time: Optional new end time
            timezone: Optional new timezone
            location: Optional new location
            description: Optional new description
            attendees: Optional new list of attendees
            calendar_id: Optional calendar ID to use (overrides the default)
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the updated event details
        """
        # Use provided calendar_id or fall back to default
        cal_id = calendar_id or self.calendar_id
        
        # Get the current event
        event = self.service.events().get(
            calendarId=cal_id,
            eventId=event_id
        ).execute()
        
        # Update fields if provided
        if summary:
            event["summary"] = summary
        if location:
            event["location"] = location
        if description:
            event["description"] = description
            
        # Update start time
        if start_time:
            timezone = timezone or event["start"].get("timeZone", "UTC")
            event["start"] = {
                "dateTime": start_time,
                "timeZone": timezone,
            }
            
        # Update end time
        if end_time:
            timezone = timezone or event["end"].get("timeZone", "UTC")
            event["end"] = {
                "dateTime": end_time,
                "timeZone": timezone,
            }
            
        # Update attendees
        if attendees:
            event["attendees"] = [{"email": email} for email in attendees]
            
        # Update the event
        updated_event = self.service.events().update(
            calendarId=cal_id,
            eventId=event_id,
            body=event,
        ).execute()
        
        return {
            "event_id": updated_event["id"],
            "status": "updated",
            "link": updated_event.get("htmlLink", ""),
            "calendar_id": cal_id,
        }
    
    def delete_event(
        self, 
        event_id: str, 
        calendar_id: Optional[str] = None,
        **kwargs
    ) -> bool:
        """Delete an event from Google Calendar.
        
        Args:
            event_id: ID of the event to delete
            calendar_id: Optional calendar ID to use (overrides the default)
            **kwargs: Additional parameters
            
        Returns:
            True if deletion was successful
        """
        # Use provided calendar_id or fall back to default
        cal_id = calendar_id or self.calendar_id
        
        self.service.events().delete(
            calendarId=cal_id,
            eventId=event_id,
        ).execute()
        
        return True
        
    def get_free_busy(
        self, 
        time_min: str, 
        time_max: str,
        calendar_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Get free/busy information for a calendar.
        
        Args:
            time_min: Start time for checking free/busy (ISO format)
            time_max: End time for checking free/busy (ISO format)
            calendar_id: Optional calendar ID to use (overrides the default)
            **kwargs: Additional parameters
            
        Returns:
            Dict containing busy periods
        """
        # Use provided calendar_id or fall back to default
        cal_id = calendar_id or self.calendar_id
        
        # Prepare the query
        query = {
            "timeMin": time_min,
            "timeMax": time_max,
            "items": [{"id": cal_id}]
        }
        
        # Execute the query
        free_busy_result = self.service.freebusy().query(body=query).execute()
        
        # Format the result
        calendars = free_busy_result.get("calendars", {})
        busy_periods = calendars.get(cal_id, {}).get("busy", [])
        
        return {
            "calendar_id": cal_id,
            "time_range": {
                "start": time_min,
                "end": time_max
            },
            "busy_periods": busy_periods
        } 