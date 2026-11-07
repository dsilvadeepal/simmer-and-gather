FROM node:22-bookworm-slim AS frontend
WORKDIR /ui
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY backend/ backend/
RUN uv sync --locked --no-dev && useradd --uid 10001 --create-home simmer
COPY --from=frontend /ui/dist frontend/dist
ENV PATH="/app/.venv/bin:$PATH"
USER simmer
EXPOSE 8000
CMD ["uvicorn", "simmer.server:build_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
