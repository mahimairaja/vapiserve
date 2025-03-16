#!/usr/bin/env python
"""Example script demonstrating ngrok integration with VapiServer."""

import os
import sys
from pathlib import Path

# Add parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.vapiserve.core.server import VapiServer
from src.vapiserve.core.tool import tool


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
    """Echo input back to user.
    
    Args:
        message: Message to echo back
        
    Returns:
        The same message that was input
    """
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
    """Greet a user by name.
    
    Args:
        name: Name to greet
        formal: Whether to use formal greeting
        
    Returns:
        A greeting message
    """
    if formal:
        return f"Good day, {name}. How may I assist you today?"
    return f"Hi {name}! How's it going?"


def main():
    """Run the example server with ngrok integration."""
    server = VapiServer(
        title="VapiServe with Ngrok",
        description="Example API demonstrating ngrok integration",
    )
    
    # Add our demo tools
    server.add_tool(echo)
    server.add_tool(greet)
    
    # Check if ngrok auth token is provided in environment
    ngrok_auth_token = os.environ.get("NGROK_AUTH_TOKEN")
    
    # Start the server with ngrok enabled
    server.serve(
        host="0.0.0.0",
        port=8000,
        use_ngrok=True,  # Enable ngrok
        ngrok_region="us",  # Use US region (or your preferred region)
        ngrok_auth_token=ngrok_auth_token,  # Use token from environment if available
    )


if __name__ == "__main__":
    main() 