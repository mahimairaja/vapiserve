# Key Features

VapiServe provides a comprehensive set of features for building, serving, and integrating API tools.

## Core Features

### Simple Tool Creation

Create API endpoints with a straightforward decorator approach:

```python
@tool(name="my_tool", description="My awesome tool")
async def my_tool(param1: str, param2: int = 42) -> dict:
    # Your logic here
    return {"result": "Success!"}
```

### FastAPI Integration

Built on top of FastAPI, VapiServe inherits all of its benefits:

- **High performance**: Based on Starlette and Pydantic
- **Automatic validation**: Request and response validation
- **Interactive documentation**: Built-in Swagger UI
- **Dependency injection**: Powerful dependency system
- **Asynchronous support**: Modern async/await syntax
- **Middleware**: Add custom middleware as needed

### Vapi Compatibility

Designed to work seamlessly with Vapi's voice AI platform:

- **API Schema**: Follows Vapi's custom tool schema
- **Response Format**: Returns results in the format expected by Vapi
- **Parameter Handling**: Properly handles and validates all parameter types
- **Error Management**: Provides clear error responses

### Modular Design

VapiServe is built with modularity in mind:

- **Selective Imports**: Only import what you need
- **Optional Dependencies**: Install only the dependencies required for your use case
- **Extensible Architecture**: Easily add new integrations or features

## Integration Features

### Service Provider Framework

A consistent interface for connecting to external services:

- **Base Classes**: Abstract base classes for each integration category
- **Common Methods**: Standardized method signatures
- **Credential Management**: Secure handling of API keys and tokens
- **Error Handling**: Consistent error handling across providers

### Pre-built Integrations

Ready-to-use integrations across multiple categories:

#### Scheduling

- Google Calendar
- Outlook Calendar

#### Tasks

- Todoist

#### Communication

- Slack
- Twilio

#### Storage

- AWS S3
- Google Cloud Storage

#### Email

- SendGrid

#### AI

- OpenAI
- Anthropic

## Server Features

### Easy Server Startup

Start your API server with a single function call:

```python
serve(
    tools=[my_tool, another_tool],
    title="My API Server",
    description="A collection of useful tools",
    port=8000
)
```

### Automatic Documentation

Generate interactive API documentation:

- **Swagger UI**: Available at `/docs`
- **ReDoc**: Available at `/redoc`
- **OpenAPI Schema**: Available at `/openapi.json`

### Configuration Options

Customize your server behavior:

- **CORS Settings**: Control cross-origin requests
- **Authentication**: Add authentication as needed
- **Rate Limiting**: Protect against abuse
- **Environment Variables**: Configure using environment variables

### Deployment Options

Deploy your server anywhere Python runs:

- **Local Development**: Run locally for development
- **Ngrok Tunneling**: Expose your local server to the internet
- **Cloud Deployment**: Deploy to any cloud provider

## Developer Experience

### Comprehensive Type Hints

Full type annotation for better IDE support and code safety:

```python
from typing import Dict, Any, List, Optional
from vapiserve import tool

@tool()
async def typed_tool(
    names: List[str],
    count: Optional[int] = None
) -> Dict[str, Any]:
    result = {name: len(name) for name in names[:count]}
    return {"result": result}
```

### Detailed Logging

Built-in logging to help with debugging and monitoring:

```python
import logging
from vapiserve import configure_logging

# Set up logging
configure_logging(level=logging.DEBUG)
```

### Extensibility

Easily extend VapiServe with custom functionality:

- **Custom Decorators**: Create your own decorators
- **Custom Validators**: Add custom validation logic
- **Custom Middleware**: Add middleware for additional functionality
- **Custom Providers**: Create your own service providers

## Cookbook Examples

Ready-to-use examples for common scenarios:

- **Basic Example**: Minimal server with a simple tool
- **Ngrok Example**: Expose your server with ngrok
- **Calendar Example**: Integration with Google Calendar
- **Storage Example**: File operations with cloud storage

## Next Steps

- Explore the [User Guide](../user-guide/core-concepts.md) to learn more
- Check out the [Cookbook](../cookbook/index.md) for practical examples
- Browse the [API Reference](../api/tools.md) for detailed documentation 