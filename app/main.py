from fastmcp import FastMCP

from app.config.server import Server


def app() -> FastMCP:
    mcp = FastMCP("MCP Server")
    return Server(mcp).get_app()


mcp = app()


if __name__ == "__main__":
    mcp.run()
