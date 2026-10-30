import os


bind = f"{os.getenv('MCP_HOST', '0.0.0.0')}:{os.getenv('MCP_PORT', '8000')}"
worker_class = "uvicorn_worker.UvicornWorker"
workers = int(os.getenv("GUNICORN_WORKERS", "2"))
timeout = 120
graceful_timeout = 30
keepalive = 5
accesslog = "-"
errorlog = "-"
