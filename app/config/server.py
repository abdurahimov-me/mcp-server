from contextlib import asynccontextmanager

from fastmcp import FastMCP

from config.docs import register_docs
from tools import __tools__


class Server:
    def __init__(self, app: FastMCP) -> None:
        self.__app = app
        self.__mount_tools(app)

    def get_app(self) -> FastMCP:
        return self.__app

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
