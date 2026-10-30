from collections.abc import Callable, Iterable
from dataclasses import dataclass

from fastmcp import FastMCP


@dataclass(frozen=True)
class Tools:
    registrars: Iterable[Callable[[FastMCP], None]]

    def register_tools(self, app: FastMCP) -> None:
        for register in self.registrars:
            register(app)
