from fastmcp import FastMCP


mcp = FastMCP("Greeting")


@mcp.tool
def greet(name: str) -> str:
    """Return a greeting for the given name."""
    return f"Salom, {name}!"
