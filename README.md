# 💰 Expense Tracker

A production-grade DevOps project built on a Flask expense tracking application.

## Tech Stack
- **Backend** — Python / Flask
- **Database** — PostgreSQL
- **Containerization** — Docker + docker-compose
- **CI/CD** — GitHub Actions (coming soon)
- **Cloud** — AWS EC2 (coming soon)
- **IaC** — Terraform (coming soon)
- **Orchestration** — Kubernetes (coming soon)
- **Monitoring** — Prometheus + Grafana (coming soon)

## How to Run

### Locally
```bash
source venv/bin/activate
python app.py
```

### With Docker
```bash
docker-compose up --build
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/expenses` | Add expense |
| GET | `/expenses` | View all expenses |
| DELETE | `/expenses/<id>` | Delete expense |
| GET | `/expenses/summary/<year>/<month>` | Monthly summary |

## Project Roadmap
| Stage | What | Status |
|-------|------|--------|
| 1 | Flask + PostgreSQL app | ✅ Done |
| 2 | Docker + docker-compose | ✅ Done |
| 3 | GitHub + branch protection | ✅ Done |
| 4 | CI/CD with GitHub Actions | 🔄 Next |
| 5 | AWS EC2 deployment | ⬜ Pending |
| 6 | Terraform | ⬜ Pending |
| 7 | Kubernetes | ⬜ Pending |
| 8 | Prometheus + Grafana | ⬜ Pending |
