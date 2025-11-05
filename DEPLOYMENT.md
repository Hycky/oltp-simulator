# Deployment Guide

This guide covers deploying the OLTP simulator in **production environments**.

> **For local development and testing**, see [README.md](README.md) or [GUIDE.md](GUIDE.md).

## Docker Deployment

### Single Container

### Build Image

```bash
docker build -t alimentador-bd:1.0.0 .
```

### Run Streaming

```bash
docker run --rm \
  --network host \
  -e PG_HOST=localhost \
  -e PG_PORT=5432 \
  -e PG_USER=app \
  -e PG_PASSWORD=app123 \
  -e PG_DATABASE=teste_pacientes \
  -e STREAM_INTERVAL_SECONDS=2 \
  -v ./logs:/app/logs \
  alimentador-bd:1.0.0 \
  python -m scripts.cli stream
```

### With External Database

```bash
docker run --rm \
  -e PG_HOST=10.42.88.67 \
  -e PG_PORT=5441 \
  -e PG_USER=app \
  -e PG_PASSWORD=app123 \
  -e PG_DATABASE=teste_pacientes \
  -v ./logs:/app/logs \
  alimentador-bd:1.0.0 \
  python -m scripts.cli stream
```

## Kubernetes Deployment

### Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: alimentador-simulator
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: alimentador-simulator
  template:
    metadata:
      labels:
        app: alimentador-simulator
    spec:
      containers:
      - name: simulator
        image: alimentador-bd:1.0.0
        imagePullPolicy: IfNotPresent
        env:
        - name: PG_HOST
          valueFrom:
            configMapKeyRef:
              name: alimentador-config
              key: db_host
        - name: PG_PORT
          valueFrom:
            configMapKeyRef:
              name: alimentador-config
              key: db_port
        - name: PG_USER
          valueFrom:
            secretKeyRef:
              name: alimentador-secrets
              key: db_user
        - name: PG_PASSWORD
          valueFrom:
            secretKeyRef:
              name: alimentador-secrets
              key: db_password
        - name: PG_DATABASE
          valueFrom:
            configMapKeyRef:
              name: alimentador-config
              key: db_name
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: alimentador-config
              key: log_level
        volumeMounts:
        - name: logs
          mountPath: /app/logs
        livenessProbe:
          exec:
            command:
            - python
            - scripts/test_connection.py
          initialDelaySeconds: 30
          periodSeconds: 60
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
      volumes:
      - name: logs
        emptyDir: {}
```

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: alimentador-config
data:
  db_host: "postgres.default.svc.cluster.local"
  db_port: "5432"
  db_name: "teste_pacientes"
  log_level: "INFO"
```

### Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: alimentador-secrets
type: Opaque
stringData:
  db_user: "app"
  db_password: "app123"
```

Deploy with:

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment.yaml
```

## AWS - EC2 Instance

### Setup

1. **Launch EC2 Instance** (Ubuntu 22.04 LTS)
   - Instance type: t3.small (minimum)
   - Storage: 20 GB
   - Security group: Allow SSH (22), PostgreSQL client

2. **Install Dependencies**

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv git postgresql-client make
```

3. **Clone and Setup**

```bash
cd /opt
sudo git clone https://github.com/yourusername/alimentador-bd.git
cd alimentador-bd
sudo chown -R ubuntu:ubuntu .

python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. **Configure**

```bash
cp config/.env.example config/.env
# Edit config/.env with RDS endpoint, credentials
nano config/.env
```

5. **Start as Service**

Create `/etc/systemd/system/alimentador.service`:

```ini
[Unit]
Description=OLTP Hospital Simulator
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/alimentador-bd
Environment="PATH=/opt/alimentador-bd/.venv/bin"
ExecStart=/opt/alimentador-bd/.venv/bin/python -m scripts.cli stream
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable alimentador
sudo systemctl start alimentador
sudo systemctl status alimentador
```

Monitor logs:

