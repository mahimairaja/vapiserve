"""Base class for file storage providers."""

from abc import ABC, abstractmethod
import io
from typing import Any, Dict, List, Optional, Union, BinaryIO


class StorageProvider(ABC):
    """Abstract base class for file storage providers."""

    @abstractmethod
    def upload_file(
        self, 
        file_content: Union[str, bytes, BinaryIO],
        destination_path: str,
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Upload a file to storage.
        
        Args:
            file_content: Content of the file to upload
            destination_path: Path where the file should be stored
            content_type: MIME type of the file
            metadata: Additional metadata to store with the file
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the upload result
        """
        pass
    
    @abstractmethod
    def download_file(
        self,
        file_path: str,
        **kwargs
    ) -> bytes:
        """Download a file from storage.
        
        Args:
            file_path: Path of the file to download
            **kwargs: Additional parameters
            
        Returns:
            File content as bytes
        """
        pass
    
    @abstractmethod
    def get_file_metadata(
        self,
        file_path: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Get metadata for a file.
        
        Args:
            file_path: Path of the file
            **kwargs: Additional parameters
            
        Returns:
            Dict containing file metadata
        """
        pass
    
    @abstractmethod
    def delete_file(
        self,
        file_path: str,
        **kwargs
    ) -> bool:
        """Delete a file from storage.
        
        Args:
            file_path: Path of the file to delete
            **kwargs: Additional parameters
            
        Returns:
            True if deletion was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def list_files(
        self,
        directory_path: str,
        recursive: bool = False,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """List files in a directory.
        
        Args:
            directory_path: Path of the directory to list
            recursive: Whether to list files in subdirectories
            **kwargs: Additional parameters
            
        Returns:
            List of file metadata
        """
        pass
    
    @abstractmethod
    def generate_signed_url(
        self,
        file_path: str,
        expiration: int,
        **kwargs
    ) -> str:
        """Generate a signed URL for temporary access to a file.
        
        Args:
            file_path: Path of the file
            expiration: Expiration time in seconds
            **kwargs: Additional parameters
            
        Returns:
            Signed URL
        """
        pass 