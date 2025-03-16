"""Base class for communication tool providers."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class CommunicationProvider(ABC):
    """Abstract base class for communication service providers."""

    @abstractmethod
    def send_message(
        self, 
        content: str, 
        recipient: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Send a message to a recipient.
        
        Args:
            content: Message content
            recipient: Recipient identifier (channel, phone number, etc.)
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the sent message details
        """
        pass
    
    @abstractmethod
    def list_channels(
        self, 
        **kwargs
    ) -> List[Dict[str, Any]]:
        """List available channels/conversations.
        
        Args:
            **kwargs: Filtering parameters
            
        Returns:
            List of channels/conversations
        """
        pass 