# Enhanced Multi-Server MCP Example

This is an enhanced version of a multi-server MCP (Model Context Protocol) client that combines capabilities from both the WeatherAssistant and task management systems. The client connects to multiple MCP servers simultaneously and provides a unified interface for weather information, task management, and more.

## Features

### Weather Capabilities
- **Comprehensive Weather Data**: Current conditions, hourly forecasts (48h), daily forecasts (8 days), weather alerts
- **Location Support**: City names with optional country codes (e.g., "London,uk")
- **Weather Comparison**: Compare weather between multiple locations using prompts
- **Detailed Information**: UV index, visibility, wind speed, humidity, pressure, and more

### Task Management
- **Persistent Task Lists**: Add and manage tasks that persist across sessions
- **Task Operations**: Add new tasks, list existing tasks
- **Resource Access**: Access meeting notes and organizational resources

### Enhanced Client Features
- **Multi-Server Support**: Seamlessly connect to multiple MCP servers
- **Prompt System**: Access and execute prompts from any connected server
- **Resource Management**: Load and process resources from different servers
- **Smart Error Handling**: Comprehensive error handling with user-friendly messages
- **Environment Configuration**: Secure API key management through environment variables

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy the example environment file and configure your API keys:
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```
GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key_here
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here
```

### 3. Get API Keys

#### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

#### OpenWeatherMap API Key
1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Subscribe to "One Call by Call" for full weather features
3. Add your API key to the `.env` file

## Usage

### Starting the Client
```bash
python mcp_client.py
```

### Available Commands

#### Weather Commands
```
What's the weather in London?
Compare weather between New York and London
Get a 3-day forecast for Tokyo
```

#### Task Management Commands
```
Add task "Buy groceries"
List my tasks
Add task "Finish the report by Friday"
```

#### System Commands
```
/prompts                                        - List all available prompts
/prompt <server_name> <prompt_name> "args"...  - Execute a specific prompt
/resources                                      - List all available resources  
/resource <server_name> <resource_uri>          - Load a resource
exit/quit/q                                     - Quit the application
```

### Example Interactions

#### Weather Examples
```
You: What's the weather in Paris?
AI: The weather in Paris, France is currently...

You: /prompt weather compare_weather_prompt "London" "Tokyo"
AI: [Executes weather comparison prompt]

You: /resource weather file://delivery_log
Resource loaded. What should I do with this content? > Analyze delivery locations for weather patterns
```

#### Task Management Examples
```
You: Add a task to finish the quarterly report
AI: Task 'finish the quarterly report' was added successfully.

You: What are my current tasks?
AI: Here are your current tasks: [lists all tasks]

You: /resource tasks file://meeting_notes
Resource loaded. What should I do with this content? > Extract action items and add them as tasks
```

## Server Architecture

### Connected Servers
1. **Weather Server** (`weather_mcp_server.py`)
   - OpenWeatherMap One Call API 3.0 integration
   - Comprehensive weather data retrieval
   - Weather comparison prompts
   - Delivery log and index resources

2. **Task Server** (`tasklist_mcp_server.py`)
   - Persistent task storage in `tasks.txt`
   - Task addition and listing capabilities
   - Meeting notes resource access

### Server Configuration
The client automatically connects to both servers using the configuration in `server_configs`:
- **weather**: Handles weather-related operations
- **tasks**: Manages task-related operations

## Advanced Features

### Prompt System
Access server-specific prompts for enhanced functionality:
```
/prompts                                    # List all available prompts
/prompt weather compare_weather_prompt "NYC" "LA"  # Execute weather comparison
```

### Resource Management
Load and process various resources:
```
/resources                                  # List all resources
/resource weather file://delivery_log      # Load delivery log
/resource tasks file://meeting_notes       # Load meeting notes
```

### Context Management
The client maintains conversation context across interactions, allowing for follow-up questions and complex multi-step operations.

## Error Handling

The enhanced client includes comprehensive error handling for:
- Network connectivity issues
- API key authentication problems
- Invalid commands or parameters
- Server communication failures
- Resource access errors

## File Structure

```
multi-server-mcp-example/
├── mcp_client.py                  # Enhanced multi-server client
├── weather_mcp_server.py          # Weather MCP server
├── tasklist_mcp_server.py         # Task management MCP server
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variable template
├── .env                          # Your API keys (create from .env.example)
├── tasks.txt                     # Persistent task storage (auto-created)
└── README.md                     # This file
```

## Contributing

This enhanced version brings together the best features from:
- WeatherAssistant single-server implementation
- Task management capabilities
- Multi-server architecture
- Enhanced error handling and user experience

Feel free to extend this example by adding more servers or capabilities!

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
2. **API Key Issues**: Verify your API keys are correctly set in the `.env` file
3. **Server Connection**: Check that the server files are in the same directory as the client
4. **Weather API Subscription**: Ensure you have subscribed to "One Call by Call" for OpenWeatherMap

### Getting Help
If you encounter issues:
1. Check the error messages in the console
2. Verify your API keys and network connection
3. Ensure all dependencies are properly installed
4. Check the server logs for detailed error information