# Ngrok Integration Example

This example demonstrates how to expose your VapiServe instance to the internet using ngrok. This is particularly useful for:

- Testing webhooks during development
- Allowing external services to interact with your local tools
- Sharing your API with others without deploying to a server

## Features

- Automatic ngrok tunnel setup
- Public URL generation
- Multiple example tools (echo and greeting)
- Configurable ngrok options

## How It Works

The example creates a VapiServe instance with two simple tools and enables ngrok integration, which:

1. Starts a local server on port 8000
2. Launches ngrok to create a secure tunnel to your local server
3. Provides a public HTTPS URL that forwards to your local server

## Prerequisites

- Python 3.8+
- VapiServe package installed (`pip install vapiserve`)
- ngrok installed and available in your PATH (https://ngrok.com/download)
- Optional: ngrok authentication token for extended session duration (free account required)

## Usage

To run this example:

```bash
cd ngrok-example
python ngrok_example.py
```

Once running, you'll see output similar to:

```
🚀 Starting ngrok tunnel... This may take a few seconds.

✨ Ngrok tunnel established!
🌎 Public URL: https://abc123.ngrok.io
⚠️  Note: This URL will change on restart unless you have a paid ngrok account
📒 Local API docs: http://localhost:8000/docs
📒 Public API docs: https://abc123.ngrok.io/docs
```

Now your server is accessible both locally and via the internet at the provided public URL.

## Authentication Token

For extended session duration and more reliable tunnels, set your ngrok authentication token:

1. Sign up for a free ngrok account at https://ngrok.com
2. Get your auth token from the ngrok dashboard
3. Set it in the `ngrok_auth_token` parameter or as an environment variable:

```bash
export NGROK_AUTH_TOKEN="your_auth_token_here"
python ngrok_example.py
```

## Code Walkthrough

### Tool Definitions

The example defines two simple tools:

```python
@tool(
    description="Echo input back to user",
    parameters={
        "message": {
            "type": "string",
            "description": "Message to echo back",
        },
    },
    group="examples"
)
def echo(message: str) -> str:
    return message

@tool(
    description="Greet a user by name",
    parameters={
        "name": {
            "type": "string",
            "description": "Name to greet",
        },
        "formal": {
            "type": "boolean",
            "description": "Whether to use formal greeting",
            "default": False,
        },
    },
    group="examples"
)
def greet(name: str, formal: bool = False) -> str:
    if formal:
        return f"Good day, {name}. How may I assist you today?"
    return f"Hi {name}! How's it going?"
```

### Server with Ngrok

The server is started with ngrok enabled:

```python
server.serve(
    host="0.0.0.0",
    port=8000,
    use_ngrok=True,  # Enable ngrok
    ngrok_region="us",  # Use US region (or your preferred region)
    ngrok_auth_token=ngrok_auth_token,  # Use token from environment if available
)
```

## Benefits of Ngrok Integration

- **Development Testing**: Test callbacks and webhooks without deploying your app
- **Collaboration**: Share your API with team members or clients
- **Mobile Testing**: Test mobile apps against your local API
- **Vapi Integration**: Allow Vapi to call your tools remotely

## Limitations

- Free ngrok accounts have session limitations (2 hours)
- The URL changes every time you restart the server (unless using a paid account)
- Some rate limits apply with free accounts

## Next Steps

After understanding this example, you can:

1. Integrate ngrok into your own VapiServe applications
2. Configure additional ngrok options (like custom subdomains with paid accounts)
3. Use the public URL to register webhook endpoints with external services 