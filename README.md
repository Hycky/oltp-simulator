# OLTP Hospital Simulator

Realistic hospital database simulator with continuous INSERT/UPDATE operations for CDC (Change Data Capture).

**📖 [Quick Start](QUICK_START.md)** | **🏗️ [Architecture](ARCHITECTURE.md)** | **🚀 [Deployment](DEPLOYMENT.md)**

## Overview

This project implements a realistic hospital event simulator (OLTP) that continuously inserts and updates data in PostgreSQL, generating a realistic stream of changes for data pipeline validation.

### Features

- ✅ **7 OLTP Tables**: patients, doctors, insurance plans, appointments, exams, hospital stays
- ✅ **Realistic Operations**: 70% INSERT, 30% UPDATE (CDC-focused, no DELETEs)
- ✅ **CDC-Ready**: Optimized schema with triggers, indexes, natural keys
- ✅ **Resilient**: Automatic reconnection with exponential backoff
- ✅ **Observable**: Detailed per-operation logging
- ✅ **Configurable**: Environment variables for customization
- ✅ **Docker Support**: docker-compose for local development

## Getting Started

### 🚀 5-Minute Setup

```bash
# Clone
git clone https://github.com/yourusername/alimentador-bd.git
cd alimentador-bd

# Setup (local)
make install
make init
make seed
make stream
```

**Or with Docker:**
```bash
docker-compose up -d postgres
make init && make seed && make stream
```

→ See [QUICK_START.md](QUICK_START.md) for detailed instructions

## Documentation

| Document | Purpose | Language |
|----------|---------|----------|
| [QUICK_START.md](QUICK_START.md) | Get running in 5 minutes | English |
| [GUIDE.md](GUIDE.md) | Complete user guide & troubleshooting | Portuguese |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Technical design & data flow | English |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Development setup & contributing | English |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment (AWS, K8s, Docker) | English |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines | English |
| [CHANGELOG.md](CHANGELOG.md) | Version history | English |

## Schema Overview

### 7 Tables with Relationships

```
Patients (2k) ─────┬──→ Appointments (4k+)
                   ├──→ Lab Exams (3.5k+)
                   ├──→ Hospital Stays (1.2k+)
                   └─┐
                     ├──→ Insurance Plan (12)
                     └──→ Doctors (200)
```

All tables feature:
- BIGSERIAL primary keys
- Natural keys (CPF, CRM, CNPJ) with UNIQUE constraints
- Cascading foreign keys (UPDATE CASCADE, DELETE RESTRICT)
- Automatic `updated_at` triggers
- Strategic B-tree indexes

### Table Definitions

| Table | Records | Purpose |
|-------|---------|---------|
| `pacientes` | 2,000 | Patients with demographics |
| `medicos` | 200 | Doctors with specialties |
| `convenios` | 12 | Insurance/payment plans |
| `pacientes_convenios` | 2,500+ | N:M patient-plan relationships |
| `consultas` | 4,000+ | Doctor appointments |
| `exames` | 3,500+ | Lab tests and results |
| `internacoes` | 1,200+ | Hospital admissions |

## Operations

### INSERT (70% of events)

- New patient
- New appointment
- New lab exam
- New hospital stay

### UPDATE (30% of events)

- Patient phone/address change
- Appointment status change (scheduled → completed)
- Exam result updates
- Hospital stay discharge date

## Configuration

```env
# Database
PG_HOST=localhost
PG_PORT=5432
PG_USER=app
PG_PASSWORD=app123
PG_DATABASE=teste_pacientes

# Stream
STREAM_INTERVAL_SECONDS=2
BATCH_SIZE=50
MAX_JITTER_MS=400

# Seed Volumes
SEED_PACIENTES=2000
SEED_MEDICOS=200
SEED_CONVENIOS=12
SEED_CONSULTAS=4000
SEED_EXAMES=3500
SEED_INTERNACOES=1200

# Logging
LOG_LEVEL=INFO
```

