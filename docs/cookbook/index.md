# Cookbook Overview

The VapiServe cookbook contains a collection of practical examples demonstrating various features and integration patterns. Each example is designed to be runnable and comes with detailed explanations.

## Available Examples

### Basic Example

The [Basic Example](./basic-example.md) demonstrates the simplest way to create and serve a VapiServe tool. It's a great starting point for understanding the core functionality.

**Key concepts covered:**
- Creating a basic tool with the `@tool` decorator
- Setting up a FastAPI server with `serve()`
- Defining parameters and return types

### Ngrok Example

The [Ngrok Example](./ngrok-example.md) shows how to expose your local VapiServe instance to the internet using ngrok. This is particularly useful for testing your tools with external services.

**Key concepts covered:**
- Automatic ngrok tunnel setup
- Public URL generation
- Configuring ngrok options

### Calendar Example

The [Calendar Example](./calendar-example.md) demonstrates integrating with Google Calendar to retrieve free/busy information.

**Key concepts covered:**
- Connecting to Google Calendar API
- Handling OAuth authentication
- Structuring calendar data for easy consumption

### Storage Example

The [Storage Example](./storage-example.md) shows how to work with cloud storage providers like AWS S3 and Google Cloud Storage.

**Key concepts covered:**
- File upload and download operations
- Provider factory pattern
- Working with multiple storage providers

## Structure of Examples

Each example follows a consistent structure:

1. **Overview**: A brief description of what the example demonstrates
2. **Prerequisites**: Required dependencies and setup
3. **Code Walkthrough**: Explanation of the key components
4. **Running the Example**: Instructions for running the example
5. **Next Steps**: Suggestions for extending or modifying the example

## Running the Examples

All examples are located in the `cookbook` directory of the VapiServe repository. To run an example:

```bash
# Navigate to the cookbook directory
cd cookbook

# Run a specific example
python basic_example.py
```

## Creating Your Own Examples

We encourage you to create your own examples based on these patterns. If you've built something interesting with VapiServe, consider contributing it to the cookbook!

To contribute an example:

1. Create a new Python file in the `cookbook` directory
2. Follow the structure of existing examples
3. Add comprehensive comments explaining your code
4. Create a documentation page in `docs/cookbook/`
5. Submit a pull request

## Example Code Repository

You can find all these examples in the [VapiServe GitHub repository](https://github.com/vapi-ai/vapiserve/tree/main/cookbook). 