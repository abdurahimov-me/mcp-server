import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from fastmcp import Client
from pydantic import ValidationError
from starlette.testclient import TestClient


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from config.settings import Settings  # noqa: E402
import main  # noqa: E402
from main import mcp  # noqa: E402


class SettingsTests(unittest.TestCase):
    def test_environment_values_are_validated(self) -> None:
        with patch.dict("os.environ", {"COMPOSE_PROJECT_NAME": "demo-mcp", "MCP_PORT": "9000", "MCP_AUTH_MODE": "JWT", "JWT_SECRET_KEY": "test-secret"}, clear=True):
            settings = Settings(_env_file=None)
        self.assertEqual(settings.project_name, "demo-mcp")
        self.assertEqual(settings.port, 9000)
        self.assertEqual(settings.auth_mode, "jwt")
        self.assertEqual(settings.jwt_secret_key.get_secret_value(), "test-secret")

    def test_jwt_requires_secret(self) -> None:
        with patch.dict("os.environ", {"MCP_AUTH_MODE": "jwt", "JWT_SECRET_KEY": ""}, clear=True):
            with self.assertRaises(ValidationError):
                Settings(_env_file=None)

    def test_fastmcp_name_follows_project_name(self) -> None:
        with patch.dict("os.environ", {"COMPOSE_PROJECT_NAME": "demo-mcp"}, clear=True):
            settings = Settings(_env_file=None)
        with patch.object(main, "SETTINGS", settings):
            self.assertEqual(main.app().name, "demo-mcp")


class ToolTests(unittest.IsolatedAsyncioTestCase):
    async def test_greet_tool_can_be_called(self) -> None:
        async with Client(mcp) as client:
            names = [tool.name for tool in await client.list_tools()]
            self.assertIn("greet", names)
            result = await client.call_tool("greet", {"name": "Ali"})
            self.assertEqual(result.data, "Salom, Ali!")


class RouteTests(unittest.TestCase):
    def test_health_and_docs_routes(self) -> None:
        with TestClient(mcp.http_app()) as client:
            health = client.get("/health")
            self.assertEqual(health.status_code, 200)
            self.assertEqual(health.json(), {"status": "ok"})

            docs = client.get("/docs")
            self.assertEqual(docs.status_code, 200)
            self.assertIn(mcp.name, docs.text)
            self.assertIn("greet", docs.text)
            self.assertIn("tool-grid", docs.text)
            self.assertIn("tool-search", docs.text)
            self.assertIn("<details>", docs.text)
            self.assertIn('data-search="greet', docs.text)
            self.assertNotIn("\ufffd", docs.text)
            self.assertIn("name", docs.text)
