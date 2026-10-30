FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HOME=/tmp \
    PYTHONPATH=/srv/mcp/app

WORKDIR /srv/mcp

COPY requirments/ ./requirments/
RUN python -m pip install --no-cache-dir -r requirements/prod.txt \
    && groupadd --system --gid 10001 mcp \
    && useradd --system --uid 10001 --gid mcp --home-dir /tmp --no-create-home mcp

COPY app/ ./app/
COPY gunicorn_conf.py ./gunicorn_conf.py
COPY scripts/entrypoint.sh ./scripts/entrypoint.sh
RUN sed -i 's/\r$//' ./scripts/entrypoint.sh \
    && chmod 755 ./scripts/entrypoint.sh \
    && chown -R mcp:mcp /srv/mcp

USER mcp
EXPOSE 8000

ENTRYPOINT ["/srv/mcp/scripts/entrypoint.sh"]
