#!/bin/sh
set -eu

exec gunicorn --config /srv/mcp/gunicorn_conf.py main:asgi_app
