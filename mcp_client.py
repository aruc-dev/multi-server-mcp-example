import asyncio
import shlex
import os
import pathlib
from mcp import StdioServerParameters
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import tools_condition, ToolNode
from typing import Annotated, List
from typing_extensions import TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

# Import the MultiServerMCPClient
from langchain_mcp_adapters.client import MultiServerMCPClient

# Load environment variables
load_dotenv()

# --- Multi-server configuration dictionary ---
# This dictionary defines all the servers the client will connect to
server_configs = {
    "weather": {
        "command": "/opt/homebrew/bin/python3.11",
        "args": ["weather_mcp_server.py"],  # The weather server
        "transport": "stdio",
    },
    "tasks": {
        "command": "/opt/homebrew/bin/python3.11", 
        "args": ["tasklist_mcp_server.py"], # The task management server
        "transport": "stdio",
    }
}

# LangGraph state definition
class State(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]


# --- 'create_graph' now accepts the list of tools directly ---
def create_graph(tools: list):
    # LLM configuration with environment variable support
    google_api_key = os.getenv("GOOGLE_GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_GEMINI_API_KEY environment variable is not set. Please set your API key in .env file.")
    
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=google_api_key)
    llm_with_tools = llm.bind_tools(tools)

    # --- Enhanced system prompt to reflect comprehensive capabilities ---
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant with access to comprehensive tools for weather information and task management. 

Weather capabilities:
- Get detailed weather information for any location including current conditions, forecasts, and alerts
- Compare weather between multiple locations
- Access weather-related resources and prompts

Task management capabilities:
- Add tasks to a persistent task list
- List and manage existing tasks
- Access meeting notes and other organizational resources

Use the tools when necessary based on the user's request. Provide clear, helpful responses and feel free to suggest related actions when appropriate."""),
        MessagesPlaceholder("messages")
    ])

    chat_llm = prompt_template | llm_with_tools

    # Define chat node 
    def chat_node(state: State) -> State:
        response = chat_llm.invoke({"messages": state["messages"]})
        return {"messages": [response]}

    # Build LangGraph with tool routing 
    graph = StateGraph(State)
    graph.add_node("chat_node", chat_node)
    graph.add_node("tool_node", ToolNode(tools=tools))
    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges("chat_node", tools_condition, {
        "tools": "tool_node",
        "__end__": END
    })
    graph.add_edge("tool_node", "chat_node")

    return graph.compile(checkpointer=MemorySaver())

# Iterates through all configured servers, lists their available resources,
# and prints them in a user-friendly format
async def list_all_resources(client: MultiServerMCPClient, server_configs: dict):
    print("\nAvailable Resources from all servers:")
    print("-------------------------------------")
    
    any_resources_found = False
    
    # Iterate through the names of the servers defined in your server_configs
    for server_name in server_configs.keys():
        try:
            # Opening a session for a specific server to list its resources
            async with client.session(server_name) as session:
                # The method to list resources is session.list_resources()
                resource_response = await session.list_resources()

                if resource_response and resource_response.resources:
                    any_resources_found = True
                    print(f"\n--- Server: '{server_name}' ---")
                    for r in resource_response.resources:
                        # The most important identifier for a resource is its URI
                        print(f"  Resource URI: {r.uri}")
                        if r.description:
                            print(f"    Description: {r.description}")
        except Exception as e:
            print(f"\nCould not fetch resources from server '{server_name}': {e}")
    
    print("\nUse: /resource <server_name> <resource_uri>")
    print("-----------------------------------")          
    
    if not any_resources_found:
        print("\nNo resources were found on any connected servers.")

# Parses a user command to fetch a specific resource from a server and
# returns its content as a string with enhanced text extraction
async def handle_resource_invocation(client: MultiServerMCPClient, command: str) -> str | None:
    try:
        parts = command.strip().split()
        if len(parts) != 3:
            print("\nUsage: /resource <server_name> <resource_uri>")
            return None

        server_name = parts[1]
        resource_uri = parts[2]

        print(f"\n--- Fetching resource '{resource_uri}' from server '{server_name}'... ---")

        # Get resources using the client
        blobs = await client.get_resources(server_name=server_name, uris=[resource_uri])

        if not blobs:
            print("Error: Resource not found or content is empty.")
            return None

        # Enhanced text extraction from LangChain Blobs
        # Handle different content types and formats
        resource_content = blobs[0].as_string()
        
        # If the content is a list of lines (common for text resources), join them
        if isinstance(resource_content, list):
            resource_content = "\n".join(str(line) for line in resource_content)
        elif not isinstance(resource_content, str):
            resource_content = str(resource_content)
        
        if not resource_content.strip():
            print("Error: Resource content is empty or not in a readable text format.")
            return None
        
        print("--- Resource content loaded successfully. ---")
        return resource_content

    except Exception as e:
        print(f"\nAn error occurred while fetching the resource: {e}")
        return None


# Fetches the list of available prompts from all connected servers
# and prints them in a user-friendly format
async def list_all_prompts(client: MultiServerMCPClient, server_configs: dict):
    print("\nAvailable Prompts from all servers:")
    print("-----------------------------------")
    
    any_prompts_found = False
    
    # Iterate through the names of the servers defined in your server_configs
    for server_name in server_configs.keys():
        try:
            # Opening a session for a specific server to list its prompts
            async with client.session(server_name) as session:
                prompt_response = await session.list_prompts()

                if prompt_response and prompt_response.prompts:
                    any_prompts_found = True
                    print(f"\n--- Server: '{server_name}' ---")
                    for p in prompt_response.prompts:
                        print(f"  Prompt: {p.name}")
                        if p.arguments:
                            arg_list = [f"<{arg.name}>" for arg in p.arguments]
                            print(f"    Arguments: {' '.join(arg_list)}")
                        else:
                            print("    Arguments: None")
                        if hasattr(p, 'description') and p.description:
                            print(f"    Description: {p.description}")
        except Exception as e:
            print(f"\nCould not fetch prompts from server '{server_name}': {e}")
    
    print("\nUsage: /prompt <server_name> <prompt_name> \"arg1\" \"arg2\" ...")
    print("-----------------------------------")
    
    if not any_prompts_found:
        print("\nNo prompts were found on any connected servers.")


