"""Utilities for security and API key handling."""

import os
from typing import Dict, Optional

from dotenv import load_dotenv


class ApiKeyManager:
    """A class to manage API keys for various services."""
    
    def __init__(self, env_file: Optional[str] = None):
        """Initialize the API key manager.
        
        Args:
            env_file: Path to a .env file to load keys from
        """
        self.keys: Dict[str, str] = {}
        
        # Load environment variables
        if env_file:
            load_dotenv(env_file)
    
    def add_key(self, name: str, value: str) -> None:
        """Add a key to the manager.
        
        Args:
            name: The name of the key
            value: The key value
        """
        self.keys[name] = value
    
    def get_key(self, name: str, env_var: Optional[str] = None) -> Optional[str]:
        """Get a key from the manager.
        
        Args:
            name: The name of the key
            env_var: Environment variable to check if key not found
            
        Returns:
            The key value, or None if not found
        """
        # Check in-memory keys first
        if name in self.keys:
            return self.keys[name]
        
        # Check environment variables
        if env_var:
            env_value = os.environ.get(env_var)
            if env_value:
                self.keys[name] = env_value
                return env_value
        
        # Check for a variable with the same name
        env_value = os.environ.get(name)
        if env_value:
            self.keys[name] = env_value
            return env_value
            
        return None
    
    def require_key(self, name: str, env_var: Optional[str] = None) -> str:
        """Get a key, raising an error if not found.
        
        Args:
            name: The name of the key
            env_var: Environment variable to check if key not found
            
        Returns:
            The key value
            
        Raises:
            ValueError: If the key is not found
        """
        key = self.get_key(name, env_var)
        if key is None:
            env_name = env_var or name
            raise ValueError(
                f"API key '{name}' is required but not found. "
                f"Please set the '{env_name}' environment variable or add it explicitly."
            )
        return key


# Global instance for easy access
api_keys = ApiKeyManager()


def load_env_file(path: str) -> None:
    """Load environment variables from a .env file.
    
    Args:
        path: Path to the .env file
    """
    load_dotenv(path)


def get_api_key(service: str, env_var: Optional[str] = None) -> Optional[str]:
    """Get an API key for a service.
    
    Args:
        service: The service name
        env_var: Environment variable to check
        
    Returns:
        The API key, or None if not found
    """
    return api_keys.get_key(service, env_var)


def require_api_key(service: str, env_var: Optional[str] = None) -> str:
    """Get an API key for a service, raising an error if not found.
    
    Args:
        service: The service name
        env_var: Environment variable to check
        
    Returns:
        The API key
        
    Raises:
        ValueError: If the API key is not found
    """
    return api_keys.require_key(service, env_var) 