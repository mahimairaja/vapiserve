# VapiServe

A framework for easily building API servers for [Vapi](https://docs.vapi.ai/introduction) custom tools. VapiServe is inspired by [LangServe](https://python.langchain.com/docs/langserve) and aims to make it simple to create, deploy, and manage custom tools for Vapi voice assistants.

## Installation

Install the package using pip:

```bash
# Install base package
pip install vapiserve

# With integrations
pip install vapiserve[integrations]

# With ngrok for development
pip install vapiserve[ngrok]

# With all features
pip install vapiserve[integrations,ngrok,dev]
```

## Quick Start

Here's a minimal example of creating a Vapi tool server:

```python
from vapiserve import tool, serve

@tool(name="hello_world")
async def hello_world(name: str = "World") -> str:
    """Say hello to a person."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    serve(hello_world, port=8000)
```

This will start a server on port 8000 with a single tool. You can then configure Vapi to use this tool by pointing it to the endpoint:

```
http://your-server:8000/tools/hello_world
```

## Features

- **Simple Tool Definition**: Use the `@tool` decorator to turn any Python function into a Vapi tool
- **Automatic Schema Generation**: Tools' parameters and response types are automatically converted to JSON Schema
- **FastAPI Backend**: Built on FastAPI for performance and modern API features
- **Ready-to-use Integrations**: Built-in integrations for popular services
- **Ngrok Support**: Easily expose local servers during development

## Creating Tools

You can define a tool using the `@tool` decorator:

```python
from typing import Dict, List
from vapiserve import tool

@tool(
    name="get_weather",
    description="Get the current weather for a location",
)
async def get_weather(location: str, unit: str = "celsius") -> Dict[str, str]:
    """Get the current weather for a location.
    
    Args:
        location: The location to get weather for
        unit: Temperature unit (celsius or fahrenheit)
    """
    # Your implementation here
    return {
        "location": location,
        "temperature": "22 °C",
        "conditions": "sunny",
    }
```

The tool's parameters and return type will be automatically inferred from the function signature and type hints.

## Starting a Server

You can start a server with your tools in two ways:

### Using the `serve` function

```python
from vapiserve import serve
from my_tools import get_weather, add_todo, get_calendar_events

serve(
    get_weather,
    add_todo,
    get_calendar_events,
    title="My Vapi Tools",
    description="Custom tools for my Vapi assistant",
    port=8000,
)
```

### Using the command line

```bash
vapiserve --module my_tools --port 8000 --ngrok
```

This will find all tools in the `my_tools` module and start a server with them. The `--ngrok` flag will start an ngrok tunnel to expose the server publicly.

## Using with Vapi

Once your server is running, you can register the tools with Vapi:

1. Create a new custom tool in the Vapi dashboard
2. Use the tool schema from your server's `/tools` endpoint
3. Set the server URL to your server's public URL (e.g., your ngrok URL during development)

Your Vapi assistant can now use your custom tools!

## Integrations

VapiServe includes built-in integrations for popular services:

- **Google Calendar**: Create and manage calendar events
- **Todoist**: Manage tasks and to-do lists
- **Slack**: Send messages to channels or users
- **OpenAI**: Generate text, images, or embeddings
- **And more...**

To use an integration, import it from the integrations module:

```python
from vapiserve.integrations.calendar import create_calendar_event, list_calendar_events
from vapiserve import serve

serve(
    create_calendar_event,
    list_calendar_events,
)
```

## API Key Management

VapiServe provides utilities for managing API keys securely. You can set environment variables for API keys or provide them explicitly:

```python
from vapiserve.utils.security import api_keys

# Set an API key
api_keys.add_key("OPENAI_API_KEY", "sk-...")

# Or use from environment variables
# export OPENAI_API_KEY=sk-...
```

## Development

To set up a development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/vapiserve.git
cd vapiserve

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