# Parses a user command to invoke a specific prompt from a server,
# then returns the generated prompt text
async def handle_prompt_invocation(client: MultiServerMCPClient, command: str) -> str | None:
    try:
        parts = shlex.split(command.strip())
        if len(parts) < 3:
            print("\nUsage: /prompt <server_name> <prompt_name> \"arg1\" \"arg2\" ...")
            return None

        server_name = parts[1]
        prompt_name = parts[2]
        user_args = parts[3:]

        print(f"\n--- Invoking prompt '{prompt_name}' from server '{server_name}'... ---")

        # Opening a session for the specific server
        async with client.session(server_name) as session:
            # Get available prompts from the server to validate
            prompt_def_response = await session.list_prompts()
            if not prompt_def_response or not prompt_def_response.prompts:
                print(f"\nError: Could not retrieve any prompts from server '{server_name}'.")
                return None
            
            # Find the specific prompt definition
            prompt_def = next((p for p in prompt_def_response.prompts if p.name == prompt_name), None)

            if not prompt_def:
                print(f"\nError: Prompt '{prompt_name}' not found on server '{server_name}'.")
                return None

            # Check if the number of user-provided arguments matches what the prompt expects
            if len(user_args) != len(prompt_def.arguments):
                expected_args = [arg.name for arg in prompt_def.arguments]
                print(f"\nError: Invalid number of arguments for prompt '{prompt_name}'.")
                print(f"Expected {len(expected_args)} arguments: {', '.join(expected_args)}")
                return None
            
            # Build the argument dictionary
            arg_dict = {arg.name: val for arg, val in zip(prompt_def.arguments, user_args)}

            # Fetch the prompt from the server using the validated name and arguments
            prompt_response = await session.get_prompt(prompt_name, arg_dict)
            
            # Extract the text content from the response
            prompt_text = prompt_response.messages[0].content.text

            print("\n--- Prompt loaded successfully. Preparing to execute... ---")
            return prompt_text

    except Exception as e:
        print(f"\nAn error occurred during prompt invocation: {e}")
        return None


# --- Main function ---
async def main():

    # The client will manage the server subprocesses internally
    client = MultiServerMCPClient(server_configs)
    
    # Get a single, unified list of tools from all connected servers
    all_tools = await client.get_tools()

    # Create the LangGraph agent with the aggregated list of tools
    agent = create_graph(all_tools)
    
    print("Enhanced MCP Agent is ready (connected to Weather and Task servers).")
    print("Type a question, or use one of the following commands:")
    print("  /prompts                                        - to list available prompts from all servers")
    print("  /prompt <server_name> <prompt_name> \"args\"...  - to run a specific prompt from a server")
    print("  /resources                                      - to list available resources from all servers")
    print("  /resource <server_name> <resource_uri>          - to load a resource for the agent")
    print("  Type 'exit', 'quit', or 'q' to quit")
    
    message_to_agent = ""
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
            
        if user_input.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break

        # --- Enhanced Command Handling Logic ---
        if user_input.lower() == "/prompts":
            await list_all_prompts(client, server_configs)
            continue # Command is done, loop back for next input

        elif user_input.startswith("/prompt"):
            # Handle prompt invocation from any server
            prompt_text = await handle_prompt_invocation(client, user_input)
            if prompt_text:
                message_to_agent = prompt_text
            else:
                # If prompt fetching failed, loop back for next input
                continue
                
        elif user_input.lower() == "/resources":
            await list_all_resources(client, server_configs)
            continue # Command is done, loop back for next input

        elif user_input.startswith("/resource"):
            resource_content = await handle_resource_invocation(client, user_input)

            if resource_content:
                action_prompt = input("Resource loaded. What should I do with this content? (Press Enter to just save to context)\n> ").strip()
                
                # If user provides an action, combine it with the resource content
                if action_prompt:
                    message_to_agent = f"""
                    CONTEXT from a loaded resource:
                    ---
                    {resource_content}
                    ---
                    TASK: {action_prompt}
                    """
              
                # If user provides no action, create a default message to save the context
                else:
                    print("No action specified. Adding resource content to conversation memory...")
                    message_to_agent = f"""
                    Please remember the following context for our conversation. Just acknowledge that you have received it.
                    ---
                    CONTEXT:
                    {resource_content}
                    ---
                    """
            else:
                # If resource loading failed, loop back for next input
                continue
        
        else:
            # For a normal chat message, the message is just the user's input
            message_to_agent = user_input

        # Final agent invocation with enhanced error handling
        if message_to_agent:
            try:
                response = await agent.ainvoke(
                    {"messages": [("user", message_to_agent)]},
                    config={"configurable": {"thread_id": "enhanced-multi-server-session"}}
                )
                print("AI:", response["messages"][-1].content)
            except Exception as e:
                print(f"Error invoking agent: {e}")
                print("Please try again or check your input.")


if __name__ == "__main__":
    asyncio.run(main())