from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier

from config.server import Server
from config.settings import SETTINGS


def app() -> FastMCP:
    auth = None
    if SETTINGS.auth_mode == "jwt":
        assert SETTINGS.jwt_secret_key is not None
        auth = JWTVerifier(
            public_key=SETTINGS.jwt_secret_key.get_secret_value(),
            algorithm="HS256",
            issuer=SETTINGS.jwt_issuer,
            audience=SETTINGS.jwt_audience,
        )

    mcp = FastMCP(
        name=SETTINGS.project_name,
        instructions=f"{SETTINGS.project_name} MCP tools. Start by listing the available tools.",
        auth=auth,
        mask_error_details=True,
    )
    return Server(mcp).get_app()


mcp = app()


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host=SETTINGS.host,
        port=SETTINGS.port,
        stateless_http=True,
    )
