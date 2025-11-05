# Development Guide

This guide is for developers who want to contribute to the project or set up a local development environment.

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Git
- Make

## Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/alimentador-bd.git
cd alimentador-bd
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
make install
# or
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp config/.env.example config/.env
```

Edit `config/.env` with your PostgreSQL credentials.

### 5. Initialize Database

```bash
make init
make seed
```

## Development Workflow

### Running Tests

```bash
# Validate connection
python scripts/test_connection.py

# Check table counts
make counts
```

### Starting Stream

```bash
# 30 seconds
timeout 30 make stream

# Custom interval
STREAM_INTERVAL_SECONDS=1 timeout 60 make stream
```

### Code Quality

```bash
# Format code
make fmt

# Lint check
make lint

# Clean cache
make clean
```

## Project Structure

```
scripts/          # Python modules
sql/              # SQL scripts
config/           # Configuration
Makefile          # Build targets
requirements.txt  # Dependencies
```

## Code Style

- **Line length**: 88 characters (Black compatible)
- **Type hints**: Required for all functions
- **Docstrings**: Required for public functions
- **Imports**: stdlib, third-party, local (organized)

## Adding Features

See [ROADMAP.md](ROADMAP.md) for planned features.

### Process

1. Fork repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes following code style
4. Test thoroughly: `make lint && make test`
5. Commit with clear message
6. Push and create Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Debugging

### Enable Debug Logging

```python
import logging
logging.getLogger("scripts").setLevel(logging.DEBUG)
```

### Inspect Database

```bash
psql -U app -h localhost -d teste_pacientes
```

## Common Issues

### "psycopg2.OperationalError: connection refused"

Check PostgreSQL is running and credentials are correct:

```bash
psql -U app -h 10.42.88.67 -d teste_pacientes -c "SELECT 1"
```

### "Stream stops after few events"

Check logs:
```bash
tail -f logs/app.log
```

## Performance

### Time operations

```bash
time make seed
```

Expected: ~2-5 seconds for 13k records.

## Resources

- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical design
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [ROADMAP.md](ROADMAP.md) - Future features
