# Cloud Storage Integration Example

This example demonstrates how to integrate with cloud storage providers (like AWS S3 and Google Cloud Storage) using VapiServe. It showcases:

- File upload, download, and listing capabilities
- Multiple storage provider support (GCS, AWS S3)
- Handling different file types and content
- Simplified storage operations through tools

## Features

- Upload files to cloud storage
- Download files from cloud storage
- List files in cloud storage
- Support for multiple providers in a single interface
- Simplified demonstration tools

## How It Works

The example uses VapiServe's storage integrations to:

1. Connect to cloud storage providers (AWS S3, Google Cloud Storage)
2. Provide a unified interface for common storage operations
3. Handle different content types and storage configurations
4. Demonstrate practical file management use cases

## Prerequisites

- Python 3.8+
- VapiServe package installed (`pip install vapiserve`)
- For actual cloud operations (not just demo):
  - AWS account with S3 access (for AWS S3)
  - Google Cloud account with Storage enabled (for GCS)
  - Appropriate credentials configured

## Setup

### AWS S3 Setup (For actual use)

If you plan to use AWS S3:

```bash
# Set environment variables for AWS
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_REGION="us-east-1"
```

### Google Cloud Storage Setup (For actual use)

If you plan to use Google Cloud Storage:

```bash
# Set environment variable for GCP credentials
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

## Usage

To run this example:

```bash
cd storage-example
python storage_example.py
```

Once running, you can:

1. Access the OpenAPI documentation at http://localhost:8000/docs
2. Test the storage tools by sending POST requests to the endpoints
3. Use the simplified demo tools to see how storage operations work

## Demo vs. Production

This example includes:

1. **Actual Cloud Operations**: Tools that interact with real cloud providers (if credentials are provided)
2. **Demo Tools**: Simplified tools that demonstrate how storage operations would work without actually connecting to cloud services

The demo tools allow you to understand how the APIs work without needing actual cloud credentials.

## Code Walkthrough

### Storage Tools

The example creates three main tools for cloud storage:

```python
@tool(
    description="Upload a file to cloud storage",
    parameters={
        "provider_type": {
            "type": "string",
            "description": "Storage provider type (gcs, s3)",
            "enum": ["gcs", "s3", "google", "aws"],
        },
        "file_content": {
            "type": "string",
            "description": "Content of the file to upload",
        },
        "destination_path": {
            "type": "string",
            "description": "Path in the storage where the file should be stored",
        },
        "bucket_name": {
            "type": "string",
            "description": "Name of the storage bucket",
        },
        # Additional parameters...
    },
    group="storage"
)
def upload_file(
    provider_type: str,
    file_content: str,
    destination_path: str,
    bucket_name: str,
    # Additional parameters...
) -> Dict[str, Any]:
    # Implementation details...
```

Similar tools are provided for downloading and listing files.

### Demo Tools

The example also includes simplified demo tools:

```python
@tool(
    description="Store a simple text file in the cloud",
    parameters={
        "content": {
            "type": "string",
            "description": "Content to store in the file",
        },
        "filename": {
            "type": "string",
            "description": "Name of the file to create",
        },
    },
    group="examples"
)
def store_text_file(content: str, filename: str):
    """Simplified demo tool for storage operations."""
    # Implementation that simulates storage operations...
```

## Provider Factory Pattern

The example demonstrates the factory pattern for creating storage providers:

```python
def get_storage_provider(provider_type: str, **credentials) -> StorageProvider:
    """Get a storage provider instance based on the provider type."""
    provider_type = provider_type.lower()
    
    if provider_type == "gcs" or provider_type == "google":
        return GoogleCloudStorageProvider(...)
    elif provider_type == "s3" or provider_type == "aws":
        return AWSS3Provider(...)
    else:
        raise ValueError(f"Unsupported storage provider type: {provider_type}")
```

## Next Steps

After understanding this example, you can:

1. Connect to your actual cloud storage accounts
2. Add support for additional operations (move, copy, delete)
3. Implement additional storage providers
4. Build more complex applications that manage files across providers 