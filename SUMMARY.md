# 📊 Project Summary & Documentation Structure

## Repository Overview

```
alimentador-bd/
├── 📖 Documentation (8 files, ~3,100 lines)
├── 🐍 Python Code (7 modules, ~1,200 lines)
├── 🗄️ SQL Scripts (4 files, ~250 lines)
├── 🐳 Docker Support (docker-compose.yml, Dockerfile)
├── ⚙️ Configuration (Makefile, pyproject.toml, requirements.txt)
└── 🔧 Development (.gitignore, .github templates)
```

## Documentation Map

### 🚀 Getting Started

```
Start Here
    ↓
QUICK_START.md (5 min)
    ├─ Local setup
    ├─ Docker setup
    ├─ Monitor progress
    └─ Common issues
```

### 📚 Main Documentation

| File | Size | Language | Purpose |
|------|------|----------|---------|
| **README.md** | 458 lines | English | Overview + quick reference |
| **GUIDE.md** | 739 lines | 🇵🇹 Portuguese | Complete user manual |
| **QUICK_START.md** | 217 lines | English | 5-minute setup |
| **ARCHITECTURE.md** | 350 lines | English | Technical design |
| **DEVELOPMENT.md** | 420 lines | English | Developer guide |
| **DEPLOYMENT.md** | 420 lines | English | Production setup |
| **CONTRIBUTING.md** | 200 lines | English | Contribution guidelines |
| **CHANGELOG.md** | 290 lines | English | Version history |
| **INDEX.md** | 400 lines | English | Documentation index |

### 🎯 Quick Navigation

**By Role:**
- 👤 **End User** → QUICK_START.md + GUIDE.md
- 👨‍💻 **Developer** → ARCHITECTURE.md + DEVELOPMENT.md
- 🔧 **DevOps** → DEPLOYMENT.md
- 📝 **Contributor** → CONTRIBUTING.md

**By Task:**
- ❓ "How do I get started?" → QUICK_START.md
- ❓ "What does it do?" → README.md
- ❓ "How does it work?" → ARCHITECTURE.md
- ❓ "I want to contribute" → CONTRIBUTING.md
- ❓ "Production setup?" → DEPLOYMENT.md
- ❓ "Troubleshoot?" → GUIDE.md (section 9)

## Code Structure

```
scripts/
├── cli.py           (Typer CLI entry point)
├── stream.py        (Continuous INSERT/UPDATE operations)
├── seed.py          (Initial data population)
├── db_init.py       (Database connection & init)
├── data_gen.py      (Faker generators for pt_BR)
├── validators.py    (FK validation + LRU cache)
├── reset.py         (Full reset orchestration)
└── __init__.py

sql/
├── 01_schema.sql    (7 OLTP tables)
├── 02_indexes.sql   (9 strategic indexes)
├── 03_seed-lookups.sql (Initial data)
└── 99_drop_all.sql  (Cleanup)

config/
├── .env             (Credentials - git-ignored)
├── .env.example     (Template - safe to commit)
└── settings.toml    (TOML configuration)
```

## Key Features

✅ **7 OLTP Tables** (13k+ initial records)
- pacientes (2k)
- medicos (200)
- convenios (12)
- pacientes_convenios (2.5k)
- consultas (4k)
- exames (3.5k)
- internacoes (1.2k)

✅ **Realistic Operations**
- 70% INSERT (new patients, appointments, exams, stays)
- 30% UPDATE (status changes, address updates)
- 100% CDC-compatible (no deletes)

✅ **Resilient Design**
- Automatic reconnection with exponential backoff
- Graceful shutdown on Ctrl+C
- Transaction management with rollback
- LRU cache (512 entries) for FK validation

✅ **Observable**
- Per-cycle logging with operation counts
- File rotation (7 days retention)
- Error tracking and reporting
- Real-time monitoring via `make counts`

## Dependencies

**Runtime** (5 packages):
- psycopg2-binary (PostgreSQL driver)
- python-dotenv (Environment variables)
- typer (CLI framework)
- faker (Data generation)
- pydantic (Validation)

**Development** (optional):
- ruff (Code linter)
- black (Code formatter)
- pytest (Testing)
- mypy (Type checking)

## Performance Metrics

| Operation | Time | Volume |
|-----------|------|--------|
| Setup (.venv) | ~30s | Python environment |
| Init DB | ~3-5s | Schema creation |
| Seed | ~2-5m | 13k records |
| Stream (1h) | 1h | ~2,000 operations |
| Stream (1d) | 1d | ~50,000 operations |

## Installation Paths

