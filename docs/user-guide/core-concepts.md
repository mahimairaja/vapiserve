# Core Concepts

VapiServe is built around a few core concepts that make it powerful and flexible.

## Tools

A **tool** in VapiServe is a Python function decorated with the `@tool` decorator. It represents an API endpoint that can be called by external systems, particularly the Vapi voice AI platform.

```python
from vapiserve import tool

@tool(
    name="add_numbers",
    description="Add two numbers together"
)
def add_numbers(a: int, b: int) -> int:
    return a + b
```

When this tool is served via a VapiServe server, it becomes available as an HTTP endpoint that can be called with JSON data.

### Tool Properties

Each tool has several important properties:

- **Name**: A unique identifier for the tool
- **Description**: A description of what the tool does
- **Parameters**: Input parameters with types and descriptions
- **Return Type**: The type of the return value
- **Function**: The actual Python function that implements the tool

### Tool Parameters

Parameters are defined by the function signature and can be enhanced with type hints and default values:

```python
@tool(
    name="format_name",
    description="Format a name with a title"
)
def format_name(
    first_name: str,
    last_name: str,
    title: str = "Mr./Ms."
) -> str:
    return f"{title} {first_name} {last_name}"
```

For more complex parameter validation, you can use Pydantic models.

## Server

A **server** in VapiServe is a FastAPI application that hosts one or more tools. It provides HTTP endpoints for accessing the tools and includes interactive documentation.

```python
from vapiserve import serve

serve(
    tools=[tool1, tool2, tool3],
    title="My API Server",
    description="A collection of useful tools",
    port=8000
)
```

### Server Properties

The server has several important properties:

- **Tools**: The collection of tools to serve
- **Title**: The title of the API
- **Description**: A description of the API
- **Host**: The host address (default: 127.0.0.1)
- **Port**: The port to listen on (default: 8000)
- **OpenAPI Documentation**: Automatically generated documentation for the API

## Integrations

An **integration** in VapiServe is a connection to an external service, such as Google Calendar or Slack. Integrations are organized into categories:

- **Scheduling**: Calendar services
- **Tasks**: Task management services
- **Communication**: Messaging and communication services
- **Storage**: File storage services
- **Email**: Email services
- **AI**: Artificial intelligence services

### Provider Pattern

Each integration follows a "Provider Pattern" with:

1. **Base Provider Class**: An abstract base class that defines the interface
2. **Concrete Provider Class**: An implementation for a specific service
3. **Common Methods**: Standard methods that all providers in a category implement
4. **Credential Management**: Secure handling of API keys and tokens

For example, a calendar integration might look like:

```python
from vapiserve.integrations.scheduling import GoogleCalendarProvider

# Create a provider instance
provider = GoogleCalendarProvider(credentials_path="credentials.json")

# Use the provider
events = await provider.list_events(calendar_id="primary", max_results=10)
```

## Tools + Integrations

The real power of VapiServe comes from combining tools with integrations:

```python
from vapiserve import tool, serve
from vapiserve.integrations.scheduling import GoogleCalendarProvider

@tool(
    name="list_upcoming_events",
    description="List upcoming events from Google Calendar"
)
async def list_upcoming_events(
    credentials_path: str,
    calendar_id: str = "primary",
    max_results: int = 10
) -> dict:
    # Create a provider instance
    provider = GoogleCalendarProvider(credentials_path=credentials_path)
    
    # Use the provider
    events = await provider.list_events(
        calendar_id=calendar_id,
        max_results=max_results
    )
    
    # Return the results
    return {"events": events}

# Serve the tool
serve(list_upcoming_events)
```

This creates a tool that uses the Google Calendar integration to list upcoming events, which can then be called by the Vapi voice AI platform or any other HTTP client.

## Next Steps

- Learn more about [Creating Tools](./creating-tools.md)
- Explore [Serving Tools](./serving-tools.md)
- Dive into [Tool Parameters](./tool-parameters.md) 