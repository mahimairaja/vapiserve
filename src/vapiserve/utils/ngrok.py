"""Utilities for ngrok integration."""

import asyncio
import atexit
import json
import logging
import os
import subprocess
import sys
import time
from typing import Dict, Optional, Union

import httpx

# Configure logging
logger = logging.getLogger(__name__)

# Set the httpx logger to WARNING level to suppress INFO logs about requests
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)


class NgrokTunnel:
    """A class to manage an ngrok tunnel."""

    def __init__(
        self,
        port: int = 8000,
        region: str = "us",
        auth_token: Optional[str] = None,
        executable: str = "ngrok",
    ):
        """Initialize an ngrok tunnel.
        
        Args:
            port: The port to tunnel to
            region: The ngrok region to use
            auth_token: The ngrok auth token
            executable: The ngrok executable path
        """
        self.port = port
        self.region = region
        self.auth_token = auth_token or os.environ.get("NGROK_AUTH_TOKEN")
        self.executable = executable
        self.process = None
        self.public_url = None
        self.api_url = "http://localhost:4040/api"
        
    def start(self, retries: int = 3, retry_delay: int = 1) -> Optional[str]:
        """Start the ngrok tunnel.
        
        Args:
            retries: Number of times to retry starting ngrok
            retry_delay: Delay between retries in seconds
            
        Returns:
            The public URL of the tunnel, or None if it failed
        """
        if self.process is not None:
            logger.warning("Ngrok tunnel already running")
            return self.public_url
            
        cmd = [self.executable, "http", str(self.port), "--region", self.region]
        
        if self.auth_token:
            cmd.extend(["--authtoken", self.auth_token])
        
        # Start ngrok
        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            
            # Register cleanup function
            atexit.register(self.stop)
            
            # Wait for ngrok to start
            for i in range(retries):
                try:
                    time.sleep(retry_delay)
                    self.public_url = self._get_public_url()
                    if self.public_url:
                        # logger.info(f"Ngrok tunnel started: {self.public_url}")
                        return self.public_url
                except Exception as e:
                    # For retry attempts, only log as a warning
                    if i < retries - 1:
                        # This is a retry attempt, not a final failure
                        logger.debug(f"Waiting for ngrok to start (attempt {i+1}/{retries}): {e}")
                    else:
                        # This was the last attempt, log as error
                        logger.error(f"Failed to get ngrok URL after {retries} attempts: {e}")
                        self.stop()
                        return None
            
            logger.error("Failed to start ngrok tunnel")
            self.stop()
            return None
            
        except Exception as e:
            logger.error(f"Failed to start ngrok: {e}")
            return None
            
    def _get_public_url(self) -> Optional[str]:
        """Get the public URL from the ngrok API.
        
        Returns:
            The public URL, or None if it could not be retrieved
        """
        try:
            # Check if the ngrok API is available
            response = httpx.get(f"{self.api_url}/tunnels", timeout=2.0)
            data = response.json()
            
            if "tunnels" not in data or not data["tunnels"]:
                # The API is available but no tunnels are set up yet
                logger.debug("Ngrok API available but no tunnels found yet")
                return None
                
            # Look for HTTPS URL
            for tunnel in data["tunnels"]:
                if tunnel["proto"] == "https":
                    return tunnel["public_url"]
                    
            # Fall back to HTTP URL
            return data["tunnels"][0]["public_url"]
            
        except httpx.ConnectError:
            # This is expected during startup - the API isn't available yet
            logger.debug("Ngrok API not yet available, waiting...")
            return None
        except httpx.TimeoutError:
            # Timeout trying to connect to the API
            logger.debug("Timeout connecting to ngrok API, retrying...")
            return None
        except Exception as e:
            # Other unexpected errors
            logger.debug(f"Error accessing ngrok API: {str(e)}")
            return None
            
    def stop(self) -> None:
        """Stop the ngrok tunnel."""
        if self.process is not None:
            logger.info("Stopping ngrok tunnel")
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except Exception as e:
                logger.error(f"Error stopping ngrok: {e}")
                try:
                    self.process.kill()
                except Exception:
                    pass
            finally:
                self.process = None
                self.public_url = None
                
                # Unregister the cleanup function
                try:
                    atexit.unregister(self.stop)
                except Exception:
                    pass


def start_ngrok(port: int = 8000) -> Optional[str]:
    """Start an ngrok tunnel to the given port.
    
    Args:
        port: The port to tunnel to
        
    Returns:
        The public URL of the tunnel, or None if it failed
    """
    tunnel = NgrokTunnel(port=port)
    return tunnel.start()


# Singleton tunnel instance for application use
_tunnel_instance = None


def setup_ngrok_for_server(
    port: int = 8000,
    region: str = "us",
    auth_token: Optional[str] = None,
    executable: str = "ngrok",
    retries: int = 3,
    retry_delay: int = 1,
    show_url: bool = True,
) -> Optional[str]:
    """Set up ngrok for a server and return the public URL.
    
    This is a convenience function that can be used to set up ngrok when starting a server.
    It creates a singleton tunnel instance that can be reused.
    
    Args:
        port: The port the server is running on
        region: The ngrok region to use
        auth_token: The ngrok auth token (can also be set via NGROK_AUTH_TOKEN env var)
        executable: The ngrok executable path or command name
        retries: Number of times to retry starting ngrok
        retry_delay: Delay between retries in seconds
        show_url: Whether to log the public URL to the console
        
    Returns:
        The public URL of the tunnel, or None if it failed
    """
    global _tunnel_instance
    
    if show_url:
        print("\n🚀 Starting ngrok tunnel... This may take a few seconds.")
    
    if _tunnel_instance is None:
        _tunnel_instance = NgrokTunnel(
            port=port,
            region=region,
            auth_token=auth_token,
            executable=executable
        )
    
    # Start the tunnel
    url = _tunnel_instance.start(retries=retries, retry_delay=retry_delay)
    
    if url and show_url:
        print("\n✨ Ngrok tunnel established!")
        print(f"🌎 Public URL: {url}")
        print("⚠️  Note: This URL will change on restart unless you have a paid ngrok account")
        print(f"📒 Local API docs: http://localhost:{port}/docs")
        print(f"📒 Public API docs: {url}/docs\n")
    elif not url and show_url:
        print("\n❌ Failed to establish ngrok tunnel. Server will only be available locally.")
        print(f"📒 Local API docs: http://localhost:{port}/docs\n")
    
    return url


def get_current_tunnel() -> Optional[NgrokTunnel]:
    """Get the current tunnel instance if one exists.
    
    Returns:
        The current tunnel instance, or None if no tunnel is running
    """
    global _tunnel_instance
    return _tunnel_instance 