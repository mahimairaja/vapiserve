"""Server implementation for Vapi custom tools."""

import asyncio
import inspect
import logging
import os
from typing import Any, Callable, Dict, List, Optional, Type, Union

try:
    import click
    HAS_CLICK = True
except ImportError:
    HAS_CLICK = False

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, create_model, Field

from .models import ToolCall, ToolResponse, ToolResult
from .tool import VapiTool

# Import ngrok utilities
try:
    from ..utils.ngrok import setup_ngrok_for_server
    HAS_NGROK = True
except ImportError:
    HAS_NGROK = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Define a model for Vapi tool call requests
class VapiToolCallRequest(BaseModel):
    """Model for Vapi tool call requests."""
    
    toolCallId: str = Field(..., description="Unique identifier for the tool call")
    name: str = Field(..., description="Name of the tool being called")
    arguments: Dict[str, Any] = Field(..., description="Arguments passed to the tool")
    
    class Config:
        """Pydantic config."""
        
        extra = "allow"  # Allow extra fields that might be sent by Vapi


# Define a model for Vapi batch tool call requests
class VapiBatchToolCallRequest(BaseModel):
    """Model for Vapi batch tool call requests."""
    
    toolCalls: List[VapiToolCallRequest] = Field(..., description="List of tool calls to execute")
    
    class Config:
        """Pydantic config."""
        
        extra = "allow"  # Allow extra fields that might be sent by Vapi


