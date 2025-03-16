"""Base class for calendar providers."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class CalendarProvider(ABC):
    """Abstract base class for calendar service providers."""

    @abstractmethod
    def create_event(
        self, 
        summary: str, 
        start_time: str, 
        end_time: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """Create a calendar event.
        
        Args:
            summary: Event title/summary
            start_time: Start time (ISO format)
            end_time: End time (ISO format)
            **kwargs: Additional parameters (location, description, etc.)
            
        Returns:
            Dict containing the created event details
        """
        pass
    
    @abstractmethod
    def list_events(
        self, 
        time_min: Optional[str] = None, 
        time_max: Optional[str] = None, 
        max_results: int = 10, 
        **kwargs
    ) -> List[Dict[str, Any]]:
        """List calendar events in a specified time range.
        
        Args:
            time_min: Start time for listing events (ISO format)
            time_max: End time for listing events (ISO format)
            max_results: Maximum number of events to return
            **kwargs: Additional parameters
            
        Returns:
            List of events matching the criteria
        """
        pass
    
    @abstractmethod
    def get_event(self, event_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific calendar event by ID.
        
        Args:
            event_id: ID of the event to retrieve
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the event details
        """
        pass
    
    @abstractmethod
    def update_event(
        self, 
        event_id: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """Update an existing calendar event.
        
        Args:
            event_id: ID of the event to update
            **kwargs: Fields to update (summary, start_time, end_time, etc.)
            
        Returns:
            Dict containing the updated event details
        """
        pass
    
    @abstractmethod
    def delete_event(self, event_id: str, **kwargs) -> bool:
        """Delete a calendar event.
        
        Args:
            event_id: ID of the event to delete
            **kwargs: Additional parameters
            
        Returns:
            True if deletion was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_free_busy(
        self, 
        time_min: str, 
        time_max: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Get free/busy information for a calendar.
        
        Args:
            time_min: Start time for checking free/busy (ISO format)
            time_max: End time for checking free/busy (ISO format)
            **kwargs: Additional parameters
            
        Returns:
            Dict containing busy periods
        """
        pass 