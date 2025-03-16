"""Command-line interface for Vapiserve."""

import argparse
import importlib
import inspect
import logging
import os
import sys
from typing import Dict, List, Optional

from .core.server import VapiServer
from .core.tool import VapiTool
from .utils.ngrok import start_ngrok

logger = logging.getLogger(__name__)


def find_tools(module_path: str) -> List[VapiTool]:
    """Find all VapiTool instances in a module.
    
    Args:
        module_path: Import path to the module (e.g., "myapp.tools")
        
    Returns:
        List of VapiTool instances found in the module
    """
    try:
        # Import the module
        module = importlib.import_module(module_path)
        
        # Find all VapiTool instances
        tools = []
        for name, obj in inspect.getmembers(module):
            if isinstance(obj, VapiTool):
                tools.append(obj)
                
        return tools
        
    except Exception as e:
        logger.error(f"Error finding tools in {module_path}: {e}")
        return []


def main():
    """Run the CLI."""
    parser = argparse.ArgumentParser(description="Vapiserve - A Vapi tools server")
    
    parser.add_argument(
        "--host", 
        type=str, 
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    
    parser.add_argument(
        "--module", 
        type=str, 
        required=True,
        help="Import path to the module containing tools (e.g., 'myapp.tools')"
    )
    
    parser.add_argument(
        "--reload", 
        action="store_true",
        help="Enable auto-reload on code changes"
    )
    
    parser.add_argument(
        "--log-level", 
        type=str,
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Logging level (default: info)"
    )
    
    parser.add_argument(
        "--title", 
        type=str,
        default="Vapi Tools API",
        help="API title for documentation"
    )
    
    parser.add_argument(
        "--description", 
        type=str,
        default="API for Vapi custom tools",
        help="API description for documentation"
    )
    
    parser.add_argument(
        "--ngrok", 
        action="store_true",
        help="Expose the server via ngrok"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    
    # Find tools in the module
    tools = find_tools(args.module)
    
    if not tools:
        logger.error(f"No tools found in module {args.module}")
        sys.exit(1)
        
    logger.info(f"Found {len(tools)} tools in {args.module}")
    
    # Start ngrok if requested
    if args.ngrok:
        public_url = start_ngrok(port=args.port)
        if public_url:
            logger.info(f"Server accessible at {public_url}")
            
            # Update tool URLs
            for tool in tools:
                tool.server_url = public_url
        else:
            logger.error("Failed to start ngrok tunnel")
            sys.exit(1)
    
    # Create server
    server = VapiServer(
        title=args.title,
        description=args.description,
    )
    
    # Register tools
    server.register_tools(*tools)
    
    # Start server
    try:
        server.serve(
            host=args.host,
            port=args.port,
            log_level=args.log_level,
            reload=args.reload,
        )
    except KeyboardInterrupt:
        logger.info("Server stopped")


if __name__ == "__main__":
    main() 