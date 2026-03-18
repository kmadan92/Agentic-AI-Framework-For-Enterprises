from mcp.server.fastmcp import FastMCP

# Initialize your MCP Server
mcp = FastMCP("LLM App")

@mcp.tool()
async def run_node_test(node_id: [str], test_type: str) -> str:
    """
    Executes a probation test on a server node for given NodeId or NodeIds and Test Type.
    
    CRITICAL INSTRUCTIONS FOR AI:
    You MUST have both node_id' or  list of node ids and a 'test_type' (e.g., CPU, Memory, Network) to call this tool.
    
    If you are missing any of these details, DO NOT CALL THIS TOOL. Instead, you must collect the missing information EXACTLY ONE QUESTION AT A TIME:
    1. First, check if you have the 'node_id'. If you do not, ask the user ONLY for the Node ID or list of Node IDs and stop. Wait for their reply.
    2. Once you have the 'node_id', check if you have the 'test_type'. If you do not, ask the user ONLY for the test type and stop. Wait for their reply.
    3. NEVER ask for both the Node ID and the Test Type in the same message.
    """
    
    return "Tests failed"

# Run the MCP server
if __name__ == "__main__":
    mcp.run()