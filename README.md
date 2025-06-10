# Monitoring Stack with FastAPI, Prometheus, Grafana, and Loki

This project sets up a complete monitoring and observability stack using Docker containers. It includes a sample FastAPI application with automated metrics collection, logging, and visualization.

## 🏗️ Architecture Overview

The stack consists of four main components:

- **FastAPI Application**: A simple web API that serves as our application to monitor
- **Prometheus**: Collects and stores metrics from the FastAPI app
- **Grafana**: Provides dashboards and visualization for metrics and logs
- **Loki**: Aggregates and stores application logs

## 📁 Project Structure

```
monitoring-stack/
├── app/
│   ├── main.py          # FastAPI application code
│   └── Dockerfile       # Docker configuration for the FastAPI app
├── docker-compose.yml   # Orchestrates all services
├── prometheus.yml       # Prometheus configuration (if exists)
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker installed on your system
- Docker Compose installed

### Running the Stack

1. **Clone or navigate to this directory**
   ```bash
   cd monitoring-stack
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Access the services**
   - FastAPI Application: http://localhost:8000
   - Grafana Dashboard: http://localhost:3000 (admin/admin)
   - Prometheus: http://localhost:9090
   - Loki: http://localhost:3100

4. **Test the FastAPI app**
   ```bash
   curl http://localhost:8000
   curl http://localhost:8000/items/42?q=test
   ```

## 📊 What Each Component Does

### FastAPI Application (`app/main.py`)

A simple web API with two endpoints:
- `GET /` - Returns a "Hello World" message
- `GET /items/{item_id}` - Returns item information with optional query parameter

**Key features:**
- Automatic Prometheus metrics collection using `prometheus-fastapi-instrumentator`
- Structured logging that gets sent to Loki
- Health check endpoints for monitoring

### Docker Configuration (`app/Dockerfile`)

- Uses Python 3.12 slim base image
- Installs `uv` for fast Python package management
- Copies dependencies and application code
- Exposes port 8000 for the FastAPI application
- Runs the app using Uvicorn ASGI server

### Docker Compose Setup (`docker-compose.yml`)

Orchestrates four services in a custom network:

1. **fastapi-app-0**: Your application container
   - Builds from the local Dockerfile
   - Exposes port 8000
   - Configured to send logs to Loki

2. **prometheus**: Metrics collection service
   - Scrapes metrics from the FastAPI app
   - Stores time-series data
   - Web UI available at port 9090

3. **grafana**: Visualization and dashboards
   - Pre-configured to connect to Prometheus and Loki
   - Persistent data storage using Docker volumes
   - Web UI available at port 3000

4. **loki**: Log aggregation service
   - Collects logs from all containers
   - Provides log querying capabilities
   - Available at port 3100

## 🔧 Configuration Details

### Logging Configuration

All services are configured to send logs to Loki using the Docker Loki logging driver:
- Logs are batched for efficiency (batch size: 100)
- Log rotation (max 10MB per file, 3 files max)
- Each service has labeled logs for easy filtering

### Network Setup

All services run in a custom bridge network named `monitoring` for secure inter-container communication.

## 📈 Monitoring Your Application

### Viewing Metrics in Prometheus

1. Open http://localhost:9090
2. Try these queries:
   - `http_requests_total` - Total HTTP requests
   - `http_request_duration_seconds` - Request duration
   - `rate(http_requests_total[5m])` - Request rate per second

### Creating Dashboards in Grafana

1. Open http://localhost:3000
2. Log in with admin/admin
3. Add Prometheus as a data source: http://prometheus:9090
4. Add Loki as a data source: http://loki:3100
5. Create dashboards combining metrics and logs

### Viewing Logs in Grafana

1. Go to Explore section in Grafana
2. Select Loki as data source
3. Use queries like: `{service="fastapi"}`

## 🛠️ Development Tips

### Adding New Metrics

Add custom metrics to your FastAPI app:
```python
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('app_request_duration_seconds', 'Request duration')
```

### Debugging Services

Check individual service logs:
```bash
docker-compose logs fastapi-app-0
docker-compose logs prometheus
docker-compose logs grafana
docker-compose logs loki
```

### Stopping the Stack

```bash
docker-compose down
```

To remove volumes and clean up completely:
```bash
docker-compose down -v
```

## 🚨 Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 3000, 8000, 9090, and 3100 are not in use
2. **Docker permissions**: Run with `sudo` if you encounter permission issues
3. **Service not starting**: Check logs with `docker-compose logs [service-name]`

### Health Checks

- FastAPI: `curl http://localhost:8000/health` (if implemented)
- Prometheus: `curl http://localhost:9090/-/healthy`
- Grafana: Check if web UI loads at http://localhost:3000

## 📚 Next Steps

1. **Add more endpoints** to your FastAPI application
2. **Create custom Grafana dashboards** for your specific metrics
3. **Set up alerting rules** in Prometheus
4. **Configure Grafana alerts** for important metrics
5. **Add more applications** to monitor by extending the docker-compose.yml

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Happy Monitoring!** 🎉
