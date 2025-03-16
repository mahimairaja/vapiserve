# Basic Example

This example demonstrates the simplest way to create and serve a VapiServe tool. It showcases:

- Creating a basic tool with the `@tool` decorator
- Setting up a FastAPI server with `serve()`
- Defining parameters and return types

## Features

- Minimal example with a single echo tool
- Shows the core patterns for creating Vapi tools
- Demonstrates how to start a simple server

## How It Works

The example creates a simple echo endpoint that returns whatever message is sent to it. This illustrates the fundamental pattern used in VapiServe for creating tools:

1. Define a function
2. Decorate it with `@tool`
3. Start a server with `serve()`

## Prerequisites

- Python 3.8+
- VapiServe package installed (`pip install vapiserve`)

## Usage

To run this example:

```bash
cd basic-example
python basic_example.py
```

Once running, you can:

1. Access the OpenAPI documentation at http://localhost:8000/docs
2. Test the echo tool by sending a POST request to the endpoint
3. See the response echoed back to you

## Code Walkthrough

### Tool Definition

```python
@tool(name="echo", description="Echo back the input message")
async def echo(message: str = "Hello, world!") -> Dict[str, Any]:
    message = f'Server received: {message}'
    return {
        "message": message,
    }
```

This creates a tool named "echo" that accepts a message parameter (with a default value) and returns a dictionary containing the message.

### Starting the Server

```python
serve(
    echo,
    title="VapiServe Echo Example",
    description="Simple echo tools demonstrating VapiServe capabilities",
    port=8000,
)
```

This starts a FastAPI server with the echo tool registered. The server includes:
- Swagger UI documentation
- JSON Schema validation
- Proper HTTP status codes and error handling

## Next Steps

After understanding this example, you can:

1. Try modifying the echo function to do something more interesting
2. Add additional parameters to the function
3. Create multiple tools and register them with the server
4. Explore the ngrok-example to see how to expose your server to the internet 