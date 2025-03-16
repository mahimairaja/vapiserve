# VapiServe
<div align="center">

<img src="assets/logo-image.png" alt="VapiServe Logo" width="400">

</div>

<div class="grid cards" markdown>

- :fontawesome-solid-bolt: **Simple API Tools**  
  Create powerful API tools with minimal code
  
- :fontawesome-solid-server: **FastAPI Integration**  
  Built on FastAPI for high performance and easy deployment

<!-- - :fontawesome-solid-phone: **Vapi Compatible**  
  Seamless integration with Vapi's voice AI platform -->

- :fontawesome-solid-puzzle-piece: **Modular Integrations**  
  Connect with popular services across multiple categories

</div>

## What is VapiServe?

VapiServe is a Python framework for building API servers that power Vapi custom tools. It provides a streamlined way to create, serve, and integrate various services into your voice AI workflows.

With VapiServe, you can:

- Create custom tools with the simple `@tool` decorator
- Connect to popular services (calendars, tasks, storage, etc.)
- Deploy your API with built-in FastAPI integration
- Expose your local development server with ngrok tunneling
- Build complex voice AI experiences with minimal code

## Quick Example

Here's a simple tool that integrates with Google Calendar:

```python
from vapiserve import tool, serve
from vapiserve.integrations.scheduling import GoogleCalendarProvider

@tool(
    name="get_free_busy_times",
    description="Get free/busy information for a calendar",
)
async def get_free_busy_times(
    days_ahead: int = 7,
    credentials_path: str = "credentials.json",
    calendar_id: str = "primary"
) -> dict:
    """Check free/busy information for a Google Calendar."""
    provider = GoogleCalendarProvider(credentials_path=credentials_path)
    free_busy_info = await provider.get_free_busy(calendar_id, days_ahead)
    return {
        "busy_periods": free_busy_info["busy_periods"],
        "free_slots": free_busy_info["free_slots"]
    }

# Start the server with the tool
serve(
    get_free_busy_times,
    title="Calendar API Tools",
    description="Tools for working with calendar services",
    port=8000,
)
```

## Features

- **Decorator-based Tool Creation**: Define API endpoints with simple Python decorators
- **Built-in Documentation**: Automatic OpenAPI documentation for all your tools
- **Service Integrations**: Connect to popular services with pre-built integrations
- **Type Validation**: Automatic request and response validation
- **Secure Credential Handling**: Safely manage API keys and tokens
- **Ngrok Integration**: Expose your local development server to the internet
- **Flexible Deployment**: Deploy locally or to any cloud provider that supports Python

## Integrations

VapiServe provides integrations across multiple categories:

| Category | Integrations |
| -------- | ------------ |
| Scheduling | Google Calendar, Outlook Calendar |
| Tasks | Todoist |
| Communication | Slack, Twilio |
| Storage | AWS S3, Google Cloud Storage |
| Email | SendGrid |
| AI | OpenAI, Anthropic |

## Getting Started

Check out the [Installation](./getting-started/installation.md) guide to get started, or explore the [Quickstart](./getting-started/quickstart.md) for a hands-on introduction. 