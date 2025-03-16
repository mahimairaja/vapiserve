"""Base class for task management providers."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class TaskProvider(ABC):
    """Abstract base class for task management service providers."""

    @abstractmethod
    def create_task(
        self, 
        title: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """Create a task.
        
        Args:
            title: Task title
            **kwargs: Additional parameters (description, due_date, etc.)
            
        Returns:
            Dict containing the created task details
        """
        pass
    
    @abstractmethod
    def list_tasks(
        self, 
        max_results: int = 10, 
        **kwargs
    ) -> List[Dict[str, Any]]:
        """List tasks with optional filtering.
        
        Args:
            max_results: Maximum number of tasks to return
            **kwargs: Additional parameters for filtering (project, status, etc.)
            
        Returns:
            List of tasks matching the criteria
        """
        pass
    
    @abstractmethod
    def get_task(self, task_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific task by ID.
        
        Args:
            task_id: ID of the task to retrieve
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the task details
        """
        pass
    
    @abstractmethod
    def update_task(
        self, 
        task_id: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """Update an existing task.
        
        Args:
            task_id: ID of the task to update
            **kwargs: Fields to update (title, description, due_date, status, etc.)
            
        Returns:
            Dict containing the updated task details
        """
        pass
    
    @abstractmethod
    def delete_task(self, task_id: str, **kwargs) -> bool:
        """Delete a task.
        
        Args:
            task_id: ID of the task to delete
            **kwargs: Additional parameters
            
        Returns:
            True if deletion was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def complete_task(self, task_id: str, **kwargs) -> Dict[str, Any]:
        """Mark a task as complete.
        
        Args:
            task_id: ID of the task to mark as complete
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the task details
        """
        pass
        
    @abstractmethod
    def list_projects(self, **kwargs) -> List[Dict[str, Any]]:
        """List projects or task lists.
        
        Args:
            **kwargs: Filtering parameters
            
        Returns:
            List of projects available to the user
        """
        pass 