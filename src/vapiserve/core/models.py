"""Pydantic models for Vapi tools."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """Represents a call to a custom tool from Vapi."""
    
    toolCallId: str = Field(..., description="Unique identifier for the tool call")
    name: str = Field(..., description="Name of the tool being called")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Arguments passed to the tool")
    
    class Config:
        """Pydantic config."""
        
        extra = "allow"  # Allow extra fields that might be sent by Vapi


class ToolResult(BaseModel):
    """The result of a single tool execution."""
    
    toolCallId: str = Field(..., description="Identifier matching the original tool call")
    result: Any = Field(None, description="The result data to return to Vapi")
    error: Optional[str] = Field(None, description="Error message if the tool execution failed")
    
    class Config:
        """Pydantic config."""
        
        extra = "allow"
        exclude_none = True  # Exclude None values from JSON responses
        

class ToolResponse(BaseModel):
    """The response format expected by Vapi."""
    
    results: List[ToolResult] = Field(..., description="Results from tool executions")
    
    class Config:
        """Pydantic config."""
        
        exclude_none = True  # Exclude None values from JSON responses


class ToolDefinition(BaseModel):
    """Defines a tool that can be registered with Vapi."""
    
    name: str = Field(..., description="The name of the tool")
    description: str = Field(..., description="Description of what the tool does")
    parameters: Dict[str, Any] = Field(..., description="JSON Schema of parameters")
    server: Dict[str, str] = Field(
        ..., 
        description="Server config including the URL where the tool is hosted"
    )


class ToolSchema(BaseModel):
    """Schema for a Vapi tool to be published."""
    
    type: str = Field("function", description="Type of tool, currently only 'function' is supported")
    function: ToolDefinition = Field(..., description="Definition of the tool") 