See [QUICK_START.md](QUICK_START.md#setup-local-or-docker) for setup instructions.

## Available Commands

```bash
make install          # Setup Python environment
make init             # Create schema & indexes
make seed             # Populate initial data (~13k records)
make stream           # Start continuous operation
make reset            # Drop + recreate + seed
make counts           # Show record counts
make fmt              # Format code (ruff + black)
make lint             # Check code (ruff)
make clean            # Remove venv + cache
```

## Project Structure

```
├── .github/                # Issue templates
├── config/
│   ├── .env.example       # Configuration template
│   └── settings.toml      # TOML settings
├── scripts/
│   ├── cli.py             # CLI entry point
│   ├── stream.py          # Streaming engine
│   ├── seed.py            # Data population
│   ├── db_init.py         # Database init
│   ├── data_gen.py        # Data generation (Faker)
│   ├── validators.py      # FK validation & cache
│   └── reset.py           # Reset orchestration
├── sql/
│   ├── 01_schema.sql      # Tables & triggers
│   ├── 02_indexes.sql     # B-tree indexes
│   ├── 03_seed-lookups.sql # Initial data
│   └── 99_drop_all.sql    # Cleanup
├── logs/                  # Generated at runtime
├── Makefile               # Command shortcuts
├── pyproject.toml         # Python packaging
├── requirements.txt       # Dependencies
├── docker-compose.yml     # Docker setup
├── Dockerfile             # Container image
└── QUICK_START.md         # ← Start here
```

## Data Generation

Uses **Faker with pt_BR locale** for realistic Brazilian data:

- **CPF**: `123.456.789-00` (validated)
- **CRM**: `123456SP` (doctor license + state)
- **CNPJ**: `12.345.678/0001-99` (validated)
- **Names**: Portuguese names (João, Maria, etc.)
- **Addresses**: Real Brazilian locations

Ensures:
- Unique natural keys (no duplicates)
- Realistic distributions
- Temporal coherence (appointment dates after patient registration)
- Referential integrity (all FKs valid)

## Logging

Logs are written to `/logs` with rotation:

```bash
tail -f logs/app.log        # Main log
grep "ERROR" logs/*.log     # Errors only
watch -n 1 'make counts'    # Monitor growth
```

## Performance

| Operation | Time | Volume |
|-----------|------|--------|
| Init DB | 3-5s | Schema + 9 indexes |
| Seed | 2-5m | ~13,000 records |
| Stream (1 event) | 100-500ms | 1 operation |
| Stream (1 hour) | 1h | ~2,000 operations |
| Stream (1 day) | 1d | ~50,000 operations |

## CDC & Debezium

This simulator is optimized for Debezium testing:

✅ **Debezium-Ready Features**:
- Unique primary keys on all tables
- Natural keys (CPF, CRM, CNPJ)
- Audit columns (`created_at`, `updated_at`)
- Updated_at triggers on all changes
- Strategic indexes for WAL scanning

### Debezium Configuration Example

```json
{
  "name": "alimentador-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "localhost",
    "database.port": 5432,
    "database.user": "app",
    "database.password": "app123",
    "database.dbname": "teste_pacientes",
    "table.include.list": "public.*",
    "publication.name": "alimentador_pub",
    "plugin.name": "pgoutput",
    "snapshot.mode": "initial"
  }
}
```

## Troubleshooting

### Connection Issues

```bash
python test_connection.py    # Test PostgreSQL connection
```

### Slow Performance

```bash
# Check indexes
psql -c "SELECT * FROM pg_stat_user_indexes;"

# Reduce interval
STREAM_INTERVAL_SECONDS=0.5 make stream
```

### Module Errors

```bash
pip install -r requirements.txt
```

See [GUIDE.md](GUIDE.md#troubleshooting) for more troubleshooting.

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for:
- Setting up a development environment
- Code style guidelines
- Adding new features
- Running tests

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Deployment

For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md) with examples for:
- AWS EC2 + RDS
- Kubernetes
- Docker Compose
- Self-hosted PostgreSQL

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- 📖 Documentation: See links above
- 🐛 Issues: Use GitHub issue templates
- 💬 Discussions: Start a GitHub discussion
- 📧 Email: maintainer@example.com

---

**Status**: ✅ Production Ready (v1.0.0)

**Maintained by**: [Contributors](CONTRIBUTING.md#contributors)

**Last Updated**: November 2025

SEED_PACIENTES_CONVENIOS=2500
```

## Comandos Disponíveis

```bash
make init       # Inicializa schema
make seed       # Popula dados iniciais
make stream     # Inicia streaming contínuo
make reset      # Drop + recreate + seed (cuidado!)
make counts     # Exibe contagens por tabela
make fmt        # Formata código
make lint       # Verifica código
make clean      # Limpa cache e venv
```

## Schema

### Tabelas Principais

- **pacientes** (2000 seed): CPF, nome, telefone, endereço
- **medicos** (200 seed): CRM, especialidade
- **convenios** (12 seed): CNPJ, tipo, cobertura
- **consultas** (4000 seed): paciente, médico, status
- **exames** (3500 seed): paciente, tipo, resultado
- **internacoes** (1200 seed): paciente, entrada/saída
- **pacientes_convenios** (2500 seed): relacionamento N:N

### Características

- PK: BIGSERIAL em todas as tabelas
- UKs: CPF, CRM, CNPJ (chaves naturais)
- FKs: ON UPDATE CASCADE, ON DELETE RESTRICT
- Triggers: `updated_at` automático em UPDATE
- Índices: Estratégicos em CPF, CRM, FK targets e datas

## Operações de Stream

### INSERT (70%)

- `insert_paciente`: Novo paciente com Faker pt_BR
- `insert_consulta`: Nova consulta com status válido
- `insert_exame`: Novo exame
- `insert_internacao`: Nova internação

### UPDATE (30%)

- `update_paciente`: Telefone ou endereço
- `update_consulta`: Status (agendada → realizada/cancelada/faltou)
- `update_exame`: Resultado (Normal/Alterado/Positivo/Negativo/Pendente)
- `update_internacao`: data_saida (alta)

## Logs

```
[    1] INSERT     consulta | INSERT:    1 | UPDATE:    0
[    2] INSERT     consulta | INSERT:    2 | UPDATE:    0
[    3] UPDATE     paciente | INSERT:    2 | UPDATE:    1
```

Formato: `[ciclo] TIPO tabela | INSERT total | UPDATE total`

## Troubleshooting

### "Banco não encontrado"

```bash
# Criar banco manualmente
psql -U postgres -c "CREATE DATABASE teste_pacientes"
```

### "Connection refused"

Verificar credenciais em `.env` e status do PostgreSQL:

```bash
pg_isready -h localhost -p 5432
```

### Limpar Cache

```bash
find . -type d -name __pycache__ -exec rm -rf {} +
rm -rf .venv logs/*.log
```

## Estrutura

```
.
├── config/
│   ├── .env                 # Credenciais (git-ignored)
│   ├── .env.example         # Template
│   └── settings.toml        # Configurações
├── sql/
│   ├── 01_schema.sql        # Schema principal
│   ├── 02_indexes.sql       # Índices
│   ├── 03_seed-lookups.sql  # Dados iniciais
│   └── 99_drop_all.sql      # Limpeza
├── scripts/
│   ├── cli.py               # CLI Typer
│   ├── db_init.py           # Inicialização
│   ├── seed.py              # Semeadura
│   ├── stream.py            # Streaming contínuo
│   ├── data_gen.py          # Geradores Faker
│   ├── validators.py        # Validações
│   └── reset.py             # Reset total
├── logs/                    # Logs em runtime
├── requirements.txt         # Dependências
├── Makefile                 # Atalhos
└── README.md               # Este arquivo
```

## Para Debezium/CDC

Este simulador é otimizado para captura via Debezium:

1. Habilitar logical replication no PostgreSQL
2. Criar publication em `teste_pacientes`
3. Configurar Debezium PostgreSQL Connector com:
   - `database.server.name`: `alimentador_bd`
   - `database.dbname`: `teste_pacientes`
   - `table.include.list`: `public.*`

Exemplo:

```json
{
  "name": "alimentador-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "localhost",
    "database.port": 5432,
    "database.user": "postgres",
    "database.password": "postgres",
    "database.dbname": "teste_pacientes",
    "database.server.name": "alimentador_bd",
    "plugin.name": "pgoutput"
  }
}
```

## Licença

MIT

## Autor

Developed for OLTP testing and CDC validation
