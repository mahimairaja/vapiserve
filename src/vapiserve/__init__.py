"""VapiServe: A framework for building API servers for Vapi custom tools."""

__version__ = "0.1.0"

from .core.server import VapiServer, serve
from .core.tool import VapiTool, tool
from .core.models import ToolCall, ToolResponse, ToolResult

__all__ = [
    "VapiServer",
    "serve",
    "VapiTool",
    "tool",
    "ToolCall",
    "ToolResponse",
    "ToolResult"
] 