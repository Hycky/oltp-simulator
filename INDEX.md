# Documentation Index

Complete guide to all documentation in this project.

## 🚀 Getting Started

Start here if you're new to the project:

1. **[QUICK_START.md](QUICK_START.md)** (5 min)
   - Installation and first run
   - Docker Compose setup
   - Common issues

2. **[README.md](README.md)**
   - Project overview
   - Features and capabilities
   - Schema diagram
   - Basic configuration

## 📚 User Documentation

For daily usage:

- **[GUIDE.md](GUIDE.md)** 📖 Portuguese
  - Complete user manual
  - Step-by-step execution
  - All available commands
  - Data generation details
  - Troubleshooting guide
  - FAQ section

## 🏗️ Technical Documentation

For developers and architects:

- **[ARCHITECTURE.md](ARCHITECTURE.md)**
  - System design and layers
  - Module descriptions
  - Data flow diagrams
  - Performance optimizations
  - CDC compatibility

- **[DEVELOPMENT.md](DEVELOPMENT.md)**
  - Development environment setup
  - Code style guidelines
  - Contributing workflow
  - Adding new features
  - Testing procedures
  - Debugging tips

## 🚀 Production & Deployment

For operations and DevOps:

- **[DEPLOYMENT.md](DEPLOYMENT.md)**
  - Docker single container
  - Kubernetes deployment
  - AWS EC2 + RDS setup
  - Monitoring and metrics
  - Backup strategies
  - Security checklist
  - Cost optimization

## 📋 Project Management

For contributors:

- **[CONTRIBUTING.md](CONTRIBUTING.md)**
  - Contribution guidelines
  - Code style standards
  - Pull request workflow
  - Issue reporting
  - License information

- **[CHANGELOG.md](CHANGELOG.md)**
  - Version history
  - Release notes
  - Migration guides
  - Future roadmap

- **[LICENSE](LICENSE)**
  - MIT License text

## 📁 File Reference

### Configuration

| File | Purpose |
|------|---------|
| `config/.env` | Your credentials (git-ignored) |
| `config/.env.example` | Template for .env |
| `config/settings.toml` | TOML configuration |
| `pyproject.toml` | Python project metadata |
| `requirements.txt` | Dependencies |

### Source Code

| Directory | Purpose |
|-----------|---------|
| `scripts/` | Python modules |
| `sql/` | SQL migration scripts |
| `.github/` | GitHub issue templates |
| `logs/` | Generated at runtime |

### Build & Deployment

| File | Purpose |
|------|---------|
| `Makefile` | Command shortcuts |
| `Dockerfile` | Container image |
| `docker-compose.yml` | Local dev environment |
| `.gitignore` | Git exclusions |

## 🎯 Quick Navigation by Role

### 👤 End User

