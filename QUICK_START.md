# Quick Start

Get the OLTP simulator running in 5 minutes.

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Git

## Setup (Local or Docker)

### Option 1: Local Installation (5 min)

```bash
# 1. Clone and enter project
git clone https://github.com/yourusername/alimentador-bd.git
cd alimentador-bd

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure database
cp config/.env.example config/.env
# Edit config/.env with your PostgreSQL credentials
nano config/.env

# 5. Initialize and seed
make init
make seed

# 6. Start streaming
make stream
```

### Option 2: Docker Compose (3 min)

```bash
# 1. Clone project
git clone https://github.com/yourusername/alimentador-bd.git
cd alimentador-bd

# 2. Start PostgreSQL
docker-compose up -d postgres

# 3. Wait for database
sleep 5

# 4. Initialize and seed
make init
make seed

# 5. Start streaming
make stream
```

**Optional**: View database with PgAdmin
```bash
docker-compose up -d pgadmin
# Access: http://localhost:5050 (admin@example.com / admin)
```

## What's Happening?

**Step 1: `make init`**
- Creates 7 OLTP tables with relationships
- Adds 9 strategic indexes
- Loads 2 initial insurance plans
- Time: ~3-5 seconds

**Step 2: `make seed`**
- Populates ~13,000 initial records
- Generates realistic Brazilian data (Faker pt_BR)
- Validates all foreign keys
- Time: ~2-5 minutes (depending on network)

**Step 3: `make stream`**
- Starts continuous INSERT/UPDATE operations
- 70% INSERT, 30% UPDATE operations
- Real-time logging to console and file
- **Stop with**: `Ctrl+C`

## Monitor Progress

In a separate terminal:

```bash
# See record counts grow in real-time
watch -n 2 'make counts'
```

## Next Steps

### Local Development
- Read [GUIDE.md](GUIDE.md) for comprehensive documentation (Portuguese)
- Check [README.md](README.md) for features and schema overview
- Review [DEVELOPMENT.md](DEVELOPMENT.md) for contribution guidelines

### Production Deployment
- Follow [DEPLOYMENT.md](DEPLOYMENT.md) for AWS, Kubernetes, or Docker production setup
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details

### CDC Testing with Debezium
- Stream is generating CDC-ready events
- Configure Debezium to capture PostgreSQL WAL
- Validate CDC sync with destination system

## Common Issues

**"Connection refused"**
```bash
# Test connection
python test_connection.py

# Verify PostgreSQL is running
psql -U app -h localhost -d postgres -c "SELECT 1"
```

**"Module not found"**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**"Database doesn't exist"**
```bash
# Create it (local only)
createdb -U postgres test_db

# Or update config/.env to existing database
PG_DATABASE=your_existing_db
```

## Commands Reference

```bash
make init          # Create schema
make seed          # Populate initial data
make stream        # Start streaming
make reset         # Drop and recreate everything
make counts        # Show record counts
make fmt           # Format code
make lint          # Check code quality
make clean         # Remove venv and cache
```

## What Gets Generated?

The simulator creates realistic hospital OLTP data:

| Table | Records | Frequency |
|-------|---------|-----------|
| Patients | 2,000 | +1 every 10 stream cycles |
| Doctors | 200 | (seeded once) |
| Insurance Plans | 12 | (seeded once) |
| Appointments | 4,000+ | +1 every 3 stream cycles |
| Lab Tests | 3,500+ | +1 every 5 stream cycles |
| Hospital Stays | 1,200+ | +1 every 8 stream cycles |

## File Structure

```
├── config/           # Configuration (.env, settings.toml)
├── sql/              # Database schema SQL scripts
├── scripts/          # Python modules (CLI, stream, seed, etc.)
├── logs/             # Runtime logs (auto-generated)
├── Makefile          # Command shortcuts
├── requirements.txt  # Python dependencies
├── docker-compose.yml # For Docker setup
└── docs/             # Documentation (README, GUIDE, ARCHITECTURE, etc.)
```

## Documentation

| File | Purpose | Language |
|------|---------|----------|
| [README.md](README.md) | Feature overview & schema | English |
| [GUIDE.md](GUIDE.md) | Complete user guide | Portuguese |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Development setup | English |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Technical architecture | English |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment | English |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines | English |

## Support

- 📖 Check the relevant documentation file above
- 🐛 Found a bug? Open an issue with reproduction steps
- 💡 Have a feature idea? Start a discussion
- 📝 See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines

---

**Ready?** Start with `make init && make seed && make stream` 🚀
