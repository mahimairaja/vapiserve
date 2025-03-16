# VapiServe

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-image.png">
    <source media="(prefers-color-scheme: light)" srcset="docs/assets/logo-image.png">
    <img alt="VapiServe Logo" src="https://raw.githubusercontent.com/mahimairaja/vapiserve/main/docs/assets/logo-image.png" width="250">
  </picture>
</p>

<p align="center">
  <a href="https://pypi.org/project/vapiserve/"><img src="https://img.shields.io/pypi/v/vapiserve.svg" alt="PyPI Version"/></a>
  <a href="https://pypi.org/project/vapiserve/"><img src="https://img.shields.io/pypi/pyversions/vapiserve.svg" alt="Python Versions"/></a>
  <a href="https://github.com/mahimairaja/vapiserve/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"/></a>
  <a href="https://mahimairaja.github.io/vapiserve/"><img src="https://img.shields.io/badge/docs-latest-brightgreen.svg" alt="Documentation"/></a>
</p>

### A lightweight framework for creating and deploying API servers for [Vapi](https://docs.vapi.ai/introduction) custom tools.

## Installation

```bash
pip install vapiserve
```

## Quick Example

```python
from vapiserve import tool, serve

@tool(name="echo")
async def echo(message: str = "Hello") -> dict:
    # Add your tool logic here
    ...
    message = f"You said: {message}"
    
    return {"message": message}

if __name__ == "__main__":
    serve(echo, port=8000)
```

Your tool is now available at `http://localhost:8000/tools/echo`.

## Features

- Create tools with simple `@tool` decorator
- Built on FastAPI for high performance
- Structured error handling and validation
- Multiple service integrations in modular design
- Expose local servers with ngrok for development
- Comprehensive type hints and documentation

## Service Integrations

VapiServe provides integrations across various categories:

- **Scheduling**: Google Calendar, Outlook Calendar
- **Tasks**: Todoist
- **Communication**: Slack, Twilio
- **Storage**: AWS S3, Google Cloud Storage
- **Email**: SendGrid
- **AI**: OpenAI, Anthropic

## Documentation

Kindly refer to our [documentation](https://mahimairaja.github.io/vapiserve/) for detailed usage instructions.

## Contributing

Contributions are welcome. Kindly fork the repository, create a feature branch, and submit a pull request.

## License

This project is licensed under the MIT License.


Made with ❤️ by [Mahimai Raja](https://github.com/mahimairaja)