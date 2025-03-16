# VapiServe Cookbook

Welcome to the VapiServe Cookbook! This collection of examples demonstrates how to use VapiServe to build powerful API tools that can be integrated with Vapi's voice AI platform or used independently.

## Overview

The cookbook is organized into separate directories, each containing a complete, runnable example focused on specific aspects of VapiServe functionality. Each example is fully documented with its own README explaining how it works and how to run it.

## Examples

| Example | Description | Key Concepts |
|---------|-------------|--------------|
| [Basic Example](./basic-example/) | The simplest possible VapiServe implementation | Tool creation, Server setup |
| [Ngrok Example](./ngrok-example/) | Expose your local server to the internet | Public URLs, Tunneling, Webhooks |
| [Calendar Example](./calendar-example/) | Google Calendar integration | API integration, OAuth, External services |
| [Storage Example](./storage-example/) | Cloud storage operations | Multiple providers, File operations |

## Prerequisites

To run these examples, you'll need:

- Python 3.8 or higher
- VapiServe package installed (`pip install vapiserve`)
- Additional dependencies as specified in individual examples

## Getting Started

The best way to get started is to:

1. Start with the [Basic Example](./basic-example/) to understand core concepts
2. Move on to other examples based on your specific needs
3. Read the individual README files in each example directory for detailed instructions

## Running the Examples

Each example is designed to be self-contained. To run an example:

```bash
cd [example-directory]
python [example_script].py
```

For example:

```bash
cd basic-example
python basic_example.py
```

## Example Structure

Each example directory follows a common structure:

```
example-name/
├── example_name.py    # Main example script
├── README.md          # Documentation for the example
└── [other files]      # Additional files needed for the example
```

## Development Patterns

Throughout these examples, you'll see common patterns:

1. **Tool Definition**: Using the `@tool` decorator to define API tools
2. **Server Setup**: Creating and configuring the VapiServe server
3. **Integration**: Connecting with external services and APIs
4. **Documentation**: Comprehensive documentation for both developers and API users

## Community and Support

- GitHub Issues: Report bugs or suggest features
- Discussions: Ask questions and share ideas
- Documentation: Read the full VapiServe documentation

## Contributing

We welcome contributions to the cookbook! If you have a useful example that demonstrates a VapiServe feature or integration, please open a pull request.

## License

These examples are provided under the MIT license - see the `LICENSE` file for details. 