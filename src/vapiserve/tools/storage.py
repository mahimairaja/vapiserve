"""Storage tools for Vapi."""

import os
from typing import Dict, List, Optional, Union, Any

from ..core.tool import tool
from ..integrations.storage import (
    StorageProvider,
    GoogleCloudStorageProvider,
    AWSS3Provider,
)


def get_storage_provider(provider_type: str, **credentials) -> StorageProvider:
    """Get a storage provider instance based on the provider type.
    
    Args:
        provider_type: Type of storage provider (gcs, s3)
        **credentials: Credentials and configuration for the provider
        
    Returns:
        StorageProvider instance
    
    Raises:
        ValueError: If provider_type is not supported
    """
    provider_type = provider_type.lower()
    
    if provider_type == "gcs" or provider_type == "google":
        return GoogleCloudStorageProvider(
            bucket_name=credentials.get("bucket_name"),
            credentials_json_or_path=credentials.get("credentials_json_or_path"),
            project_id=credentials.get("project_id"),
        )
    elif provider_type == "s3" or provider_type == "aws":
        return AWSS3Provider(
            bucket_name=credentials.get("bucket_name"),
            aws_access_key_id=credentials.get("aws_access_key_id"),
            aws_secret_access_key=credentials.get("aws_secret_access_key"),
            aws_session_token=credentials.get("aws_session_token"),
            region_name=credentials.get("region_name"),
            endpoint_url=credentials.get("endpoint_url"),
        )
    else:
        raise ValueError(f"Unsupported storage provider type: {provider_type}")


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
        "content_type": {
            "type": "string",
            "description": "MIME type of the file",
            "optional": True,
        },
        "metadata": {
            "type": "object",
            "description": "Additional metadata to store with the file",
            "optional": True,
        },
    },
    group="storage"
)
def upload_file(
    provider_type: str,
    file_content: str,
    destination_path: str,
    bucket_name: str,
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    **credentials
) -> Dict[str, Any]:
    """Upload a file to cloud storage.
    
    Args:
        provider_type: Storage provider type (gcs, s3)
        file_content: Content of the file to upload
        destination_path: Path in the storage where the file should be stored
        bucket_name: Name of the storage bucket
        content_type: MIME type of the file
        metadata: Additional metadata to store with the file
        **credentials: Additional credentials for the provider
        
    Returns:
        Dict containing the upload result
    """
    # TODO: Implement file upload using the storage provider
    
    provider = get_storage_provider(
        provider_type=provider_type,
        bucket_name=bucket_name,
        **credentials
    )
    
    # Convert string content to bytes if needed
    if isinstance(file_content, str):
        file_content_bytes = file_content.encode("utf-8")
    else:
        file_content_bytes = file_content
    
    # Upload the file
    result = provider.upload_file(
        file_content=file_content_bytes,
        destination_path=destination_path,
        content_type=content_type,
        metadata=metadata,
    )
    
    return result


@tool(
    description="Download a file from cloud storage",
    parameters={
        "provider_type": {
            "type": "string",
            "description": "Storage provider type (gcs, s3)",
            "enum": ["gcs", "s3", "google", "aws"],
        },
        "file_path": {
            "type": "string",
            "description": "Path of the file in storage to download",
        },
        "bucket_name": {
            "type": "string",
            "description": "Name of the storage bucket",
        },
    },
    group="storage"
)
def download_file(
    provider_type: str,
    file_path: str,
    bucket_name: str,
    **credentials
) -> str:
    """Download a file from cloud storage.
    
    Args:
        provider_type: Storage provider type (gcs, s3)
        file_path: Path of the file in storage to download
        bucket_name: Name of the storage bucket
        **credentials: Additional credentials for the provider
        
    Returns:
        File content as a string (base64 encoded if binary)
    """
    # TODO: Implement file download using the storage provider
    
    provider = get_storage_provider(
        provider_type=provider_type,
        bucket_name=bucket_name,
        **credentials
    )
    
    # Download the file
    content = provider.download_file(file_path=file_path)
    
    # Try to decode as UTF-8 text, otherwise return as base64
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        import base64
        return base64.b64encode(content).decode("ascii")


@tool(
    description="List files in cloud storage",
    parameters={
        "provider_type": {
            "type": "string",
            "description": "Storage provider type (gcs, s3)",
            "enum": ["gcs", "s3", "google", "aws"],
        },
        "directory_path": {
            "type": "string",
            "description": "Path of the directory in storage to list",
        },
        "bucket_name": {
            "type": "string",
            "description": "Name of the storage bucket",
        },
        "recursive": {
            "type": "boolean",
            "description": "Whether to list files in subdirectories",
            "optional": True,
        },
    },
    group="storage"
)
def list_files(
    provider_type: str,
    directory_path: str,
    bucket_name: str,
    recursive: bool = False,
    **credentials
) -> List[Dict[str, Any]]:
    """List files in cloud storage.
    
    Args:
        provider_type: Storage provider type (gcs, s3)
        directory_path: Path of the directory in storage to list
        bucket_name: Name of the storage bucket
        recursive: Whether to list files in subdirectories
        **credentials: Additional credentials for the provider
        
    Returns:
        List of file metadata
    """
    # TODO: Implement file listing using the storage provider
    
    provider = get_storage_provider(
        provider_type=provider_type,
        bucket_name=bucket_name,
        **credentials
    )
    
    # List the files
    files = provider.list_files(
        directory_path=directory_path,
        recursive=recursive,
    )
    
    return files 