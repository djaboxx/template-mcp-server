FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Create non-root user for security
RUN useradd -m mcp && \
    chown -R mcp:mcp /app
USER mcp

# Run MCP server
CMD ["python", "src/server.py"]

# Uncomment and modify if using HTTP transport instead of stdio
#EXPOSE 3000
#ENV MCP_PORT=3000
#ENV MCP_HOST=0.0.0.0