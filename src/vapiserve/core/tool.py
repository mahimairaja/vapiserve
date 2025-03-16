"""Tool implementation for Vapi custom tools."""

import inspect
import json
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Type, get_type_hints

from pydantic import BaseModel, create_model

from .models import ToolDefinition, ToolSchema


class VapiTool:
    """A class that wraps a function to be used as a Vapi tool."""

    def __init__(
        self,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
        server_url: Optional[str] = None,
        group: str = "tools",
    ):
        """Initialize a VapiTool.

        Args:
            func: The function to be exposed as a tool
            name: The name of the tool (defaults to function name)
            description: Description of the tool (defaults to function docstring)
            server_url: URL where the tool is hosted
            group: Tag/group name for organizing tools in the Swagger UI
        """
        self.func = func
        self.name = name or func.__name__
        self.description = description or inspect.getdoc(func) or ""
        self.server_url = server_url
        self.group = group
        
        # Extract parameter info from function signature
        self.signature = inspect.signature(func)
        self.type_hints = get_type_hints(func)
        
        # Create a Pydantic model for the function parameters
        self._create_parameters_model()
    
    def _create_parameters_model(self) -> None:
        """Create a Pydantic model from the function parameters."""
        fields = {}
        required_params = []
        
        for param_name, param in self.signature.parameters.items():
            # Skip self parameter if it's a method
            if param_name == "self":
                continue
                
            # Get type annotation (default to Any if not specified)
            param_type = self.type_hints.get(param_name, Any)
            
            # Check if parameter has a default value
            if param.default is inspect.Parameter.empty:
                required_params.append(param_name)
                fields[param_name] = (param_type, ...)
            else:
                fields[param_name] = (param_type, param.default)
        
        # Create the model dynamically
        model_name = f"{self.name.capitalize()}Parameters"
        self.parameters_model = create_model(model_name, **fields)
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the JSON Schema for the tool parameters."""
        schema = self.parameters_model.model_json_schema()
        
        # Vapi expects a slightly different format than the default Pydantic schema
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        
        return {
            "properties": properties,
            "required": required,
            "type": "object"
        }
    
    def get_tool_definition(self, server_url: Optional[str] = None) -> ToolDefinition:
        """Get the tool definition for registering with Vapi.
        
        Args:
            server_url: Override the server URL
            
        Returns:
            ToolDefinition: The tool definition
        """
        url = server_url or self.server_url
        if not url:
            raise ValueError("Server URL must be provided")
            
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters=self.get_schema(),
            server={"url": url}
        )
    
    def get_tool_schema(self, server_url: Optional[str] = None) -> ToolSchema:
        """Get the complete tool schema for registering with Vapi.
        
        Args:
            server_url: Override the server URL
            
        Returns:
            ToolSchema: The complete tool schema
        """
        return ToolSchema(
            type="function",
            function=self.get_tool_definition(server_url)
        )
    
    async def __call__(self, **kwargs: Any) -> Any:
        """Execute the tool function with the given arguments.
        
        Args:
            **kwargs: Arguments to pass to the function
            
        Returns:
            The result of the function
        """
        # Validate arguments against the parameters model
        validated_args = self.parameters_model(**kwargs)
        
        # Convert to dict for passing to the function
        args_dict = validated_args.model_dump()
        
        # Call the function
        if inspect.iscoroutinefunction(self.func):
            return await self.func(**args_dict)
        else:
            return self.func(**args_dict)


def tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    server_url: Optional[str] = None,
    group: str = "tools",
) -> Callable:
    """Decorator to mark a function as a Vapi tool.
    
    Args:
        name: The name of the tool (defaults to function name)
        description: Description of the tool (defaults to function docstring)
        server_url: URL where the tool is hosted
        group: Tag/group name for organizing tools in the Swagger UI
        
    Returns:
        A decorator function
    """
    def decorator(func: Callable) -> VapiTool:
        """Create a VapiTool from the decorated function.
        
        Args:
            func: The function to decorate
            
        Returns:
            VapiTool: The wrapped function
        """
        return VapiTool(
            func=func,
            name=name or func.__name__,
            description=description or inspect.getdoc(func),
            server_url=server_url,
            group=group,
        )
    
    return decorator 