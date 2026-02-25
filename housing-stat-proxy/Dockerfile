FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.10 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

FROM python:3.14-slim
WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY app.py .

ENV PATH="/app/.venv/bin:$PATH"

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--no-control-socket", "app:app"]
