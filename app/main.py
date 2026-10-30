from fastmcp import FastMCP

from config.server import Server
from config.settings import SETTINGS


def app() -> FastMCP:
    return Server(SETTINGS).get_app()


mcp = app()
asgi_app = mcp.http_app(stateless_http=True)


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host=SETTINGS.host,
        port=SETTINGS.port,
        stateless_http=True,
    )
