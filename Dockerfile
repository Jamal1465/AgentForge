FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    AGENTFORGE_HOST=0.0.0.0 \
    AGENTFORGE_PORT=8080

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir -e .

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -m agentforge.interfaces.cli.main ready >/dev/null || exit 1

CMD ["python", "-m", "agentforge.interfaces.cli.main", "serve"]
