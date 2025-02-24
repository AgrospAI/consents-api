FROM python:3.13-slim-bookworm AS installer

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /env
COPY pyproject.toml uv.lock /env/

RUN uv venv .venv && uv sync

FROM python:3.13-slim-bookworm AS runner

WORKDIR /app

COPY --from=installer /env/.venv /.venv
ENV PATH="/.venv/bin/:$PATH"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]