class VapiServer:
    """Server for handling Vapi custom tool requests."""

    def __init__(
        self,
        title: str = "Vapi Tools API",
        description: str = "API for Vapi custom tools",
        version: str = "0.1.0",
        root_path: str = "",
    ):
        """Initialize a VapiServer.
        
        Args:
            title: Title of the API (shown in docs)
            description: Description of the API
            version: API version
            root_path: Root path for the API (useful when behind a proxy)
        """
        # Default tag for information endpoints
        info_tag = {
            "name": "info",
            "description": "General information about the API"
        }
        
        # Tag for vapi-specific endpoints (always at the bottom)
        vapi_tag = {
            "name": "vapi-tools",
            "description": "Endpoints formatted specifically for Vapi integration"
        }
        
        # Create the app with tag ordering
        self.app = FastAPI(
            title=title,
            description=description,
            version=version,
            root_path=root_path,
            openapi_tags=[info_tag, vapi_tag]  # This will be dynamically extended with tool groups
        )
        
        # Set up CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Dictionary to store registered tools
        self.tools: Dict[str, VapiTool] = {}
        
        # Dictionary to track available tool groups
        self.tool_groups: Dict[str, List[str]] = {}
        
        # Set up default routes
        self._setup_default_routes()
        
    def _setup_default_routes(self) -> None:
        """Set up default routes for the server."""
        
        @self.app.get("/", tags=["info"])
        async def root():
            """Root endpoint."""
            return {
                "name": self.app.title,
                "description": self.app.description,
                "version": self.app.version,
                "tools": list(self.tools.keys()),
                "groups": self.tool_groups,
            }
        
        @self.app.get("/health", tags=["info"])
        async def health():
            """Health check endpoint."""
            return {"status": "ok"}
        
        @self.app.get("/tools", tags=["info"])
        async def list_tools():
            """List all registered tools."""
            return {
                "tools": [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.get_schema(),
                        "group": tool.group,
                    }
                    for tool in self.tools.values()
                ],
                "groups": self.tool_groups,
            }
    
    def _create_request_model(self, tool: VapiTool) -> Type[BaseModel]:
        """Create a Pydantic model for the tool's request parameters.
        
        Args:
            tool: The tool to create a model for
            
        Returns:
            A Pydantic model class for the tool's parameters
        """
        # Get the tool's parameter schema
        schema = tool.get_schema()
        
        # Create field definitions
        field_definitions = {}
        for name, details in schema.get("properties", {}).items():
            # Get the field type
            field_type = Any
            if details.get("type") == "string":
                field_type = str
            elif details.get("type") == "integer":
                field_type = int
            elif details.get("type") == "number":
                field_type = float
            elif details.get("type") == "boolean":
                field_type = bool
            elif details.get("type") == "array":
                field_type = List[Any]
            elif details.get("type") == "object":
                field_type = Dict[str, Any]
            
            # Check if field is required
            required = name in schema.get("required", [])
            
            # Get default value if any
            default = details.get("default", ... if required else None)
            
            # Add field to definitions
            field_definitions[name] = (field_type, default)
        
        # Create and return the model
        return create_model(
            f"{tool.name.capitalize()}Request",
            **field_definitions
        )
    
    def add_tool(self, tool: VapiTool) -> None:
        """Add a tool to the server.
        
        Args:
            tool: The tool to add
        """
        if tool.name in self.tools:
            logger.warning(f"Tool '{tool.name}' already registered, replacing it")
            
        self.tools[tool.name] = tool
        
        # Add tool to group mapping
        if tool.group not in self.tool_groups:
            self.tool_groups[tool.group] = []
            
            # Add new tool group to OpenAPI tags if not already there
            # This ensures that new groups appear in the UI in the order they're added
            # (but still before vapi-tools which is always last)
            group_exists = False
            for tag in self.app.openapi_tags:
                if tag.get("name") == tool.group:
                    group_exists = True
                    break
                
            if not group_exists:
                # Insert the new group tag before the vapi-tools tag (which should be last)
                self.app.openapi_tags.insert(
                    len(self.app.openapi_tags) - 1,  # Insert before the last tag (vapi-tools)
                    {"name": tool.group, "description": f"Tools in the {tool.group} group"}
                )
        
        if tool.name not in self.tool_groups[tool.group]:
            self.tool_groups[tool.group].append(tool.name)
        
        # Create a request model for the tool
        request_model = self._create_request_model(tool)
        
        # Create POST endpoint for the tool
        @self.app.post(f"/tools/{tool.name}", tags=[tool.group])
        async def handle_tool_call(request_body: request_model):
            """Handle a call to this tool."""
            try:
                # Convert request body to dict
                body = request_body.dict()
                
                # Log incoming request
                logger.info(f"Received tool call: {body}")
                
                # Create a tool call
                tool_call = ToolCall(
                    toolCallId=body.get("toolCallId", "default-id"),
                    name=tool.name,
                    arguments=body
                )
                
                # Execute the tool
                try:
                    # Execute the tool function
                    result = await tool(**tool_call.arguments)
                    
                    # Return the result directly for the regular endpoint
                    # This provides a simpler response format for direct API usage
                    return JSONResponse(content=result)
                
                except Exception as e:
                    # Log the error
                    logger.exception(f"Error executing tool {tool_call.name}")
                    
                    # Return a simple error response
                    return JSONResponse(
                        content={"error": str(e)},
                        status_code=500
                    )
            
            except Exception as e:
                logger.exception("Error processing request")
                raise HTTPException(status_code=400, detail=str(e))
        
        # Also support Vapi's format with a separate endpoint
        @self.app.post(f"/tools/{tool.name}/vapi", tags=["vapi-tools"])
        async def handle_vapi_call(
            request_body: Union[VapiToolCallRequest, VapiBatchToolCallRequest] = Body(
                ...,
                examples=[
                    {
                        "toolCallId": "example-id",
                        "name": tool.name,
                        "arguments": {k: "..." for k in request_model.__annotations__}
                    },
                    {
                        "toolCalls": [
                            {
                                "toolCallId": "batch-example-id",
                                "name": tool.name,
                                "arguments": {k: "..." for k in request_model.__annotations__}
                            }
                        ]
                    }
                ]
            )
        ):
            """Handle a Vapi-format call to this tool.
            
            This endpoint supports both single tool calls and batched tool calls in Vapi format.
            """
            try:
                # Convert request to dict
                body = request_body.dict()
                
                # Log incoming request
                logger.info(f"Received Vapi tool call: {body}")
                
                # Extract tool calls
                tool_calls = []
                if "toolCalls" in body:
                    # Handle batch of tool calls
                    tool_calls = [ToolCall(**call) for call in body["toolCalls"]]
                else:
                    # Handle single tool call
                    tool_calls = [ToolCall(**body)]
                
                # Process each tool call
                results = []
                for call in tool_calls:
                    try:
                        if call.name != tool.name:
                            raise ValueError(f"Tool name mismatch: {call.name} vs {tool.name}")
                        
                        # Execute the tool with the provided arguments
                        result = await tool(**call.arguments)
                        
                        # Add successful result (no error field)
                        results.append({
                            "toolCallId": call.toolCallId,
                            "result": result
                        })
                    
                    except Exception as e:
                        # Log the error
                        logger.exception(f"Error executing tool {call.name}")
                        
                        # Add error result (no result field)
                        results.append({
                            "toolCallId": call.toolCallId,
                            "error": str(e)
                        })
                
                # Return direct JSON response
                return JSONResponse(content={"results": results})
            
            except Exception as e:
                logger.exception("Error processing request")
                raise HTTPException(status_code=400, detail=str(e))
    
    def register_tools(self, *tools: VapiTool) -> None:
        """Register multiple tools with the server.
        
        Args:
            *tools: Tools to register
        """
        for tool in tools:
            self.add_tool(tool)
    
    def _display_banner(self, host: str, port: int, public_url: Optional[str] = None) -> None:
        """Display a stylish server startup banner.
        
        Args:
            host: The host the server is running on
            port: The port the server is running on
            public_url: Public ngrok URL if available
        """
        if not HAS_CLICK:
            logger.info(f"Starting {self.app.title} at {host}:{port}")
            if public_url:
                logger.info(f"Public URL: {public_url}")
            return
            
        # Get the list of registered tools
        tools_by_group = {}
        for name, tool in self.tools.items():
            group = tool.group
            if group not in tools_by_group:
                tools_by_group[group] = []
            tools_by_group[group].append((name, tool.description))
        
        # Display the banner
        click.secho(f"  Starting VapiServe server!", fg="bright_green", bold=True)
        
        # Display server info
        API_URI = f"http://{host if host != '0.0.0.0' else 'localhost'}:{port}/"
        DOCS_URI = f"{API_URI}docs"

        click.echo("  Local server: " + 
                   click.style(f"{API_URI}", fg="yellow"))
        click.echo("  API Documentation: " + 
                   click.style(f"{DOCS_URI}", fg="yellow"))
                   
        # Display public URL if ngrok is used
        if public_url:
            click.echo("  Public URL: " + 
                       click.style(f"{public_url}", fg="bright_green", bold=True))
            click.echo("  Public API Docs: " + 
                       click.style(f"{public_url}/docs", fg="bright_green"))
    def serve(
        self,
        host: str = "0.0.0.0",
        port: int = 8000,
        log_level: str = "info",
        reload: bool = False,
        quiet: bool = False,
        use_ngrok: bool = False,
        ngrok_region: str = "us",
        ngrok_auth_token: Optional[str] = None,
    ) -> None:
        """Start the server.
        
        Args:
            host: Host to bind to
            port: Port to bind to
            log_level: Logging level
            reload: Whether to reload on code changes
            quiet: If True, suppress startup messages from uvicorn
            use_ngrok: Whether to expose the server via ngrok
            ngrok_region: ngrok region to use
            ngrok_auth_token: ngrok auth token
        """
        if not self.tools:
            logger.warning("No tools registered")
            
        # Use configured port from environment if available
        port_env = os.environ.get("PORT")
        if port_env:
            try:
                port = int(port_env)
            except ValueError:
                logger.warning(f"Invalid PORT environment variable: {port_env}")
        
        # Set up ngrok if requested
        public_url = None
        if use_ngrok:
            if not HAS_NGROK:
                logger.warning("Ngrok support not available. Make sure ngrok is installed.")
            else:
                try:
                    public_url = setup_ngrok_for_server(
                        port=port,
                        region=ngrok_region,
                        auth_token=ngrok_auth_token,
                        show_url=not quiet
                    )
                    if not public_url and not quiet:
                        logger.warning("Failed to start ngrok tunnel")
                except Exception as e:
                    logger.error(f"Error setting up ngrok: {e}")
        
        # Display a cool banner before starting
        self._display_banner(host, port, public_url)
        
        # When quiet mode is enabled, set log_level to error to suppress info messages
        if quiet:
            log_level = "error"
        
        # Start the server
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            log_level=log_level,
            reload=reload,
        )


