# 🏥 Alimentador-BD

**OLTP Hospital Simulator** — Continuous data streaming for CDC testing with Debezium

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![PostgreSQL 14+](https://img.shields.io/badge/PostgreSQL-14+-336791.svg)](https://www.postgresql.org/)

---

## 🎯 Overview

Alimentador-BD is a production-ready Python simulator that generates **realistic hospital data** in PostgreSQL with continuous INSERT/UPDATE operations. Perfect for testing **CDC (Change Data Capture)** pipelines with Debezium, validating data consistency, and developing ETL/ELT systems.

### Key Features

✨ **Continuous Data Streaming**
- 70% INSERT operations (new records)
- 30% UPDATE operations (realistic modifications)
- ~1 operation per 2 seconds (configurable)

🏥 **Realistic Hospital Schema**
- 7 OLTP tables (patients, doctors, appointments, exams, admissions, etc.)
- ~13k initial seed records
- Proper foreign keys and constraints
- CDC-compatible triggers and indexes

🐍 **Production-Ready Code**
- Type hints, docstrings, PEP 8 compliance
- Error handling with exponential backoff
- Batch operations with transaction support
- Comprehensive logging with rotation

🐳 **Multiple Deployment Options**
- Local development (Docker Compose)
- AWS EC2 / RDS
- Kubernetes
- Standalone Python

📚 **Comprehensive Documentation**
- Quick start (5 minutes)
- Complete user guide (Portuguese)
- Technical architecture
- Production deployment guide
- Developer contribution guide

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Docker & Docker Compose (optional)

### 1. Setup (5 minutes)

```bash
# Clone repository
git clone https://github.com/yourusername/alimentador-bd.git
cd alimentador-bd

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure (copy example and edit credentials)
cp config/.env.example config/.env
# Edit config/.env with your PostgreSQL connection
```

### 2. Initialize Database

```bash
make init    # Create schema and indexes
make seed    # Populate ~13k initial records
```

### 3. Start Streaming

```bash
make stream  # Continuous INSERT/UPDATE operations
```

### 4. Monitor

```bash
# In another terminal
make counts  # Show record counts
tail -f logs/app.log  # View live logs
```

### With Docker Compose

```bash
# Start PostgreSQL + PgAdmin
docker-compose up -d postgres

# From host machine, initialize
make init
make seed

# Stream
make stream
```

---

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `make install` | Create venv and install dependencies |
| `make init` | Create schema, indexes, lookup data |
| `make seed` | Populate ~13k initial records |
| `make stream` | Start continuous streaming |
| `make reset` | Drop + recreate + seed all |
| `make counts` | Display table record counts |
| `make fmt` | Format code with Black |
| `make lint` | Check code with Ruff |
| `make clean` | Remove cache and temp files |

---

## 🏛️ Database Schema

### 7 OLTP Tables

```sql
pacientes (2,000)
├── id, nome, nascimento, cpf, telefone, endereco
├── created_at, updated_at (automatic)
└── PRIMARY KEY, UNIQUE(cpf), INDEX(cpf)

medicos (200)
├── id, nome, crm, especialidade, telefone
└── PRIMARY KEY, UNIQUE(crm), INDEX(crm)

convenios (12)
├── id, nome, cnpj, tipo, cobertura
└── PRIMARY KEY, UNIQUE(cnpj)

pacientes_convenios (2,500+)
├── id, paciente_id → pacientes
├── convenio_id → convenios
└── UNIQUE(paciente_id, convenio_id)

consultas (4,000+)
├── id, paciente_id → pacientes
├── medico_id → medicos
├── data, motivo, status (agendada|realizada|cancelada|faltou)
└── INDEX(paciente_id, medico_id, data)

exames (3,500+)
├── id, paciente_id → pacientes
├── tipo_exame, data, resultado
└── INDEX(paciente_id, data)

internacoes (1,200+)
├── id, paciente_id → pacientes
├── data_entrada, data_saida, motivo, quarto
└── CHECK(data_saida >= data_entrada)
```

### Key Features

- ✅ **BIGSERIAL primary keys** on all tables
- ✅ **Unique constraints** on natural keys (CPF, CRM, CNPJ)
- ✅ **Cascading foreign keys** (ON UPDATE CASCADE, ON DELETE RESTRICT)
- ✅ **Automatic timestamps** with triggers (`created_at`, `updated_at`)
- ✅ **9 strategic indexes** for performance
- ✅ **CDC-compatible** schema for Debezium

---

## ⚙️ Configuration

### Environment Variables (`.env`)

```env
# PostgreSQL Connection
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD=postgres
PG_DATABASE=teste_pacientes

# Streaming Configuration
STREAM_INTERVAL_SECONDS=2      # Delay between operations (seconds)
BATCH_SIZE=50                  # Records per batch
MAX_JITTER_MS=400              # Random delay variation (ms)

# Seeding Configuration
SEED_PACIENTES=2000
SEED_MEDICOS=200
SEED_CONVENIOS=12
SEED_CONSULTAS=4000
SEED_EXAMES=3500
SEED_INTERNACOES=1200
SEED_PACIENTES_CONVENIOS=2500

# Logging
LOG_LEVEL=INFO                 # DEBUG, INFO, WARNING, ERROR
```

### TOML Configuration (`config/settings.toml`)

```toml
[db]
search_path = "public"
connect_timeout = 10

[stream]
interval_seconds = 2
batch_size = 50
max_jitter_ms = 400
fail_fast_on_critical = true

[logging]
level = "INFO"
rotate_when = "midnight"
backup_count = 7
```

---

## 🔄 Streaming Operations

The simulator executes **8 realistic operations**:

### INSERTs (70%)
1. **insert_paciente** - Register new patient
2. **insert_consulta** - Schedule new appointment
3. **insert_exame** - Request new lab test
4. **insert_internacao** - Admit patient to hospital

### UPDATEs (30%)
5. **update_paciente** - Modify contact info
6. **update_consulta** - Change appointment status
7. **update_exame** - Record lab results
8. **update_internacao** - Discharge patient

Each operation:
- ✅ Validates foreign keys before execution
- ✅ Commits in batches for performance
- ✅ Logs operation type and counts
- ✅ Handles errors gracefully (continues on non-critical failures)
- ✅ Reconnects automatically with exponential backoff

---

## 🧪 Testing & Validation

### Verify Data Consistency

```sql
-- Check for orphaned records (should return 0)
SELECT COUNT(*) FROM consultas 
WHERE paciente_id NOT IN (SELECT id FROM pacientes);

-- Verify unique CPFs
SELECT cpf, COUNT(*) FROM pacientes 
GROUP BY cpf HAVING COUNT(*) > 1;

-- Check timestamp coherence
SELECT COUNT(*) FROM consultas 
WHERE created_at > now();
```

### Monitor Growth

```bash
# Terminal 1 - Stream for 5 minutes
timeout 300 make stream

# Terminal 2 - Check growth every 10 seconds
while true; do make counts; sleep 10; done
```

### Performance Testing

```bash
# Stress test: high throughput
STREAM_INTERVAL_SECONDS=0 timeout 60 make stream

# Measure: ~200 ops/minute
```

---

## 🔌 Debezium / CDC Integration

Alimentador-BD generates **CDC-compatible changes** for Debezium capture.

### Debezium Configuration

```json
{
  "name": "postgres-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "10.42.88.67",
    "database.port": 5441,
    "database.user": "app",
    "database.password": "app123",
    "database.dbname": "teste_pacientes",
    "database.server.name": "alimentador-bd",
    "plugin.name": "pgoutput",
    "publication.name": "alimentador_pub",
    "table.include.list": "public.*",
    "publication.autocreate.mode": "filtered",
    "slot.name": "alimentador_slot"
  }
}
```

### What Gets Captured

- ✅ All INSERT operations → `{before: null, after: {patient data}}`
- ✅ All UPDATE operations → `{before: {old data}, after: {new data}}`
- ✅ `updated_at` field automatically populated by triggers
- ✅ Natural keys (CPF, CRM, CNPJ) for deduplication

### Expected Kafka Events

```json
{
  "schema": {...},
  "payload": {
    "before": null,
    "after": {
      "id": 2045,
      "nome": "João Silva",
      "cpf": "123.456.789-00",
      "created_at": 1705255200000,
      "updated_at": 1705255200000
    },
    "source": {
      "version": "2.4.0.Final",
      "connector": "postgresql",
      "name": "alimentador-bd",
      "ts_ms": 1705255200123,
      "txId": 12345,
      "lsn": 12345678,
      "xmin": null
    },
    "op": "c",
    "ts_ms": 1705255200123,
    "transaction": null
  }
}
```

---

## 📁 Project Structure

```
alimentador_bd/
├── config/
│   ├── .env.example          # Template for credentials
│   └── settings.toml         # Configuration
├── scripts/                  # Python modules
│   ├── cli.py               # CLI interface (Typer)
│   ├── stream.py            # Streaming engine
│   ├── seed.py              # Initial data population
│   ├── db_init.py           # Database connection
│   ├── data_gen.py          # Data generation (Faker)
│   ├── validators.py        # FK validation cache
│   └── reset.py             # Reset orchestration
├── sql/                      # SQL scripts
│   ├── 01_schema.sql        # Table definitions
│   ├── 02_indexes.sql       # Indexes
│   ├── 03_seed-lookups.sql  # Initial data
│   └── 99_drop_all.sql      # Cleanup
├── logs/                     # Runtime logs
├── Makefile                  # Build automation
├── Dockerfile                # Container image
├── docker-compose.yml        # Local stack
├── pyproject.toml           # Python config
├── requirements.txt         # Dependencies
├── README.md                # This file
├── GUIDE.md                 # User guide (Portuguese)
├── ARCHITECTURE.md          # Technical design
├── DEPLOYMENT.md            # Production setup
├── CONTRIBUTING.md          # Contribution guide
├── CHANGELOG.md             # Version history
└── LICENSE                  # MIT license
```

---

## 🐳 Docker Deployment

### Run Locally

```bash
# Start PostgreSQL (Docker)
docker-compose up -d postgres

# Initialize from host
make init
make seed

# Stream
make stream
```

### Build Image

```bash
docker build -t alimentador-bd:1.0.0 .

docker run --rm \
  -e PG_HOST=localhost \
  -e PG_USER=app \
  -e PG_PASSWORD=app123 \
  -e PG_DATABASE=teste_pacientes \
  -v ./logs:/app/logs \
  alimentador-bd:1.0.0 \
  python -m scripts.cli stream
```

---

## ☁️ Production Deployment

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed guides:
- ✅ AWS EC2 + RDS setup
- ✅ Kubernetes deployment
- ✅ Monitoring and scaling
- ✅ Backup and recovery
- ✅ Security best practices

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [**README.md**](README.md) | Overview, quick start, schema (this file) |
| [**GUIDE.md**](GUIDE.md) | Complete user manual in Portuguese 🇧🇷 |
| [**ARCHITECTURE.md**](ARCHITECTURE.md) | Technical design and data flow |
| [**DEPLOYMENT.md**](DEPLOYMENT.md) | Production setup (AWS, K8s, Docker) |
| [**CONTRIBUTING.md**](CONTRIBUTING.md) | How to contribute, dev setup |
| [**CHANGELOG.md**](CHANGELOG.md) | Version history and roadmap |

---

## 🐛 Troubleshooting

### Connection Error: "connection refused"

```bash
# Check PostgreSQL is running
psql -U postgres -h localhost -c "SELECT 1"

# Verify credentials in config/.env
cat config/.env | grep PG_
```

### IntegrityError: "duplicate key value"

This is **expected and handled gracefully**. The simulator skips duplicates and logs them:

```bash
grep "IntegrityError" logs/app.log
```

### Stream not starting

```bash
# Verify database is initialized
make init
make seed
make counts

# Check logs
tail -20 logs/app.log
```

### Slow inserts

```bash
# Check disk space and PostgreSQL performance
df -h
psql -U app -d teste_pacientes -c "SELECT * FROM pg_stat_user_tables"

# Reduce batch size if needed
BATCH_SIZE=25 make stream
```

---

## 🤝 Contributing

We welcome contributions! See [**CONTRIBUTING.md**](CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Testing procedures
- Pull request workflow

Quick start for contributors:

```bash
git clone https://github.com/yourusername/alimentador-bd.git
cd alimentador-bd
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make init && make seed
make stream  # Test it works
```

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Seed time | <2 seconds |
| Initial records | ~13,000 |
| Stream rate | 1 op / 2s |
| Batch size | 50 records |
| Insert ops | 70% |
| Update ops | 30% |
| Throughput | 200+ ops/min |
| Memory usage | ~256 MB |
| CPU usage | Low (<1 core) |

---

## 📝 License

MIT License - See [LICENSE](LICENSE) for details

**Copyright © 2025 Henrique Ferreira**

---

## 📞 Support

- **Documentation**: See [GUIDE.md](GUIDE.md) (Portuguese) or [ARCHITECTURE.md](ARCHITECTURE.md) (English)
- **Issues**: Report bugs using GitHub issue templates
- **Discussions**: Ask questions in GitHub Discussions
- **Email**: [your-email@example.com]

---

## 🎉 Next Steps

1. **Read** [GUIDE.md](GUIDE.md) (Portuguese user guide) or this README
2. **Setup** with `make install && make init && make seed`
3. **Run** with `make stream`
4. **Monitor** with `make counts` and `tail -f logs/app.log`
5. **Deploy** using [DEPLOYMENT.md](DEPLOYMENT.md) for production

---

**Version**: 1.0.0 | **Status**: Production Ready ✅ | **License**: MIT
