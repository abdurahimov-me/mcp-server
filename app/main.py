from fastmcp import FastMCP

from config.server import Server


def app() -> FastMCP:
    mcp = FastMCP(
        name="Breeze"
    )
    return Server(mcp).get_app()


mcp = app()


if __name__ == "__main__":
    mcp.run_http_async()
