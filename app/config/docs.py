import html
import json
from pathlib import Path

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import HTMLResponse


DOCS_HTML = Path(__file__).with_name("docs.html").read_text(encoding="utf-8")


def register_docs(app: FastMCP) -> None:
    @app.custom_route("/docs", methods=["GET"])
    async def docs(_request: Request) -> HTMLResponse:
        cards = []
        tools = sorted(await app.list_tools(), key=lambda tool: tool.name.casefold())
        for tool in tools:
            title = html.escape(tool.title or tool.name)
            name = html.escape(tool.name)
            subtitle = f'<span class="tool-name">{name}</span>' if tool.title and tool.title != tool.name else ""
            description = html.escape(tool.description or "")
            schema = html.escape(json.dumps(tool.parameters, ensure_ascii=False, indent=2))
            properties = tool.parameters.get("properties", {})
            required = set(tool.parameters.get("required", []))
            search = html.escape(
                " ".join([tool.name, tool.title or "", tool.description or "", *properties]),
                quote=True,
            )
            arguments = []
            for key, value in list(properties.items())[:4]:
                kind = value.get("type", "value")
                marker = '<span class="required">*</span>' if key in required else ""
                arguments.append(
                    f'<span class="arg"><span>{html.escape(key)}{marker}</span>'
                    f'<small>{html.escape(kind)}</small></span>'
                )
            if len(properties) > 4:
                arguments.append(f'<span class="arg more">+{len(properties) - 4}</span>')
            arguments_html = "".join(arguments) or '<span class="no-args">Argument yo‘q</span>'
            cards.append(
                f'<article class="tool-card" data-search="{search}">'
                f'<div class="tool-heading"><span class="tool-icon">&#123; &#125;</span>'
                f'<div><h3>{title}</h3>{subtitle}</div></div>'
                f'<p class="tool-description">{description or "Tavsif berilmagan."}</p>'
                f'<div class="arguments">{arguments_html}</div>'
                f'<details><summary>Sxemani ko‘rish <span aria-hidden="true">⌄</span></summary>'
                f'<pre><code>{schema}</code></pre></details></article>'
            )
        page = DOCS_HTML.replace("<!-- SERVER_NAME -->", html.escape(app.name))
        page = page.replace("<!-- TOOL_COUNT -->", str(len(cards)))
        page = page.replace("<!-- TOOL_CARDS -->", "\n".join(cards))
        return HTMLResponse(page)
