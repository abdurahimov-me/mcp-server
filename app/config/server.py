from pathlib import Path

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

from tools import __tools__


DOCS_HTML = (Path(__file__).with_name("docs.html")).read_text(encoding="utf-8")


class Server:
    def __init__(self, app: FastMCP) -> None:
        self.__app = app
        self.__mount_tools(app)
        self.__register_routes(app)

    def get_app(self) -> FastMCP:
        return self.__app

    @staticmethod
    def __mount_tools(app: FastMCP) -> None:
        __tools__.mount_tools(app)

    @staticmethod
    def __register_routes(app: FastMCP) -> None:
        @app.custom_route("/health", methods=["GET"])
        async def health(_request: Request) -> JSONResponse:
            return JSONResponse({"status": "ok"})

        @app.custom_route("/docs", methods=["GET"])
        async def docs(_request: Request) -> HTMLResponse:
            return HTMLResponse(DOCS_HTML)
