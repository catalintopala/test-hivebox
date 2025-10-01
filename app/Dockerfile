FROM python:3.13.7-slim-trixie@sha256:27f90d79cc85e9b7b2560063ef44fa0e9eaae7a7c3f5a9f74563065c5477cc24

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Create the user to run the app.
RUN groupadd hivebox && useradd -m -g hivebox hivebox
USER hivebox
WORKDIR /home/hivebox

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.8.15@sha256:a5727064a0de127bdb7c9d3c1383f3a9ac307d9f2d8a391edc7896c54289ced0 /uv /uvx /bin/

WORKDIR /app

# Install dependencies.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-dev --locked --no-install-project

COPY --chown=hivebox:hivebox . .

# Sync the project.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --locked

EXPOSE 80/tcp
EXPOSE 80/udp

ENTRYPOINT ["uv", "run", "fastapi"]
CMD ["run", "main.py", "--port", "80"]
