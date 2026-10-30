from collections.abc import Iterable
from dataclasses import dataclass

from fastmcp import FastMCP


@dataclass(frozen=True)
class Tools:
    servers: Iterable[FastMCP]

    def mount_tools(self, app: FastMCP) -> None:
        for server in self.servers:
            app.mount(server)
