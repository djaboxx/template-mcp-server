# Python MCP Server Template

A template repository for creating VS Code Model Context Protocol (MCP) servers using Python. This template follows patterns and best practices established by production MCP servers.

## Purpose

This template provides a foundation for building MCP servers that:
- Integrate with VS Code's AI features
- Follow established patterns from production MCP servers
- Handle configuration, logging, and error cases consistently
- Use best practices for async Python and MCP tools

## Architecture

The template follows these key architectural patterns seen in production MCP servers:

1. **Service Configuration**
   - Pydantic models for configuration validation
   - Environment variable based configuration
   - Service client initialization in server lifespan

2. **Server Lifecycle**
   - Async context manager for server lifespan
   - Clean startup/shutdown handling
   - Resource cleanup in finally blocks

3. **Tool Implementation**
   - Decorator-based tool registration
   - Consistent error handling and logging
   - Structured response formats

4. **Development Patterns**
   - Type hints throughout
   - Detailed logging with configurable levels
   - Service state validation checks

## Project Structure

Standard MCP server structure based on production patterns:

```
.
├── src/                     # Python source code
│   ├── server.py           # Main MCP server implementation
│   ├── services/           # Service client implementations
│   │   └── client.py       # Your service client code
│   ├── models.py           # Data models and schemas
│   ├── config.py           # Configuration models
│   └── utils/              # Utility functions
├── docs/                   # Documentation
│   └── mcp-server-guide.md # Server implementation guide
├── tests/                  # Test files
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## Code Organization

The template follows these conventions from production MCP servers:

1. **Server Entry Point** (`src/server.py`):
   ```python
   # Configuration models
   class ServiceConfig(BaseModel):
       api_key: str
       # ...

   # Server lifespan
   @asynccontextmanager
   async def server_lifespan(server: FastMCP):
       try:
           # Initialize services
           yield
       finally:
           # Cleanup

   # FastMCP instance
   mcp = FastMCP(
       name="Your Server",
       instructions="Your server description",
       lifespan=server_lifespan
   )

   # Tools
   @mcp.tool()
   async def your_tool(ctx: Context):
       # Tool implementation
   ```

2. **Service Clients** (`src/services/`):
   - Implement service-specific clients
   - Handle authentication and retries
   - Manage connection state

3. **Models** (`src/models.py`):
   - Define Pydantic models for data validation
   - Structure tool inputs and outputs
   - Define service-specific types

## Implementation Guide

1. **Configuration**:
   - Add config models to match your service needs
   - Use environment variables for secrets
   - Add validation for required fields

2. **Service Client**:
   - Implement your service client in `services/`
   - Add connection/retry handling
   - Include proper cleanup

3. **Tools**:
   - Use the `@mcp.tool()` decorator
   - Include type hints and docstrings
   - Follow the error handling pattern:
   ```python
   @mcp.tool()
   async def your_tool(ctx: Context) -> Dict[str, Any]:
       try:
           # Implementation
           return {"status": "success", "result": result}
       except Exception as e:
           await ctx.error(f"Error: {e}")
           return {"status": "error", "message": str(e)}
   ```

4. **Error Handling**:
   - Use structured error responses
   - Log errors with context
   - Return user-friendly messages

## Getting Started

1. Create your new repository from this template:
   ```zsh
   git clone https://github.com/username/template-mcp-server.git your-server
   cd your-server
   ```

2. Set up development environment:
   ```zsh
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Update server name and description in `src/server.py`

4. Add your service configuration and client

## VS Code Configuration

To use this server with VS Code's MCP functionality, add the following configuration to your VS Code `settings.json`:

```json
"mcp": {
  "inputs": [
    {
      "type": "promptString",
      "id": "service-api-key",
      "description": "Service API Key",
      "password": true
    }
  ],
  "servers": {
    "template-mcp": {
      "type": "stdio",
      "command": "${userHome}/git/template-mcp-server/venv/bin/python",
      "args": [
        "${userHome}/git/template-mcp-server/src/server.py"
      ],
      "env": {
        "SERVICE_API_KEY": "${input:service-api-key}",
        "SERVICE_ENDPOINT": "https://api.example.com",
        "SERVICE_TIMEOUT": "30",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Configuration Options

- **Environment Variables**:
  - `SERVICE_API_KEY`: Your service API key (required)
  - `SERVICE_ENDPOINT`: Service endpoint URL (default: https://api.example.com)
  - `SERVICE_TIMEOUT`: Request timeout in seconds (default: 30)
  - `LOG_LEVEL`: Logging level (default: INFO)

## Testing

Following the patterns from production MCP servers:

1. **Manual Testing**:
   ```zsh
   # Run the server directly
   python src/server.py

   # Test with different log levels
   LOG_LEVEL=DEBUG python src/server.py
   ```

2. **Integration Testing**:
   ```zsh
   # Start server with test configuration
   SERVICE_API_KEY=test-key python src/server.py
   ```

3. **Development Tips**:
   - Use VS Code's Python debugger to step through tool execution
   - Set breakpoints in your service client to debug integration issues
   - Use DEBUG log level during development for detailed output

## Common Patterns

From analyzing production MCP servers, here are key patterns to follow:

1. **Service Client State**:
   - Initialize in server lifespan
   - Store in global variable
   - Check initialization before use
   - Clean up in finally block

2. **Error Handling**:
   - Log errors with context
   - Return structured error responses
   - Use ctx.error() for user feedback
   - Include both status and message

3. **Configuration**:
   - Use Pydantic models
   - Set sensible defaults
   - Validate at startup
   - Support environment overrides

4. **Tool Implementation**:
   - Clear docstrings with Args section
   - Type hints for all parameters
   - Structured responses
   - Consistent error format

## Resources

- [MCP Server Guide](docs/mcp-server-guide.md)
- [Python SDK Documentation](https://github.com/username/python-sdk)
- [VS Code MCP Documentation](https://code.visualstudio.com/docs/mcp)

## VS Code Configuration

To use this server with VS Code's MCP (Model Context Protocol) functionality, add the following configuration to your VS Code `settings.json`:

```json
"mcp": {
  "inputs": [
    {
      "type": "promptString",
      "id": "service-api-key",
      "description": "Service API Key",
      "password": true
    }
  ],
  "servers": {
    "template-mcp": {
      "type": "stdio",
      "command": "${userHome}/git/template-mcp-server/venv/bin/python",
      "args": [
        "${userHome}/git/template-mcp-server/src/server.py"
      ],
      "env": {
        "SERVICE_API_KEY": "${input:service-api-key}",
        "SERVICE_ENDPOINT": "https://api.example.com",
        "SERVICE_TIMEOUT": "30",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Configuration Options

- **Environment Variables**:
  - `SERVICE_API_KEY`: Your service API key (required)
  - `SERVICE_ENDPOINT`: Service endpoint URL (default: https://api.example.com)
  - `SERVICE_TIMEOUT`: Request timeout in seconds (default: 30)
  - `LOG_LEVEL`: Logging level (default: INFO)

### Prerequisites

Before using the server:

1. Set up a Python virtual environment in the project directory:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

2. Configure VS Code:
   - Create .vscode/mcp.json with stdio configuration
   - Set up Python interpreter in VS Code
   - Use the integrated terminal for running commands
   - Debug your MCP server using VS Code's Python debugger

3. Test your MCP server:
   - Use VS Code's built-in MCP server testing capabilities
   - Debug with breakpoints and VS Code's debug console
   - Monitor stdio communication in the output panel

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

[Your chosen license]