# OMNIMIND Deployment Guide

## Quick Start

```bash
git clone https://github.com/priyanshumishra610/OMNIMIND.git
cd OMNIMIND
cp .env.example .env
docker-compose up --build
```

- API: [localhost:8000/health](http://localhost:8000/health)
- Neo4j: [localhost:7474](http://localhost:7474)
- Prometheus: [localhost:9090](http://localhost:9090)

## Scaling Tips

- Use managed Neo4j or Pinecone for production.
- Deploy on cloud (AWS, GCP, Azure, etc). 