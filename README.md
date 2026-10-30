# MCP server

FastMCP 4 asosidagi HTTP MCP server. `app/tools/` ichidagi kichik MCP serverlar `app/utils/tools.py` yordamida asosiy serverga `mount` qilinadi. Hozir `greet` namuna tool’i bor.

## Manzillar

| Manzil | Maqsad |
| --- | --- |
| `/mcp` | MCP client ulanadigan Streamable HTTP endpoint |
| `/docs` | Tool sxemalaridan avtomatik tuziladigan katalog va ulanish yo‘riqnomasi |

MCP Swagger/OpenAPI REST API emas. `/docs` sahifasidagi tool katalogi `list_tools()` ma’lumotlaridan har so‘rovda avtomatik tuziladi. Toollarni interaktiv sinash uchun MCP Inspector ishlating. `/docs` ochiq HTTP yo‘l; JWT auth `/mcp`ga qo‘llanadi.

Inspector uchun `npx @modelcontextprotocol/inspector`ni ishga tushiring, brauzerda **Streamable HTTP** transportini tanlang va server URL sifatida `http://127.0.0.1:8000/mcp`ni kiriting. Docker rejimida ulanishga `Authorization: Bearer <JWT_TOKEN>` headerini qo‘shing. Inspector tool ro‘yxati, argumentlari va chaqiruv natijasini ko‘rsatadi.

## Docker bilan production ishga tushirish

1. `.env.example` nusxasini `.env` qilib oling.
2. `JWT_SECRET_KEY`ga `slayd24-ai` ishlatadigan **aynan o‘sha HS256 signing secret**ni kiriting. `.env`dagi `MCP_AUTH_MODE=jwt` qiymatini saqlang. `.env`ni Git’ga qo‘shmang.
3. Repo ildizida ishga tushiring:

```powershell
Copy-Item .env.example .env
# .env ichidagi JWT_SECRET_KEY qiymatini to‘ldiring
docker compose up --build -d
docker compose ps
```

Keyin `http://127.0.0.1:8000/docs`ni oching. MCP endpoint: `http://127.0.0.1:8000/mcp`. Loglar: `docker compose logs -f mcp`. To‘xtatish: `docker compose down`.

Compose `.env`ni `env_file` orqali containerga uzatadi. Container Gunicorn master va Uvicorn workerlar bilan ishlaydi; `GUNICORN_WORKERS` workerlar sonini belgilaydi. `MCP_HOST=0.0.0.0` container ichidagi bind manzili, `MCP_PORT=8000` esa container porti. Compose serverni standart holatda faqat hostning `127.0.0.1` manziliga chiqaradi. Tashqi clientlar uchun HTTPS reverse proxy orqali `/mcp`ni chiqaring; `MCP_BIND_ADDRESS`ni faqat tarmoq siyosatiga mos holda o‘zgartiring. `MCP_PUBLIC_PORT` host portini almashtiradi.

`.env`dagi `COMPOSE_PROJECT_NAME` Compose project nomini va FastMCP server nomini belgilaydi. `CONTAINER_PREFIX` Docker image va container nomi prefiksi uchun ishlatiladi; masalan, `CONTAINER_PREFIX=myapp` bo‘lsa container nomi `myapp-mcp` bo‘ladi. Bir hostda bir nechta instansiya ishlasa, har biriga alohida prefix qo‘ying.

`slayd24-ai`ning hozirgi JWT’larida `iss` va `aud` claim’lari yo‘q. Shuning uchun `.env`dagi `MCP_JWT_ISSUER` va `MCP_JWT_AUDIENCE` dastlab bo‘sh qoladi. Token chiqarish qismiga ushbu claim’lar qo‘shilgach, ikkisini ham tekshirish uchun mos qiymatga sozlang. Token muddati (`exp`) va HS256 imzosi tekshiriladi.

## Lokal ishga tushirish

Python 3.12 tavsiya etiladi. Repo ildizida:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirments\dev.txt
.venv\Scripts\python.exe app\main.py
```

Lokal `python app/main.py` FastMCP’ning ichki Uvicorn serverini ishga tushiradi. Sozlamalar `pydantic-settings` orqali repo ildizidagi `.env` faylidan yoki environment o‘zgaruvchilaridan o‘qiladi; environment qiymatlari ustun turadi. `.env` bo‘lmasa `127.0.0.1:8000`da auth’siz ishlaydi. Docker uchun nusxalangan `.env` lokal rejimga ham ta’sir qiladi: unda `MCP_HOST=0.0.0.0` va `MCP_AUTH_MODE=jwt` berilgan.

## Client bilan tekshirish

JWT rejimida `slayd24-ai` bergan tokenni `SLAYD24_JWT` environment o‘zgaruvchisiga qo‘ying:

```python
import asyncio
import os
from fastmcp import Client

async def main():
    async with Client("http://127.0.0.1:8000/mcp", auth=os.environ["SLAYD24_JWT"]) as client:
        print([tool.name for tool in await client.list_tools()])
        print((await client.call_tool("greet", {"name": "Ali"})).data)

asyncio.run(main())
```

## Yangi tool qo‘shish

`app/tools/`da `FastMCP` obyektli modul yarating, tool’larni unga dekorator bilan qo‘shing. So‘ng modulning `mcp` obyektini `app/tools/__init__.py`dagi `__tools__` ro‘yxatiga kiriting; `Server` uni asosiy serverga mount qiladi.
