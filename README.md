# Ploston Enterprise

Ploston Enterprise - Premium Agent Execution Layer

## Overview

This package provides enterprise features for the Ploston agent execution platform,
including license validation, policy-based access control, pattern mining, and
workflow synthesis.

## Installation

### From PyPI (Private)

```bash
pip install ploston-enterprise
```

### From Source

```bash
git clone https://github.com/ostanlabs/ploston-enterprise.git
cd ploston-enterprise
make install
```

## Usage

### Set License Key

```bash
export PLOSTON_LICENSE_KEY=your-license-key
# or
export PLOSTON_LICENSE_FILE=/path/to/license.jwt
```

### Start the Server

```bash
# Using the CLI
ploston-enterprise-server --host 0.0.0.0 --port 8080

# Or using make
make serve
```

### Server Options

| Option | Default | Description |
|--------|---------|-------------|
| `--host` | `0.0.0.0` | Host to bind to |
| `--port` | `8080` | Port for MCP HTTP server |
| `--metrics-port` | `9090` | Port for Prometheus metrics |
| `--reload` | `false` | Enable auto-reload for development |

## Docker

### Pull from Docker Hub

```bash
docker pull ostanlabs/ploston-enterprise:latest
```

### Run with Docker

```bash
docker run -d \
  --name ploston-enterprise \
  -p 8080:8080 \
  -p 9090:9090 \
  -e PLOSTON_LICENSE_KEY=your-license-key \
  ostanlabs/ploston-enterprise:latest
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PLOSTON_LICENSE_KEY` | - | License key (required) |
| `PLOSTON_LICENSE_FILE` | - | Path to license file (alternative to key) |
| `PLOSTON_HOST` | `0.0.0.0` | Server host |
| `PLOSTON_PORT` | `8080` | MCP HTTP port |
| `PLOSTON_METRICS_PORT` | `9090` | Prometheus metrics port |
| `PLOSTON_LOG_LEVEL` | `INFO` | Log level (DEBUG, INFO, WARNING, ERROR) |

### Docker Compose Example

```yaml
version: '3.8'
services:
  ploston-enterprise:
    image: ostanlabs/ploston-enterprise:latest
    ports:
      - "8080:8080"
      - "9090:9090"
    environment:
      - PLOSTON_LICENSE_KEY=${PLOSTON_LICENSE_KEY}
      - PLOSTON_LOG_LEVEL=INFO
    restart: unless-stopped
```

### Build Locally

```bash
make docker-build
make docker-run
```

## Development

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

```bash
make install
```

### Commands

```bash
make help         # Show all commands
make test         # Run all tests
make test-unit    # Run unit tests only
make lint         # Run linter
make format       # Format code
make check        # Run lint + tests
make serve        # Start server locally
make docker-build # Build Docker image
make docker-run   # Run in Docker
```

## Features

- License validation (online and offline)
- Policy-based access control (RBAC/ABAC)
- Workflow pattern mining
- Workflow synthesis
- Extended limits and quotas
- Prometheus metrics

## License

Proprietary - Contact sales@ostanlabs.com
