"""Base class for AI service providers."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class AIProvider(ABC):
    """Abstract base class for AI service providers."""

    @abstractmethod
    def generate_text(
        self, 
        prompt: str, 
        **kwargs
    ) -> str:
        """Generate text using an AI model.
        
        Args:
            prompt: Text prompt to generate from
            **kwargs: Additional parameters (max_tokens, temperature, etc.)
            
        Returns:
            Generated text
        """
        pass
    
    @abstractmethod
    def generate_chat_response(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> Dict[str, Any]:
        """Generate a chat response using an AI model.
        
        Args:
            messages: List of message objects with role and content
            **kwargs: Additional parameters (max_tokens, temperature, etc.)
            
        Returns:
            Dict containing the response and metadata
        """
        pass
    
    @abstractmethod
    def embed_text(
        self, 
        text: str, 
        **kwargs
    ) -> List[float]:
        """Generate embeddings for text.
        
        Args:
            text: Text to embed
            **kwargs: Additional parameters
            
        Returns:
            Vector embedding as a list of floats
        """
        pass
        
    @abstractmethod
    def list_models(
        self, 
        **kwargs
    ) -> List[Dict[str, Any]]:
        """List available AI models.
        
        Args:
            **kwargs: Filtering parameters
            
        Returns:
            List of available models with metadata
        """
        pass 