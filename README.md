# Monitoring Stack with FastAPI, Prometheus, Grafana, and Loki

This project sets up a complete monitoring and observability stack using Docker containers. It includes a sample FastAPI application with automated metrics collection, logging, and visualization.

## 🏗️ Architecture Overview

The stack consists of six main components:

- **FastAPI Application**: A simple web API that serves as our application to monitor
- **Prometheus**: Collects and stores metrics from the FastAPI app and system metrics
- **Grafana**: Provides dashboards and visualization for metrics and logs
- **Loki**: Aggregates and stores application logs
- **Node Exporter**: Collects host system metrics (CPU, memory, disk, network)
- **cAdvisor**: Collects container resource usage and performance metrics

## 📁 Project Structure

```
monitoring-stack/
├── app/
│   ├── main.py          # FastAPI application code
│   └── Dockerfile       # Docker configuration for the FastAPI app
├── docker-compose.yml   # Orchestrates all services
├── prometheus.yml       # Prometheus configuration
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
   - Grafana Dashboard: http://localhost:3000 (admin/admin123)
   - Prometheus: http://localhost:9090
   - cAdvisor: http://localhost:8080
   - Loki: http://localhost:3100
   - Node Exporter: Internal access only (metrics available through Prometheus)

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

Orchestrates six services across two custom networks:

1. **fastapi-app**: Your application container
   - Builds from the local Dockerfile
   - Exposes port 8000 to host
   - Configured to send logs to Loki
   - Connected to both frontend and monitoring networks

2. **prometheus**: Metrics collection service
   - Scrapes metrics from the FastAPI app, Node Exporter, and cAdvisor
   - Stores time-series data
   - Web UI available at port 9090
   - Connected to monitoring network only

3. **grafana**: Visualization and dashboards
   - Pre-configured to connect to Prometheus and Loki
   - Persistent data storage using Docker volumes
   - Web UI available at port 3000
   - Connected to both frontend and monitoring networks

4. **loki**: Log aggregation service
   - Collects logs from all containers
   - Provides log querying capabilities
   - Available at port 3100
   - Connected to monitoring network only

5. **node-exporter**: System metrics collection service
   - Collects host system metrics (CPU, memory, disk, network, etc.)
   - Runs with host PID namespace for comprehensive monitoring
   - Internal access only (no host port binding)
   - Connected to monitoring network only

6. **cadvisor**: Container metrics collection service
   - Collects container resource usage and performance metrics
   - Provides insights into Docker container behavior
   - Web UI available at port 8080
   - Connected to both frontend and monitoring networks

## 🔧 Configuration Details

### Network Architecture

The stack uses two Docker networks for improved security and organization:

- **frontend**: Network for user-facing services (FastAPI, Grafana, cAdvisor)
- **monitoring**: Network for internal monitoring services (Prometheus, Loki, Node Exporter, cAdvisor)

Services are strategically placed:
- FastAPI, Grafana, and cAdvisor: Both networks (can communicate with all services)
- Prometheus, Loki, and Node Exporter: Monitoring network only (internal communication)

### Logging Configuration

All services are configured to send logs to Loki using the Docker Loki logging driver:
- Logs are batched for efficiency (batch size: 400)
- Retry configuration (5 retries, 2s max backoff)
- Each service has labeled logs for easy filtering

### Security Features

- **Node Exporter**: No external port exposure (internal access only)
- **Network Segmentation**: Separate networks for frontend and monitoring
- **Graceful Shutdowns**: Configured stop signals and grace periods
- **cAdvisor**: Requires privileged access for container monitoring

## 📈 Monitoring Your Application

### Viewing Metrics in Prometheus

1. Open http://localhost:9090
2. Try these queries:
   - **Application Metrics:**
     - `http_requests_total` - Total HTTP requests
     - `http_request_duration_seconds` - Request duration
     - `rate(http_requests_total[5m])` - Request rate per second
   - **System Metrics:**
     - `node_cpu_seconds_total` - CPU usage by core
     - `node_memory_MemAvailable_bytes` - Available memory
     - `node_filesystem_size_bytes` - Disk space usage
     - `node_load1` - 1-minute load average
   - **Container Metrics:**
     - `container_cpu_usage_seconds_total` - Container CPU usage
     - `container_memory_usage_bytes` - Container memory usage
     - `container_network_receive_bytes_total` - Container network RX
     - `container_fs_usage_bytes` - Container filesystem usage

### Creating Dashboards in Grafana

1. Open http://localhost:3000
2. Log in with admin/admin123
3. Add data sources:
   - Prometheus: http://prometheus:9090
   - Loki: http://loki:3100
4. Create dashboards combining application, system, and container metrics with logs

### Container Monitoring with cAdvisor

cAdvisor provides detailed container-level insights:

- **Resource Usage**: CPU, memory, network, and filesystem usage per container
- **Performance Metrics**: Container performance characteristics and bottlenecks
- **Historical Data**: Time-series data for container resource consumption
- **Container Discovery**: Automatic detection of running containers
- **Web Interface**: Browse container stats at http://localhost:8080

### System Monitoring with Node Exporter

Node Exporter provides comprehensive host system metrics:

- **CPU Metrics**: Usage, load average, context switches
- **Memory Metrics**: RAM usage, swap, buffers/cache
- **Storage Metrics**: Disk usage, I/O statistics, filesystem info
- **Network Metrics**: Interface statistics, connections, traffic
- **System Health**: Uptime, temperature sensors, hardware status

### Viewing Logs in Grafana

1. Go to Explore section in Grafana
2. Select Loki as data source
3. Use queries like: 
   - `{service="fastapi"}` - FastAPI application logs
   - `{service="node-exporter"}` - Node Exporter logs
   - `{service="prometheus"}` - Prometheus logs
   - `{service="cadvisor"}` - cAdvisor logs

## 🛠️ Development Tips

### Adding New Metrics

Add custom metrics to your FastAPI app:
```python
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('app_request_duration_seconds', 'Request duration')
```

### Useful Prometheus Queries

**System Performance:**
```promql
# CPU usage percentage
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage percentage
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# Disk usage percentage
(1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes)) * 100
```

**Container Performance:**
```promql
# Container CPU usage percentage
rate(container_cpu_usage_seconds_total{name!=""}[5m]) * 100

