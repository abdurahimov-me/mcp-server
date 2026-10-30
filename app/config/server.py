from contextlib import asynccontextmanager

from fastmcp import FastMCP
from fastmcp.server.auth import AuthProvider
from fastmcp.server.auth.providers.jwt import JWTVerifier

from config.docs import register_docs
from config.settings import Settings
from tools import __tools__


class Server:
    def __init__(self, settings: Settings) -> None:
        app = FastMCP(
            name=settings.project_name,
            instructions=f"{settings.project_name} MCP tools. Start by listing the available tools.",
            auth=self.__apply_auth(settings),
            mask_error_details=True,
            lifespan=self.lifespan,
        )
        self.__app = app
        self.__mount_tools(app)
        self.__register_docs(app)

    def get_app(self) -> FastMCP:
        return self.__app

    @staticmethod
    def __apply_auth(settings: Settings) -> AuthProvider | None:
        if settings.auth_mode != "jwt":
            return None

        assert settings.jwt_secret_key is not None
        return JWTVerifier(
            public_key=settings.jwt_secret_key.get_secret_value(),
            algorithm="HS256",
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
        )

    @staticmethod
    def __mount_tools(app: FastMCP) -> None:
        __tools__.mount_tools(app)

    @staticmethod
    def __register_docs(app: FastMCP) -> None:
        register_docs(app)

    @staticmethod
    @asynccontextmanager
    async def lifespan(app: FastMCP):
        from .events import on_startup, on_shutdown
        await on_startup(app)
        yield
        await on_shutdown(app)
