ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim-bookworm AS python-base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install uv

WORKDIR /app
COPY pyproject.toml uv.lock ./

ENV UV_NO_DEV=1
RUN uv export -o requirements.txt

FROM python:${PYTHON_VERSION}-bookworm AS app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN adduser -u 8192 --disabled-password --gecos "" appuser && chown -R appuser /app

COPY --from=python-base --chown=appuser /app/requirements.txt ./
COPY LICENSE ./
RUN pip install -r requirements.txt

COPY src/ ./src
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 CMD ["python", "-c", "import os, sys, urllib.request; host = os.getenv('HEALTHCHECK_HOST', '127.0.0.1'); port = os.getenv('HEALTHCHECK_PORT', '8080'); path = os.getenv('HEALTHCHECK_PATH', '/'); path = path if path.startswith('/') else '/' + path; url = f'http://{host}:{port}{path}'; sys.exit(0 if urllib.request.urlopen(url, timeout=3).status == 200 else 1)"]

CMD ["python", "-m", "src"]