```bash
sudo journalctl -u alimentador -f
```

## AWS - RDS Setup

### Create Database

```bash
aws rds create-db-instance \
  --db-instance-identifier alimentador-oltp \
  --db-instance-class db.t3.small \
  --engine postgres \
  --engine-version 16.1 \
  --master-username app \
  --master-user-password 'YourSecurePassword123!' \
  --allocated-storage 20 \
  --vpc-security-group-ids sg-12345678
```

### Connection

```bash
# From EC2
PGPASSWORD='YourSecurePassword123!' psql \
  -h alimentador-oltp.c9akciq32.us-east-1.rds.amazonaws.com \
  -U app \
  -d teste_pacientes
```

## Monitoring

### Prometheus Metrics (Future Enhancement)

For now, use PostgreSQL-native monitoring:

```bash
# Connect to database
psql -U app -d teste_pacientes

# View table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

# View transaction throughput
SELECT datname, xact_commit + xact_rollback as transactions_per_second
FROM pg_stat_database
WHERE datname = 'teste_pacientes';
```

### CloudWatch (AWS)

Configure CloudWatch agent to monitor:
- CPU usage
- Memory consumption
- Disk I/O
- Log streams

```bash
# Install CloudWatch agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i -E ./amazon-cloudwatch-agent.deb
```

## Scaling

### Multiple Instances

Run multiple simulators against same database:

```bash
# Instance 1
STREAM_INTERVAL_SECONDS=2 make stream

# Instance 2
STREAM_INTERVAL_SECONDS=3 make stream

# Instance 3
STREAM_INTERVAL_SECONDS=2.5 make stream
```

Database handles concurrent operations. Monitor:

```sql
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';
```

### Load Balancing

For Debezium replication across regions, consider:
- AWS DMS (Database Migration Service)
- Logical replication slots
- Multi-master PostgreSQL (pg_partman)

## Backup Strategy

### Automated Backups

```bash
# Daily backup to S3
0 2 * * * pg_dump -U app -h localhost teste_pacientes | gzip | aws s3 cp - s3://backups/$(date +\%Y\%m\%d).sql.gz
```

### Restore

```bash
aws s3 cp s3://backups/20250114.sql.gz - | gunzip | psql -U app -d teste_pacientes
```

## Troubleshooting

### Streaming Stops

1. Check logs:
```bash
tail -100 logs/app.log | grep -i error
```

2. Verify database:
```bash
make counts
```

3. Restart service:
```bash
sudo systemctl restart alimentador
```

### High Memory Usage

1. Reduce batch size:
```env
BATCH_SIZE=25
```

2. Check for connection leaks:
```sql
SELECT count(*) FROM pg_stat_activity;
```

### Slow Inserts

1. Check indexes:
```sql
SELECT * FROM pg_stat_user_indexes;
```

2. Verify vacuum is running:
```sql
SELECT * FROM pg_stat_user_tables;
```

## Security Checklist

- [ ] Environment variables not in git (.env in .gitignore)
- [ ] Database credentials in secrets manager (AWS Secrets Manager, HashiCorp Vault)
- [ ] Network restricted to necessary ports only
- [ ] SSL/TLS enabled for database connections
- [ ] Regular backups tested for recovery
- [ ] Logs monitored for suspicious activity
- [ ] Least privilege database user configured
- [ ] VPC/network segmentation in place

## Cost Optimization

### AWS Example (us-east-1)

- **t3.small EC2**: ~$16/month
- **RDS db.t3.small**: ~$28/month
- **Storage (20GB EBS)**: ~$2/month
- **Data transfer**: ~$0.09/GB (typically <5GB/month)

**Estimated cost**: ~$46/month for continuous operation

### Optimization Tips

1. Use `db.t3.micro` for testing (~$14/month)
2. Reduce storage if not needed
3. Use Reserved Instances for 1-year commitments (30% discount)
4. Monitor CloudWatch for unused resources