### Path 1: Docker Compose (Easiest)
```bash
docker-compose up -d postgres
make init && make seed && make stream
```
⏱️ **Total Time**: ~10 minutes

### Path 2: Local Python (Most Flexible)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make init && make seed && make stream
```
⏱️ **Total Time**: ~5 minutes (setup) + 2-5 minutes (seed)

### Path 3: Production (AWS/K8s)
See [DEPLOYMENT.md](DEPLOYMENT.md)
⏱️ **Total Time**: 20-60 minutes (infrastructure setup)

## Command Reference

| Command | Purpose | Time |
|---------|---------|------|
| `make install` | Setup venv | ~30s |
| `make init` | Create schema | ~3-5s |
| `make seed` | Populate data | ~2-5m |
| `make stream` | Start streaming | ∞ |
| `make reset` | Full reset | ~10s |
| `make counts` | Show statistics | ~1s |
| `make fmt` | Format code | ~2s |
| `make lint` | Check code | ~2s |

## What Gets Logged?

**Stream Output** (per cycle):
```
[Cycle 50] INSERT consulta | Total INSERTs: 1,250 | Total UPDATEs: 300
[Cycle 51] UPDATE paciente | Total INSERTs: 1,250 | Total UPDATEs: 301
```

**Log Files** (in `/logs`):
- `app.log` - All operations
- `stream.log` - Stream-specific
- `errors.log` - Errors only

## CDC Compatibility

✅ **Debezium-Ready**:
- BIGSERIAL primary keys ✓
- Natural keys (CPF, CRM, CNPJ) ✓
- Audit columns (created_at, updated_at) ✓
- Automatic triggers ✓
- Strategic indexes ✓
- Cascading FKs ✓

✅ **Tested With**:
- PostgreSQL 14+ ✓
- PostgreSQL 16 (current) ✓
- Debezium 2.x ✓

## Configuration Options

**Core**:
```env
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=teste_pacientes
```

**Streaming**:
```env
STREAM_INTERVAL_SECONDS=2
BATCH_SIZE=50
MAX_JITTER_MS=400
```

**Volumes**:
```env
SEED_PACIENTES=2000
SEED_MEDICOS=200
SEED_CONVENIOS=12
SEED_CONSULTAS=4000
SEED_EXAMES=3500
SEED_INTERNACOES=1200
```

## Troubleshooting at a Glance

| Issue | Check | Fix |
|-------|-------|-----|
| Connection refused | `python test_connection.py` | Update .env credentials |
| Slow seed | Network latency | Try `BATCH_SIZE=100` |
| Stream stops | `tail logs/app.log` | Restart: `make stream` |
| Module not found | `pip list` | `pip install -r requirements.txt` |

## File Statistics

```
Total Files: 30+
├─ Documentation: 9 files (~3,100 lines)
├─ Python: 8 files (~1,200 lines)
├─ SQL: 4 files (~250 lines)
├─ Config: 5 files (~100 lines)
└─ Build: 4 files (Makefile, Dockerfile, compose, etc.)

Code Distribution:
├─ Stream logic: 30%
├─ Data generation: 25%
├─ Database init: 20%
├─ Validation: 15%
└─ CLI/Utilities: 10%
```

## Version & Status

```
Project Version: 1.0.0
Python: 3.11+
PostgreSQL: 14+
License: MIT
Status: ✅ Production Ready
Last Updated: November 2025
```

## Support Matrix

| Platform | Status | Notes |
|----------|--------|-------|
| Linux | ✅ Full | Ubuntu/Debian tested |
| macOS | ✅ Full | Intel/ARM tested |
| Windows | ⚠️ Partial | WSL2 recommended |
| Docker | ✅ Full | docker-compose included |
| Kubernetes | ✅ Full | YAML templates in DEPLOYMENT.md |
| AWS | ✅ Full | EC2 + RDS setup guide |

## Next Actions

1. **First Time?**
   - Go to → [QUICK_START.md](QUICK_START.md)
   - Read → [README.md](README.md)

2. **Want Details?**
   - Portuguese → [GUIDE.md](GUIDE.md)
   - Technical → [ARCHITECTURE.md](ARCHITECTURE.md)
   - Development → [DEVELOPMENT.md](DEVELOPMENT.md)

3. **Production Ready?**
   - Read → [DEPLOYMENT.md](DEPLOYMENT.md)
   - Review → Security checklist

4. **Want to Help?**
   - Read → [CONTRIBUTING.md](CONTRIBUTING.md)
   - Check → GitHub issues

---

**Welcome to alimentador-bd!** 🚀

**Start with**: `git clone ... && cd alimentador-bd && cat QUICK_START.md`
