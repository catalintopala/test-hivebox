FROM ghcr.io/astral-sh/uv:0.8.15-python3.13-trixie-slim@sha256:f01cf9b376c8109d92d2bb144dbff892e34103352a63a875e4a2c54cc127f24a AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN useradd --create-home hivebox
USER hivebox
WORKDIR /home/hivebox/app

# Install dependencies.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project --no-dev --no-editable

COPY . .

# Sync the project.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --no-editable

FROM python:3.13.7-slim-trixie@sha256:2be5d3cb08aa616c6e38d922bd7072975166b2de772004f79ee1bae59fe983dc

RUN useradd --create-home hivebox
USER hivebox

COPY --from=builder /home/hivebox/app /home/hivebox/app

WORKDIR /home/hivebox/app

EXPOSE 80/tcp
EXPOSE 80/udp

ENTRYPOINT [".venv/bin/fastapi"]
CMD ["run", "main.py", "--port", "80"]
