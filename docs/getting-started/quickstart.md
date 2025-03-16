# Quickstart

This quickstart guide will walk you through creating a simple VapiServe tool and serving it via a FastAPI server.

## 1. Install VapiServe

First, install the VapiServe package:

```bash
pip install vapiserve
```

## 2. Create a Simple Tool

Create a new file named `echo_tool.py` with the following code:

```python
from typing import Dict, Any
from vapiserve import tool, serve

@tool(
    name="echo",
    description="Echo back the input message"
)
async def echo(message: str = "Hello, world!") -> Dict[str, Any]:
    """
    Simply returns the input message.
    
    Args:
        message: The message to echo back
        
    Returns:
        A dictionary containing the echoed message
    """
    return {
        "message": f"Server received: {message}"
    }

if __name__ == "__main__":
    serve(
        echo,
        title="Echo API",
        description="A simple echo API built with VapiServe",
        port=8000
    )
```

## 3. Run Your Server

Run the server with:

```bash
python echo_tool.py
```

You should see output similar to:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## 4. Test Your API

### Using the Swagger UI

Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). You'll see the Swagger UI where you can:

1. Click on the `/tools/echo` endpoint
2. Click the "Try it out" button
3. Enter a message in the request body
4. Click "Execute"
5. View the response

### Using curl

Alternatively, you can use curl to test your API:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/tools/echo' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"message": "Hello from curl!"}'
```

You should receive a response like:

```json
{
  "message": "Server received: Hello from curl!"
}
```

## 5. Integrate with Vapi

To use your tool with Vapi:

1. Make sure your server is accessible from the internet (see [Ngrok Tunneling](../deployment/ngrok.md))
2. In your Vapi dashboard, create a custom tool:
   - Set the server URL to your API endpoint
   - Define the parameters based on your tool's schema
   - Set the name and description to match your tool

Now you can reference this tool in your Vapi conversations!

## 6. Next Steps

- Add more tools to your server
- Explore integrations with external services
- Configure advanced server options
- Check out the cookbook examples

## Complete Example with Multiple Tools

Here's a more complete example with multiple tools:

```python
from typing import Dict, Any
from vapiserve import tool, serve

@tool(
    name="echo",
    description="Echo back the input message"
)
async def echo(message: str = "Hello, world!") -> Dict[str, Any]:
    return {
        "message": f"Server received: {message}"
    }

@tool(
    name="greet",
    description="Generate a personalized greeting"
)
async def greet(name: str, formal: bool = False) -> Dict[str, Any]:
    greeting = "Good day" if formal else "Hello"
    return {
        "greeting": f"{greeting}, {name}!"
    }

if __name__ == "__main__":
    serve(
        [echo, greet],  # Pass a list of tools
        title="My API Tools",
        description="Collection of simple API tools",
        port=8000
    )
```

Each tool will be available as a separate endpoint under the `/tools/` path. 