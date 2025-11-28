# Contributing to Enhanced Multi-Server MCP Example

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the Enhanced Multi-Server MCP Example.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Code Standards](#code-standards)
- [Submitting Changes](#submitting-changes)
- [Adding New Servers](#adding-new-servers)
- [Testing](#testing)
- [Documentation](#documentation)

## Getting Started

### Prerequisites

- Python 3.10 or higher (Python 3.11+ recommended)
- Git for version control
- API keys for external services (OpenWeatherMap, Google Gemini)

### Development Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd multi-server-mcp-example
   ```

2. **Set up virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Test the setup**:
   ```bash
   python test_servers.py
   python mcp_client.py
   ```

## Contributing Guidelines

### Types of Contributions

We welcome several types of contributions:

- **Bug fixes**: Fix existing issues or unexpected behavior
- **Feature enhancements**: Improve existing functionality
- **New servers**: Add support for new MCP servers
- **Documentation**: Improve or add documentation
- **Examples**: Add usage examples or tutorials
- **Testing**: Improve test coverage or add new tests

### Before You Start

1. **Check existing issues**: Look for existing issues or feature requests
2. **Create an issue**: If none exists, create one to discuss your proposed changes
3. **Fork the repository**: Create your own fork to work on changes
4. **Create a feature branch**: Use a descriptive branch name

## Code Standards

### Python Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add type hints where appropriate
- Include docstrings for functions and classes
- Keep functions focused and modular

### Example Code Structure

```python
def add_new_server_config(server_name: str, config: dict) -> bool:
    """
    Add a new server configuration to the client.
    
    Args:
        server_name: Unique name for the server
        config: Server configuration dictionary with command, args, and transport
        
    Returns:
        True if server was added successfully, False otherwise
        
    Raises:
        ValueError: If server_name already exists or config is invalid
    """
    # Implementation here
    pass
```

### MCP Server Standards

When creating new MCP servers:

1. **Use FastMCP framework** for consistency
2. **Include proper error handling** for all external API calls
3. **Add comprehensive docstrings** for tools, prompts, and resources
4. **Follow naming conventions**: Use descriptive names for tools and resources
5. **Include resource documentation**: Provide clear descriptions for all resources

### Example Server Structure

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("YourServerName")

@mcp.tool()
def your_tool_function(param: str) -> dict:
    """
    Clear description of what the tool does.
    
    Args:
        param: Description of the parameter
        
    Returns:
        Dictionary containing the result or error information
    """
    # Implementation
    pass

@mcp.resource("file://your_resource")
def your_resource() -> list[str]:
    """
    Description of what this resource provides.
    """
    # Implementation
    pass
```

## Submitting Changes

### Pull Request Process

1. **Update documentation**: Ensure README and other docs reflect your changes
2. **Add/update tests**: Include tests for new functionality
3. **Update CHANGELOG.md**: Add entry describing your changes
4. **Test thoroughly**: Ensure all existing functionality still works
5. **Create pull request**: Use a clear title and description

### Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (specify)

## Testing
- [ ] Tested locally with test_servers.py
- [ ] Tested full client functionality
- [ ] Added/updated relevant tests
- [ ] All existing tests pass

## Documentation
- [ ] Updated README if needed
- [ ] Updated CHANGELOG.md
- [ ] Added inline code comments
- [ ] Updated docstrings

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] No breaking changes (or clearly documented)
- [ ] API keys and secrets not included in code
```

## Adding New Servers

### Server Integration Checklist

1. **Create server file**: Following naming convention `{purpose}_mcp_server.py`
2. **Add server config**: Update `server_configs` in `mcp_client.py`
3. **Test server independently**: Ensure server starts and responds properly
4. **Update documentation**: Add server description to README
5. **Add example usage**: Include examples of server capabilities
6. **Test integration**: Verify server works with the multi-server client

### Server Configuration

Add your server to the `server_configs` dictionary:

```python
server_configs = {
    # Existing servers...
    "your_server": {
        "command": "/path/to/python",
        "args": ["your_server_mcp_server.py"],
        "transport": "stdio",
    }
}
```

## Testing

### Running Tests

```bash
# Test individual servers
python test_servers.py

# Test full client
python mcp_client.py

# Manual testing commands
/prompts
/resources
/prompt weather compare_weather_prompt "City1" "City2"
/resource tasks file://meeting_notes
```

### Adding Tests

When adding new functionality:

1. **Unit tests**: Test individual functions
2. **Integration tests**: Test server communication
3. **End-to-end tests**: Test full user workflows
4. **Error handling tests**: Test failure scenarios

## Documentation

### Documentation Standards

- **Clear and concise**: Write for users of all experience levels
- **Examples included**: Provide concrete usage examples
- **Up to date**: Ensure docs match current functionality
- **Well organized**: Use clear headings and structure

### Required Documentation Updates

For new features:
- Update README.md with new capabilities
- Add entries to CHANGELOG.md
- Include usage examples
- Update command reference if applicable

## Getting Help

- **Create an issue**: For questions or problems
- **Check documentation**: README and code comments
- **Review examples**: Look at existing server implementations

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and contribute
- Maintain professional communication

Thank you for contributing to the Enhanced Multi-Server MCP Example!