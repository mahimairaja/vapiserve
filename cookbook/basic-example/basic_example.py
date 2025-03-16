from typing import Dict, Any
from vapiserve import tool, serve


@tool(name="echo", description="Echo back the input message")
async def echo(message: str = "Hello, world!") -> Dict[str, Any]:
    message = f'Server received: {message}'
    # TODO: Add your logic here
    # ...
    return {
        "message": message,
    }


if __name__ == "__main__":
    serve(
        echo,
        title="VapiServe Echo Example",
        description="Simple echo tools demonstrating VapiServe capabilities",
        port=8000,
        # use_ngrok=True,
        # ngrok_region="us",
        # ngrok_auth_token="YOUR_NGROK_AUTH_TOKEN",
    ) 