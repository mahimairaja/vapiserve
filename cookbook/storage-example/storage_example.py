#!/usr/bin/env python
"""Example script demonstrating storage tools usage."""

import os
import sys
from pathlib import Path

# Add parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.vapiserve.core.server import VapiServer
from src.vapiserve.core.tool import tool
from src.vapiserve.tools.storage import upload_file, download_file, list_files


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
    """Store a simple text file in cloud storage.
    
    This is a simple wrapper around the upload_file tool that makes it easier
    to store text content without having to provide storage provider details.
    
    Args:
        content: Text content to store
        filename: Name to use for the file
        
    Returns:
        Information about the uploaded file
    """
    # For demo purposes, we're hardcoding these values
    # In a real application, you would get these from environment variables or a config file
    bucket_name = "my-demo-bucket"
    
    # In a real implementation, this would actually call the provider's upload method
    # For now, we just return what would happen
    
    return {
        "message": "In a real implementation, the following would be uploaded:",
        "provider": "gcs (demo only - not actually uploading)",
        "bucket": bucket_name,
        "path": filename,
        "content_length": len(content),
        "content_preview": content[:50] + ("..." if len(content) > 50 else ""),
    }


@tool(
    description="Generate a signed URL for a file",
    parameters={
        "filename": {
            "type": "string",
            "description": "Name of the file to generate a URL for",
        },
        "expiration_seconds": {
            "type": "integer",
            "description": "How long the URL should be valid for (in seconds)",
            "default": 3600,
        },
    },
    group="examples"
)
def get_file_url(filename: str, expiration_seconds: int = 3600):
    """Generate a signed URL for a file in cloud storage.
    
    This is a demo tool that simulates generating a signed URL.
    
    Args:
        filename: Name of the file to generate a URL for
        expiration_seconds: How long the URL should be valid for (in seconds)
        
    Returns:
        Information about the signed URL
    """
    # For demo purposes, we're returning a fake URL
    
    return {
        "message": "In a real implementation, a signed URL would be generated:",
        "provider": "gcs (demo only - not actually generating URL)",
        "filename": filename,
        "expiration_seconds": expiration_seconds,
        "url": f"https://storage.googleapis.com/my-demo-bucket/{filename}?expiry={expiration_seconds}s&signature=demo123",
    }


def main():
    """Run the example server with storage tools."""
    server = VapiServer(
        title="VapiServe Storage Tools Demo",
        description="Demo of storage tools for cloud storage providers",
    )
    
    # Add the storage tools
    server.add_tool(upload_file)
    server.add_tool(download_file)
    server.add_tool(list_files)
    
    # Add our demo tools
    server.add_tool(store_text_file)
    server.add_tool(get_file_url)
    
    # Start the server
    server.serve(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main() 