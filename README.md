#  MiniMathAPI – FastAPI Microservice

A lightweight microservice that exposes mathematical operations (`pow`, `fib`, `factorial`) via a REST API. All requests are logged in a SQLite database.

The service uses Pydantic for validation, includes request-level caching, multithreading for CPU-bound operations, and Prometheus-compatible monitoring at `/metrics`. The application is containerized with Docker and deployed using Rancher.

## Run with Docker

```bash
docker build -t minimathapi .
docker run -p 8000:8000 minimathapi
```
Access the API docs:
http://localhost:8000/docs

## Stack
FastAPI + Uvicorn

SQLModel + SQLite

Pydantic

ThreadPoolExecutor

Prometheus monitoring

Docker + Rancher

## Testing
```bash
pytest
```
Unit tests cover core logic and API endpoints (tests/ folder).

## Monitoring

Metrics exposed at `/metrics`, compatible with Prometheus and Rancher monitoring.

## Deployment

Built with Docker and deployed to Rancher via container workload.