def serve(
    *tools: VapiTool,
    title: str = "Vapi Tools API",
    description: str = "API for Vapi custom tools",
    version: str = "0.1.0",
    host: str = "0.0.0.0",
    port: int = 8000,
    log_level: str = "info",
    reload: bool = False,
    quiet: bool = True,
    use_ngrok: bool = False,
    ngrok_region: str = "us",
    ngrok_auth_token: Optional[str] = None,
) -> None:
    """Start a Vapi tools server with the given tools.
    
    Args:
        *tools: Tools to register
        title: Title of the API
        description: Description of the API
        version: API version
        host: Host to bind to
        port: Port to bind to
        log_level: Logging level
        reload: Whether to reload on code changes
        quiet: If True, suppress startup messages from uvicorn
        use_ngrok: Whether to expose the server via ngrok
        ngrok_region: ngrok region to use
        ngrok_auth_token: ngrok auth token (can also be set via NGROK_AUTH_TOKEN env var)
    """
    server = VapiServer(
        title=title,
        description=description,
        version=version,
    )
    
    for tool in tools:
        server.add_tool(tool)
    
    server.serve(
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
        quiet=quiet,
        use_ngrok=use_ngrok,
        ngrok_region=ngrok_region,
        ngrok_auth_token=ngrok_auth_token,
    ) 