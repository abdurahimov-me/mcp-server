from collections.abc import Iterable
from dataclasses import dataclass

from fastmcp import FastMCP


@dataclass(frozen=True)
class ToolMount:
    server: FastMCP
    namespace: str | None = None


@dataclass(frozen=True)
class Tools:
    servers: Iterable[ToolMount]

    def mount_tools(self, app: FastMCP) -> None:
        for item in self.servers:
            app.mount(item.server, namespace=item.namespace)
