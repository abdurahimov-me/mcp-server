from fastmcp import FastMCP

from app.tools import __tools__


class Server:
    def __init__(self, app: FastMCP) -> None:
        self.__app = app
        self.__mount_tools(app)

    def get_app(self) -> FastMCP:
        return self.__app

    @staticmethod
    def __mount_tools(app: FastMCP) -> None:
        __tools__.mount_tools(app)
