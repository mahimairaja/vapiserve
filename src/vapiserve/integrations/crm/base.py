"""Base class for CRM providers."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class CrmProvider(ABC):
    """Abstract base class for Customer Relationship Management (CRM) providers."""

    @abstractmethod
    def create_contact(
        self, 
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a new contact in the CRM.
        
        Args:
            email: Email address of the contact
            first_name: First name of the contact
            last_name: Last name of the contact
            **kwargs: Additional fields for the contact
            
        Returns:
            Dict containing the created contact details
        """
        pass
    
    @abstractmethod
    def get_contact(
        self, 
        contact_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Get a contact by ID.
        
        Args:
            contact_id: ID of the contact to retrieve
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the contact details
        """
        pass
    
    @abstractmethod
    def update_contact(
        self, 
        contact_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Update an existing contact.
        
        Args:
            contact_id: ID of the contact to update
            **kwargs: Fields to update
            
        Returns:
            Dict containing the updated contact details
        """
        pass
    
    @abstractmethod
    def delete_contact(
        self, 
        contact_id: str,
        **kwargs
    ) -> bool:
        """Delete a contact.
        
        Args:
            contact_id: ID of the contact to delete
            **kwargs: Additional parameters
            
        Returns:
            True if deletion was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def search_contacts(
        self,
        query: str,
        limit: int = 10,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search for contacts.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            **kwargs: Additional search parameters
            
        Returns:
            List of contacts matching the search criteria
        """
        pass
    
    @abstractmethod
    def create_deal(
        self,
        name: str,
        contact_id: Optional[str] = None,
        value: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a new deal or opportunity.
        
        Args:
            name: Name of the deal
            contact_id: ID of the associated contact
            value: Value of the deal
            **kwargs: Additional deal parameters
            
        Returns:
            Dict containing the created deal details
        """
        pass
    
    @abstractmethod
    def update_deal(
        self,
        deal_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Update an existing deal.
        
        Args:
            deal_id: ID of the deal to update
            **kwargs: Fields to update
            
        Returns:
            Dict containing the updated deal details
        """
        pass 