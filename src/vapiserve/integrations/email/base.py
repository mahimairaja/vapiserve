"""Base class for email service providers."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class EmailProvider(ABC):
    """Abstract base class for email service providers."""

    @abstractmethod
    def send_email(
        self, 
        to: Union[str, List[str]],
        subject: str,
        body: str,
        from_email: Optional[str] = None,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        html_body: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send an email.
        
        Args:
            to: Recipient email address(es)
            subject: Email subject
            body: Plain text email body
            from_email: Sender email address
            cc: Carbon copy recipient(s)
            bcc: Blind carbon copy recipient(s)
            html_body: HTML version of the email body
            attachments: List of attachments
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the send result
        """
        pass
    
    @abstractmethod
    def send_template_email(
        self,
        to: Union[str, List[str]],
        template_id: str,
        template_data: Dict[str, Any],
        from_email: Optional[str] = None,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send an email using a template.
        
        Args:
            to: Recipient email address(es)
            template_id: ID of the email template to use
            template_data: Data to populate the template
            from_email: Sender email address
            cc: Carbon copy recipient(s)
            bcc: Blind carbon copy recipient(s)
            attachments: List of attachments
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the send result
        """
        pass
    
    @abstractmethod
    def get_email_status(
        self,
        message_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Get the status of a sent email.
        
        Args:
            message_id: ID of the email to check
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the email status
        """
        pass 