1. [QUICK_START.md](QUICK_START.md) - Get running
2. [README.md](README.md) - Understand features
3. [GUIDE.md](GUIDE.md) - Deep dive (Portuguese)
4. [QUICK_START.md#common-issues](QUICK_START.md) - Troubleshoot

### 👨‍💻 Developer

1. [QUICK_START.md](QUICK_START.md) - Setup
2. [ARCHITECTURE.md](ARCHITECTURE.md) - Understand design
3. [DEVELOPMENT.md](DEVELOPMENT.md) - Development workflow
4. [CONTRIBUTING.md](CONTRIBUTING.md) - Contribute

### 🔧 DevOps / SRE

1. [DEPLOYMENT.md](DEPLOYMENT.md) - Production setup
2. [ARCHITECTURE.md](ARCHITECTURE.md) - Technical details
3. [README.md#cdc--debezium](README.md#cdc--debezium) - CDC integration

### 📚 Technical Writer

1. [README.md](README.md) - Overview
2. [GUIDE.md](GUIDE.md) - User guide (Portuguese)
3. [ARCHITECTURE.md](ARCHITECTURE.md) - Technical details
4. [DEVELOPMENT.md](DEVELOPMENT.md) - Developer guide

## 📖 Language Support

| Document | Language |
|----------|----------|
| [GUIDE.md](GUIDE.md) | Portuguese (pt_BR) |
| All others | English |

**Note**: GUIDE.md is the primary Portuguese documentation. Use it for detailed, step-by-step instructions in Portuguese.

## 🔍 Finding Specific Information

### "How do I...?"

| Question | Document | Section |
|----------|----------|---------|
| Get started quickly? | [QUICK_START.md](QUICK_START.md) | Setup |
| Configure the system? | [README.md](README.md) | Configuration |
| Troubleshoot issues? | [GUIDE.md](GUIDE.md) | Troubleshooting |
| Deploy to production? | [DEPLOYMENT.md](DEPLOYMENT.md) | AWS / Kubernetes |
| Contribute code? | [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |
| Understand the architecture? | [ARCHITECTURE.md](ARCHITECTURE.md) | Overview |
| Set up development? | [DEVELOPMENT.md](DEVELOPMENT.md) | Setup |
| See version history? | [CHANGELOG.md](CHANGELOG.md) | Releases |

## 📞 Support Resources

**Problem**: Connection errors
- Check: [QUICK_START.md#common-issues](QUICK_START.md#common-issues)
- See: [GUIDE.md#troubleshooting](GUIDE.md#troubleshooting)

**Problem**: Slow performance
- Check: [README.md#performance](README.md#performance)
- See: [DEVELOPMENT.md#performance-profiling](DEVELOPMENT.md#performance-profiling)

**Problem**: Need to add a feature
- Read: [DEVELOPMENT.md#adding-features](DEVELOPMENT.md#adding-features)
- Follow: [CONTRIBUTING.md](CONTRIBUTING.md)

**Problem**: Want to report a bug
- Use GitHub issue templates in `.github/`
- Include: Version, Python version, PostgreSQL version

## 📊 Documentation Statistics

| Document | Lines | Purpose |
|----------|-------|---------|
| README.md | ~458 | Overview & reference |
| GUIDE.md | ~739 | Complete user manual |
| QUICK_START.md | ~217 | Fast onboarding |
| ARCHITECTURE.md | ~350 | Technical design |
| DEVELOPMENT.md | ~420 | Developer workflow |
| DEPLOYMENT.md | ~420 | Production setup |
| CONTRIBUTING.md | ~200 | Contribution guidelines |
| CHANGELOG.md | ~290 | Release history |

**Total**: ~3,100 lines of documentation

## 🎓 Learning Path

### Beginner

1. [QUICK_START.md](QUICK_START.md)
2. [README.md](README.md)
3. [GUIDE.md](GUIDE.md) - Sections 1-5

### Intermediate

1. [ARCHITECTURE.md](ARCHITECTURE.md)
2. [DEVELOPMENT.md](DEVELOPMENT.md)
3. [GUIDE.md](GUIDE.md) - Full document

### Advanced

1. [DEPLOYMENT.md](DEPLOYMENT.md)
2. Source code (scripts/ and sql/)
3. [CONTRIBUTING.md](CONTRIBUTING.md)

## 📝 Document Relationships

```
┌─ README.md (overview)
│  ├─ QUICK_START.md (fast track)
│  ├─ GUIDE.md (Portuguese reference)
│  └─ ARCHITECTURE.md (technical)
│
├─ DEVELOPMENT.md (contributors)
│  └─ CONTRIBUTING.md (guidelines)
│
├─ DEPLOYMENT.md (production)
│  └─ ARCHITECTURE.md (design)
│
└─ CHANGELOG.md (history)
```

## ✅ Documentation Checklist

Before opening a new issue:

- [ ] Read [QUICK_START.md](QUICK_START.md)
- [ ] Check [README.md#troubleshooting](README.md#troubleshooting)
- [ ] Search [GUIDE.md](GUIDE.md#troubleshooting)
- [ ] Review GitHub issue templates

## 🚀 Next Steps

Choose your path:

- **Just want to run it?** → Go to [QUICK_START.md](QUICK_START.md)
- **Need detailed guide?** → Go to [GUIDE.md](GUIDE.md)
- **Want to develop?** → Go to [DEVELOPMENT.md](DEVELOPMENT.md)
- **Deploying to prod?** → Go to [DEPLOYMENT.md](DEPLOYMENT.md)
- **Contributing code?** → Go to [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Last Updated**: November 2025

**Documentation Version**: 1.0.0 (aligns with project v1.0.0)
