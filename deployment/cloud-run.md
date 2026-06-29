# Cloud Run Deployment Notes

AgentForge Milestone 11 ships a container-ready interface layer. The runtime can
be deployed as a standard container process using the stdlib HTTP server, or it
can be adapted to an ADK/ASGI deployment later through the optional FastAPI
adapter.

## Local Docker

```bash
docker build -t agentforge:local .
docker run --rm -p 8080:8080 agentforge:local
curl http://localhost:8080/health
curl http://localhost:8080/ready
```

## Docker Compose

```bash
docker compose up --build
```

## Cloud Run Direction

Use the container image created by the Dockerfile, or map this package into an
ADK Cloud Run deployment once the live ADK agent adapter is introduced.

Required environment variables:

```text
AGENTFORGE_ENV=production
AGENTFORGE_HOST=0.0.0.0
AGENTFORGE_PORT=8080
AGENTFORGE_LOG_LEVEL=INFO
```
