# Creating VS Code MCP Servers

## Overview

This guide details how to create a Model Context Protocol (MCP) server that integrates with Visual Studio Code. This template repository provides a foundation for building MCP servers that can be used by VS Code to extend AI capabilities through custom tools and services.

MCP follows a client-server architecture where:
- MCP clients (like VS Code) connect to MCP servers and request actions on behalf of the AI model
- MCP servers provide one or more tools that expose specific functionalities through a well-defined interface
- The Model Context Protocol defines the message format for communication between clients and servers

## Prerequisites

1. Python 3.8 or higher
2. Visual Studio Code
3. Basic understanding of the VS Code extension model
4. VS Code MCP extension (required for testing)

## Setting Up Your Development Environment

### 1. Getting Started with the Template

1. Create a new repository using this template:
   - Click "Use this template" on GitHub
   - Or clone and reinitialize:
   ```bash
   git clone https://github.com/your-org/mcp-server-template
   cd mcp-server-template
   ```

2. Set up your Python environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

3. Install the VS Code MCP extension (if not already installed)

### 2. Configuration Options

You can configure your MCP server in several ways:

1. Workspace Configuration (`.vscode/mcp.json`):
```json
{
  "servers": {
    "your-server-name": {
      "type": "stdio",
      "command": "python",
      "args": ["${workspaceFolder}/src/server.py"],
      "env": {
        "CUSTOM_ENV": "${input:custom_env_var}"
      }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "custom_env_var",
      "description": "Custom environment variable",
      "password": true
    }
  ]
}
```

2. User Settings:
   - Add server configuration to VS Code's user settings.json
   - Useful for personal configurations that shouldn't be committed to version control
   - Supports the same configuration format as workspace configuration

3. Command Line:
   ```bash
   code --add-mcp '{"name":"server-name","command":"python","args":["server.py"]}'
   ```

## Implementation Guide

### 1. Basic Server Structure

The server implementation in `src/server.py` follows this pattern:

```python
from mcp.server import Server, tool

class MCPServer(Server):
    def __init__(self):
        super().__init__()
        # Initialize any required clients or resources

    @tool("Example tool")
    def example_tool(self, input_param: str) -> str:
        """A simple example tool.
        
        Args:
            input_param: Description of the input parameter
            
        Returns:
            The result of the tool's operation
        """
        return f"Processed: {input_param}"
```

### 2. Implementing Tools

Tools are the primary way your MCP server extends VS Code's AI capabilities. Tools should be:

1. Focused and atomic
2. Well-documented with clear docstrings
3. Properly typed with type hints
4. Error-handled appropriately
5. Returning structured data when possible

Example tool patterns:

```python
class MyMCPServer(Server):
    @tool("Process file")
    async def process_file(self, file_path: str) -> dict:
        """Process a file and return results.
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            Dict containing processing results
        """
        try:
            # Implementation
            pass
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            raise ToolError(f"Failed to process file: {str(e)}")

    @tool("Search items")
    async def search_items(
        self, 
        query: str, 
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for items matching the query.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of matching items with their details
        """
        # Implementation
        pass
```

### 3. Error Handling and Logging

Implement comprehensive error handling:
- Input validation with clear error messages
- Resource access error handling
- External service failure management
- Timeout handling
- Proper error logging
- VS Code integration error handling

Use structured logging:
```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Add handlers as needed
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
```

## Security Best Practices

### 1. Credentials Management

- Never hardcode credentials in server code
- Use VS Code's input variables for sensitive data
- Support environment variables for configuration
- Use secure credential storage when possible

### 2. Input Validation

- Validate all tool inputs
- Sanitize file paths and URLs
- Implement proper access controls
- Follow the principle of least privilege

### 3. Error Messages

- Avoid exposing sensitive information in error messages
- Log detailed errors for debugging
- Return sanitized error messages to users

## Testing and Debugging

### 1. Local Testing

1. Use VS Code's built-in debugging:
   - Set breakpoints in your server code
   - Use the Debug Console
   - Monitor server output in Output panel

2. Tool Testing:
   - Test individual tools
   - Verify error handling
   - Check edge cases
   - Test concurrent operations

### 2. Integration Testing

1. VS Code Integration:
   - Test tool discovery
   - Verify input handling
   - Check error reporting
   - Test with different workspace configurations

2. AI Model Integration:
   - Test tool invocation patterns
   - Verify response handling
   - Check error recovery

## Deployment

### 1. Local Installation

Package your server for local installation:
- Create proper setup files
- Include dependencies
- Document installation steps

### 2. Distribution

If distributing your server:
- Package with pip/PyPI
- Provide clear installation instructions
- Include configuration examples
- Document requirements

## Docker Support

### 1. Docker Configuration

The template includes Docker support out of the box:

1. `Dockerfile`: Base configuration for running the MCP server
   - Uses Python 3.12 slim image for minimal size
   - Runs as non-root user for security
   - Configurable for both stdio and HTTP transport
   - Easy to extend for specific needs

2. `docker-compose.yml`: Development and deployment configuration
   - Volume mounts for live code updates
   - Environment variable support
   - Configurable port mapping
   - Easy credential mounting

3. `.dockerignore`: Optimized build context
   - Excludes development artifacts
   - Prevents sensitive files from being included
   - Reduces build time and image size

### 2. Using Docker

#### Local Development

```bash
# Build and start the server
docker compose up --build

# Run in detached mode
docker compose up -d

# View logs
docker compose logs -f
```

#### Production Deployment

1. Build optimized image:
   ```bash
   docker build -t your-mcp-server .
   ```

2. Run with specific configuration:
   ```bash
   docker run -e ENV_VAR_NAME=value your-mcp-server
   ```

### 3. Customizing for Your MCP Server

1. Environment Variables:
   - Add environment variables in docker-compose.yml
   - Use .env file for local development
   - Configure credentials mounting

2. Transport Configuration:
   - stdio (default): No additional configuration needed
   - HTTP: Uncomment EXPOSE and ENV settings in Dockerfile

3. Dependencies:
   - Add requirements to requirements.txt
   - They will be installed during build

4. Security:
   - Server runs as non-root user
   - Mount credentials as read-only
   - Use environment variables for sensitive data

## Contributing

1. Follow the code style guide
2. Add tests for new features
3. Update documentation
4. Submit pull requests

## Additional Resources

- [VS Code Extension API](https://code.visualstudio.com/api)
- [MCP Protocol Specification](https://github.com/microsoft/model-control-protocol)
- [Python MCP SDK Documentation](https://microsoft.github.io/model-control-protocol/python-sdk/)
- [Official VS Code MCP Documentation](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)