# Container memory usage percentage
(container_memory_usage_bytes{name!=""} / container_spec_memory_limit_bytes{name!=""}) * 100

# Container network traffic
rate(container_network_receive_bytes_total{name!=""}[5m])
```

### Debugging Services

Check individual service logs:
```bash
docker-compose logs fastapi-app
docker-compose logs prometheus
docker-compose logs grafana
docker-compose logs loki
docker-compose logs node-exporter
docker-compose logs cadvisor
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

1. **Port conflicts**: Ensure ports 3000, 8000, 8080, 9090, and 3100 are not in use
2. **Docker permissions**: Run with `sudo` if you encounter permission issues
3. **Service not starting**: Check logs with `docker-compose logs [service-name]`
4. **Node Exporter mounting issues**: Ensure Docker has access to host filesystem
5. **cAdvisor privileged access**: cAdvisor requires privileged mode for container monitoring

### Health Checks

- FastAPI: `curl http://localhost:8000/health` (if implemented)
- Prometheus: `curl http://localhost:9090/-/healthy`
- Grafana: Check if web UI loads at http://localhost:3000
- Loki: `curl http://localhost:3100/ready`
- Node Exporter: Check metrics with `curl http://node-exporter:9100/metrics` (internal)
- cAdvisor: `curl http://localhost:8080/healthz`

## 📚 Next Steps

1. **Add more endpoints** to your FastAPI application
2. **Create custom Grafana dashboards** for your specific metrics
3. **Set up alerting rules** in Prometheus for system and application metrics
4. **Configure Grafana alerts** for important metrics (high CPU, low disk space, etc.)
5. **Add more applications** to monitor by extending the docker-compose.yml
6. **Create system monitoring dashboards** using Node Exporter metrics
7. **Create container monitoring dashboards** using cAdvisor metrics
8. **Set up log-based alerts** using Loki queries
9. **Monitor container resource limits** and optimize application performance

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Happy Monitoring!** 🎉
