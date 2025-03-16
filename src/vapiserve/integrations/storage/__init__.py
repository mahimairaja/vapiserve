"""Storage service integrations for Vapi tools."""

from .base import StorageProvider
from .google_cloud_storage import GoogleCloudStorageProvider
from .aws_s3 import AWSS3Provider

__all__ = [
    "StorageProvider",
    "GoogleCloudStorageProvider",
    "AWSS3Provider",
] 