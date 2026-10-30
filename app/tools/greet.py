from fastmcp import FastMCP


mcp = FastMCP("Greeting", mask_error_details=True)


@mcp.tool
def greet(name: str) -> str:
    """Return a greeting for the given name."""
    return f"Salom, {name}!"
