# Contributing to VapiServe

We love your input! We want to make contributing to VapiServe as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Adding a new integration
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Requests

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Add your changes
4. Ensure tests are passing (add tests for new functionality)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Adding a New Integration

VapiServe is designed to be easily extensible with new integrations. Here's how to add a new service:

1. Identify the appropriate category (scheduling, tasks, communication, etc.)
2. Create a new provider class that inherits from the relevant base class
3. Implement all required methods from the abstract base class
4. Add optional methods specific to your integration
5. Create Vapi tools that use your integration
6. Add example code demonstrating how to use your integration

For example, to add a new calendar provider:

1. Create a file in `src/vapiserve/integrations/scheduling/` (e.g., `custom_calendar.py`)
2. Define a class that inherits from `CalendarProvider`
3. Implement all required methods (create_event, list_events, etc.)
4. Update `__init__.py` to expose your new provider
5. Add a tool function that uses your provider in `src/vapiserve/tools/calendar.py`
6. Create an example in the `examples/` directory

### Code Style

We follow these style guidelines:

- Use [PEP 8](https://pep8.org/) for Python code style
- Sort imports with [isort](https://pep8.org/)
- Format code with [black](https://black.readthedocs.io/) (line length 88)
- Add type hints to all function parameters and return values
- Use docstrings for all classes and functions (Google style)
- Keep lines under 88 characters

### Testing

- Write test cases for all new functionality
- Tests should be placed in the `tests/` directory
- We use pytest for testing
- Run tests with `pytest` in the project root directory

## Project Structure

```
vapiserve/
├── examples/                  # Example code demonstrating usage
├── src/
│   └── vapiserve/
│       ├── core/              # Core functionality
│       │   ├── models.py      # Data models
│       │   ├── server.py      # FastAPI server
│       │   └── tool.py        # Vapi tool decorator
│       ├── integrations/      # Service integrations
│       │   ├── scheduling/    # Calendar integrations
│       │   ├── tasks/         # Task management integrations
│       │   ├── crm/           # CRM integrations
│       │   └── ...
│       └── tools/             # Vapi tools using integrations
│           ├── calendar.py    # Calendar tools
│           ├── tasks.py       # Task management tools
│           └── ...
└── tests/                     # Test suite
```

## Setting Up Development Environment

1. Clone the repository
   ```
   git clone https://github.com/yourusername/vapiserve.git
   cd vapiserve
   ```

2. Create a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies
   ```
   pip install -e ".[dev]"
   ```

4. Run tests to verify your setup
   ```
   pytest
   ```

## Environment Variables

For testing integrations, you'll need to set up your own API keys and credentials. We recommend using a `.env` file for local development:

```
# Google Calendar
GOOGLE_TOKEN_JSON={"your": "credentials"}

# Slack
SLACK_BOT_TOKEN=xoxb-your-token

# OpenAI
OPENAI_API_KEY=your-api-key

# Add other API keys as needed
```

## Dependency Management

- Add new dependencies to `setup.py` in the appropriate section
- For optional dependencies, add them to the "extras" section
- Use semantic versioning for dependencies (`>=1.0.0, <2.0.0`)

## Reporting Bugs

We use GitHub issues to track public bugs. Report a bug by opening a new issue; it's that easy!

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License. 