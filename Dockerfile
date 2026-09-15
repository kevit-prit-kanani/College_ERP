# syntax=docker/dockerfile:1.7

FROM ghcr.io/astral-sh/uv:0.9.18 AS uv

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install exactly the dependencies recorded in uv.lock. This layer is cached
# until the dependency metadata changes.
COPY --from=uv /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Run the API without root. Source and runtime uploads belong to this account.
RUN addgroup --system app && adduser --system --ingroup app app
COPY --chown=app:app . .
RUN mkdir -p uploads && chown -R app:app uploads

USER app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
