"""Template MCP Server implementation."""

from typing import List, Dict, Optional, Any, AsyncIterator
import logging
import os
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field
import anyio
import click
from mcp.server.fastmcp import FastMCP, Context

# Configure logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define configuration models
class ServiceConfig(BaseModel):
    """Example service configuration"""
    api_key: str = Field(..., description="API key for the service")
    endpoint: str = Field(default="https://api.example.com", description="Service endpoint")
    timeout: int = Field(default=30, description="Request timeout in seconds")

# Initialize global service instances
service_client = None

@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[None]:
    """Server lifespan handler."""
    global service_client
    
    logger.info("Starting Template MCP Server...")
    try:
        # Load configuration
        service_config = ServiceConfig(
            api_key=os.getenv("SERVICE_API_KEY")
        )
        if not service_config.api_key:
            raise ValueError("SERVICE_API_KEY environment variable must be set")
            
        # Initialize your service client here
        # service_client = YourServiceClient(service_config)
        logger.info("Service client initialized successfully")
        
        yield
    finally:
        # Cleanup resources
        if service_client:
            # Add cleanup code here
            logger.info("Service client cleaned up")

# Create FastMCP server instance with lifespan
mcp = FastMCP(
    name="Template MCP Server",
    instructions="A template server for building MCP services",
    lifespan=server_lifespan
)

def check_service_initialized():
    """Check if service client is initialized."""
    if not service_client:
        raise RuntimeError("Service client not initialized")

@mcp.tool()
async def test_connection(ctx: Context) -> Dict[str, Any]:
    """Test the service connection using configured credentials."""
    try:
        check_service_initialized()
        # Add your connection test here
        # result = await service_client.test_connection()
        
        return {
            "status": "success",
            "message": "Successfully connected to service"
        }
    except Exception as e:
        error_msg = str(e)
        await ctx.error(f"Connection error: {error_msg}")
        return {
            "status": "error",
            "message": f"Connection error: {error_msg}"
        }

@mcp.tool()
async def example_operation(
    input_text: str = Field(..., description="Text input to process"),
    optional_param: str = Field(default="", description="Optional processing parameter")
) -> Dict[str, Any]:
    """Example operation demonstrating tool implementation pattern.
    
    Args:
        input_text: Text input to process
        optional_param: Optional parameter for processing
    """
    try:
        check_service_initialized()
        
        logger.info(f"Processing input: {input_text}")
        # Add your operation implementation here
        # result = await service_client.process(input_text, optional_param)
        
        return {
            "status": "success",
            "result": f"Processed: {input_text}",
            "metadata": {
                "timestamp": "2025-04-25T10:00:00Z",
                "params_used": {
                    "optional_param": optional_param or None
                }
            }
        }
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Operation failed: {error_msg}")
        return {
            "status": "error",
            "message": f"Operation failed: {error_msg}"
        }

if __name__ == "__main__":
    try:
        # Run the server with stdio transport by default
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise