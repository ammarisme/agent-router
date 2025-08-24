# Agent Router API

A high-performance, production-ready FastAPI backend for the Agent Router application.

## Features

- **FastAPI 0.116** with async/await support
- **SQLAlchemy 2.0** with async SQLite (WAL mode) or PostgreSQL
- **Redis** for caching and rate limiting
- **JWT Authentication** with Argon2 password hashing
- **Prometheus Metrics** and **OpenTelemetry** tracing
- **Security Headers** and CORS protection
- **Idempotency Keys** for POST operations
- **Health Checks** for Kubernetes readiness/liveness probes
- **Comprehensive Testing** with pytest
- **Code Quality** with ruff, mypy, and pre-commit hooks

## Quick Start

### Prerequisites

- Python 3.12+
- Redis (for caching and rate limiting)
- Docker (optional, for containerized deployment)

### Local Development

1. **Install dependencies:**
   ```bash
   cd apps/api
   pip install -e ".[dev]"
   ```

2. **Set up environment:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Run Redis:**
   ```bash
   # Using Docker
   docker run -d -p 6379:6379 redis:7-alpine
   
   # Or using docker-compose
   docker-compose up redis -d
   ```

4. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Start the development server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health/live
   - Metrics: http://localhost:8000/metrics

### Docker Development

```bash
# Build and run with docker-compose
docker-compose up --build

# Or build and run manually
docker build -t agent-router-api:local .
docker run --rm -p 8000:8000 -v $(pwd)/data:/app/data --env-file .env agent-router-api:local
```

## API Endpoints

### Health Checks
- `GET /health/live` - Liveness probe
- `GET /health/ready` - Readiness probe (checks DB + Redis)

### Items API (v1)
- `GET /v1/items/` - List items with pagination
- `POST /v1/items/` - Create item (supports idempotency)
- `GET /v1/items/{id}` - Get item by ID
- `PUT /v1/items/{id}` - Update item
- `DELETE /v1/items/{id}` - Delete item

### Monitoring
- `GET /metrics` - Prometheus metrics
- `GET /` - API information

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | "Agent Router API" | Application name |
| `APP_ENV` | "development" | Environment (development/production) |
| `DB_DSN` | `sqlite+aiosqlite:///./data/app.db` | Database connection string |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection URL |
| `JWT_SECRET` | (required) | JWT signing secret |
| `CORS_ORIGINS` | `["http://localhost:3000"]` | Allowed CORS origins |
| `RATE_LIMIT` | `"100/minute"` | Rate limiting configuration |

### Database Configuration

#### SQLite (Default)
```bash
DB_DSN=sqlite+aiosqlite:///./data/app.db
```

#### PostgreSQL
```bash
DB_DSN=postgresql+asyncpg://user:password@localhost/dbname
```

### Redis Configuration
```bash
REDIS_URL=redis://localhost:6379/0
```

## Development

### Code Quality

```bash
# Lint and format code
ruff check .
ruff format .

# Type checking
mypy app

# Security audit
bandit -r app/
pip-audit

# Run tests
pytest -v

# Run tests with coverage
pytest --cov=app --cov-report=html
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks
pre-commit run --all-files
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Production Deployment

### Docker

```bash
# Build production image
docker build -t agent-router-api:latest .

# Run with environment variables
docker run -d \
  -p 8000:8000 \
  -e JWT_SECRET=your-secret \
  -e DB_DSN=postgresql+asyncpg://user:pass@db:5432/app \
  -e REDIS_URL=redis://redis:6379/0 \
  agent-router-api:latest
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-router-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent-router-api
  template:
    metadata:
      labels:
        app: agent-router-api
    spec:
      containers:
      - name: api
        image: agent-router-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: jwt-secret
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Monitoring

### Prometheus Metrics

The application exposes Prometheus metrics at `/metrics` including:
- Request counters and latency histograms
- Database connection metrics
- Redis connection metrics

### OpenTelemetry

Configure OpenTelemetry tracing by setting:
```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://your-collector:4317
OTEL_RESOURCE_ATTRIBUTES=service.name=agent-router-api
```

### Logging

Structured JSON logging with correlation IDs:
```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "level": "INFO",
  "message": "Request processed",
  "correlation_id": "uuid-here",
  "trace_id": "trace-id-here"
}
```

## Security

### Security Headers
- Content Security Policy (CSP)
- Strict Transport Security (HSTS)
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Referrer-Policy

### Rate Limiting
- Configurable rate limits per endpoint
- Redis-backed rate limiting
- Idempotency key support for POST operations

### Authentication
- JWT tokens with configurable expiration
- Argon2 password hashing
- Refresh token support

## Backup and Recovery

### SQLite with Litestream (Optional)

For production SQLite deployments, consider using Litestream for continuous backup:

```bash
# Install Litestream
curl -L https://github.com/benbjohnson/litestream/releases/latest/download/litestream-windows-amd64.zip -o litestream.zip
unzip litestream.zip

# Configure Litestream
litestream replicate data/app.db s3://your-backup-bucket/agent-router-api/
```

## Troubleshooting

### Common Issues

1. **Database connection errors:**
   - Ensure the data directory exists: `mkdir -p data`
   - Check database permissions
   - Verify SQLite is in WAL mode

2. **Redis connection errors:**
   - Ensure Redis is running: `redis-cli ping`
   - Check Redis URL configuration
   - Verify network connectivity

3. **Rate limiting issues:**
   - Check Redis connection
   - Verify rate limit configuration
   - Monitor Redis memory usage

### Logs

Check application logs for detailed error information:
```bash
# Docker logs
docker logs container-name

# Kubernetes logs
kubectl logs deployment/agent-router-api
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
