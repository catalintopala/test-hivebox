FROM ghcr.io/astral-sh/uv:0.8.15-trixie-slim@sha256:76e1b7a58ab7b1e7e9c213d67d1c5738ca9dbf76a39de6155bf202a58e07cc56 AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_INSTALL_DIR=/python \
    UV_PYTHON_PREFERENCE=only-managed

RUN uv python install 3.13

WORKDIR /app

# Install dependencies.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev --no-editable

COPY . .

# Sync the project.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

FROM gcr.io/distroless/cc:nonroot

COPY --from=builder --chown=python:python /python /python

COPY --from=builder --chown=app:app /app /app

EXPOSE 80/tcp
EXPOSE 80/udp

ENTRYPOINT ["/app/.venv/bin/fastapi"]
CMD ["run", "/app/main.py", "--port", "80"]
