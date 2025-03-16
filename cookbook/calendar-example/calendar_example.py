"""Simple example showing how to check free/busy information in Google Calendar."""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from vapiserve import serve, tool
from vapiserve.integrations.scheduling import GoogleCalendarProvider
from vapiserve.utils.security import load_env_file


@tool(
    name="get_free_busy_times",
    description="Get free/busy information for a calendar",
)
async def get_free_busy_times(
    days_ahead: Optional[int] = 7,
    credentials_path: Optional[str] = "credentials.json",
    calendar_id: Optional[str] = "mahimairaja3@gmail.com"
) -> Dict[str, Any]:
    """Get free/busy information for a calendar.
    
    Args:
        days_ahead: Number of days to look ahead
        credentials_path: Path to credentials JSON file
        calendar_id: Calendar ID to check
        
    Returns:
        Dictionary with busy periods
    """
    try:
        # Create calendar provider
        calendar = GoogleCalendarProvider(credentials_path, calendar_id=calendar_id)
        
        # Set time range
        now = datetime.now()
        end_time = now + timedelta(days=days_ahead)
        
        # Format times for the API
        time_min = now.isoformat() + "Z"
        time_max = end_time.isoformat() + "Z"
        
        # Get events to determine busy periods
        events = calendar.list_events(
            time_min=time_min,
            time_max=time_max,
            max_results=100
        )
        
        # Format busy periods
        busy_periods = []
        for event in events:
            busy_periods.append({
                "title": event["summary"],
                "start_time": event["start"],
                "end_time": event["end"]
            })
        
        return {
            "time_range": {
                "from": time_min,
                "to": time_max
            },
            "calendar_id": calendar_id,
            "busy_periods": busy_periods
        }
    except Exception as e:
        # Return error information
        return {
            "error": str(e),
            "calendar_id": calendar_id,
            "time_range": {
                "from": now.isoformat() + "Z",
                "to": end_time.isoformat() + "Z" if 'end_time' in locals() else "unknown"
            }
        }


if __name__ == "__main__":
    # Start the server with both tools
    serve(
        get_free_busy_times,
        title="Vapi Custom Tools Example",
        description="Example showing grouped tools in Swagger UI",
        port=7272,
    ) 