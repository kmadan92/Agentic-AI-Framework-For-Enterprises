from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("Fleet Health Server")

@mcp.tool()
def cpu_test() -> str:
    """
    Simulates a CPU test.
    """
    return "cpu-test successful"

@mcp.tool()
def memory_test() -> str:
    """
    Simulates a memory test.
    """
    return "memory test successful"

if __name__ == "__main__":
    # Run the server using standard input/output
    mcp.run()