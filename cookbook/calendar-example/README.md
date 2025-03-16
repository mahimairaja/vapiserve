# Google Calendar Integration Example

This example demonstrates how to integrate Google Calendar functionality into your VapiServe application. It showcases:

- Connecting to Google Calendar API
- Checking free/busy information for a calendar
- Handling authentication with OAuth credentials
- Structuring calendar data for easy consumption

## Features

- Retrieves free/busy information from Google Calendar
- Configurable time range (days ahead)
- Uses OAuth 2.0 for secure authentication
- Structured output format for easy integration with other services

## How It Works

The example uses the GoogleCalendarProvider from VapiServe's scheduling integrations to:

1. Authenticate with Google Calendar using OAuth 2.0 credentials
2. Calculate a time range (current time + specified days ahead)
3. Query the Calendar API for free/busy information in that range
4. Return structured data about busy periods and free slots

## Prerequisites

- Python 3.8+
- VapiServe package installed (`pip install vapiserve`)
- Google Calendar API enabled in Google Cloud Console
- OAuth 2.0 credentials file (`credentials.json`) - see Setup section

## Setup

### Google Cloud Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API for your project
4. Create OAuth 2.0 credentials (Desktop application type)
5. Download the credentials JSON file and save it as `credentials.json` in this directory

### Environment Setup

If you're using environment variables for credentials:

```bash
# Optional: Set environment variables for credentials path
export GOOGLE_CREDENTIALS_PATH="/path/to/your/credentials.json"
export GOOGLE_CALENDAR_ID="your_calendar_id@gmail.com"
```

## Usage

To run this example:

```bash
cd calendar-example
python calendar_example.py
```

When first executed, the script will:
1. Open a browser window for OAuth authentication
2. Ask you to log in and grant permissions
3. Save a token file for future use
4. Start the server and make the tool available

Once running, you can:

1. Access the OpenAPI documentation at http://localhost:8000/docs
2. Test the calendar tool by sending a POST request with parameters
3. View the free/busy information in the response

## Code Walkthrough

### Tool Definition

```python
@tool(
    name="get_free_busy_times",
    description="Get free/busy information for a calendar",
)
async def get_free_busy_times(
    days_ahead: Optional[int] = 7,
    credentials_path: Optional[str] = "credentials.json",
    calendar_id: Optional[str] = "primary"
) -> Dict[str, Any]:
    # Authentication and API call logic
    # ...
    return {
        "busy_periods": busy_periods,
        "free_slots": free_slots
    }
```

This creates a tool that:
- Takes optional parameters for customization
- Uses the GoogleCalendarProvider to interact with Google Calendar API
- Returns busy periods and available free slots

### Free/Busy Calculation

The tool calculates:
- Busy periods (meetings and events)
- Free slots (gaps between busy periods)
- Time ranges in a user-friendly format

## Response Format

The API returns data in this format:

```json
{
  "busy_periods": [
    {
      "start": "2023-03-16T09:00:00-04:00",
      "end": "2023-03-16T10:00:00-04:00"
    },
    ...
  ],
  "free_slots": [
    {
      "start": "2023-03-16T08:00:00-04:00",
      "end": "2023-03-16T09:00:00-04:00"
    },
    ...
  ]
}
```

## Security Considerations

This example demonstrates secure handling of Google Calendar credentials:
- OAuth 2.0 for secure authentication
- Local token storage for persistence
- Environmental variable support for production deployment

## Next Steps

After understanding this example, you can:

1. Extend the functionality to create or update calendar events
2. Integrate with other scheduling providers (Outlook, etc.)
3. Build complex scheduling applications for meeting coordination
4. Combine with the ngrok-example to create public scheduling tools 