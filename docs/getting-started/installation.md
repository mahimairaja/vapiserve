# Installation

VapiServe is available on PyPI and can be installed with pip.

## Requirements

- Python 3.8 or higher
- pip (Python package installer)

## Basic Installation

Install VapiServe with pip:

```bash
pip install vapiserve
```

This will install the core VapiServe package with its basic dependencies, including FastAPI, Pydantic, Uvicorn, and essential utilities.

## Installing with Optional Dependencies

VapiServe is designed with modularity in mind. You can install only the dependencies you need for specific integrations.

### Integration Categories

VapiServe provides several extra dependency groups for different integration categories:

```bash
# Install scheduling integrations (Google Calendar, Outlook)
pip install "vapiserve[scheduling]"

# Install task management integrations (Todoist)
pip install "vapiserve[tasks]"

# Install communication integrations (Slack, Twilio)
pip install "vapiserve[communication]"

# Install storage integrations (AWS S3, Google Cloud Storage)
pip install "vapiserve[storage]"

# Install email integrations (SendGrid)
pip install "vapiserve[email]"

# Install AI integrations (OpenAI, Anthropic)
pip install "vapiserve[ai]"
```

### Combined Installations

You can combine multiple extras:

```bash
# Install scheduling and tasks integrations
pip install "vapiserve[scheduling,tasks]"

# Install all integrations
pip install "vapiserve[all-integrations]"
```

### Development Dependencies

For development, you can install additional tools for testing, linting, and formatting:

```bash
pip install "vapiserve[dev]"
```

### Ngrok Integration

To expose your local server to the internet using ngrok:

```bash
pip install "vapiserve[ngrok]"
```

### Complete Installation

For a complete installation with all dependencies:

```bash
pip install "vapiserve[all-integrations,dev,ngrok]"
```

## Installation from Source

If you prefer to install from source, clone the repository and install using pip:

```bash
git clone https://github.com/vapi-ai/vapiserve.git
cd vapiserve
pip install -e .
```

For development installation:

```bash
pip install -e ".[dev,all-integrations]"
```

## Verification

After installation, you can verify that VapiServe is working correctly:

```python
from vapiserve import __version__

print(f"VapiServe version: {__version__}")
```

## Next Steps

- Follow the [Quickstart](./quickstart.md) guide to create your first tool
- Explore the [Key Features](./features.md) of VapiServe
- Check out the [Cookbook](../cookbook/index.md) for examples 