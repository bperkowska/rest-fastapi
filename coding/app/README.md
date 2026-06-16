# 20 - Production Deployment Setup

**Nginx + Uvicorn + Docker Compose + Structured Logging**

---

## Quick Start

> **Uwaga:** Nginx słucha na porcie **8080** (zamiast 80), bo port 80 bywa zajęty systemowo.

```bash
# Uruchom
docker-compose up --build

# Test
curl http://localhost:8080/health
curl http://localhost:8080/tasks

# Logi (follow)
docker compose logs -f

# Zatrzymaj
docker compose down
```

---

## Struktura

```
20/
├── main.py                         # FastAPI app (CRUD + /health)
├── Dockerfile                      # Multi-stage build
├── docker-compose.yml              # nginx + app orchestration
├── requirements.txt                # Python deps
├── nginx/
│   ├── nginx.conf                 # Reverse proxy config
│   └── Dockerfile                 # Nginx image
├── logs/                           # JSON logs (volume)
│   ├── nginx/                     # access.log, error.log
│   └── app/
└── 20_production_deployment.ipynb # 📖 SZCZEGÓŁY TUTAJ!
```

---

## Kluczowe Koncepcje (szczegóły w notebooku)

1. **Nginx Reverse Proxy** - Load balancing, rate limiting, SSL termination
2. **Uvicorn Workers** - Multiple processes (2 workers = 2 równoległe requesty)
3. **Multi-stage Build** - Mniejszy obraz (~150MB vs ~500MB)
4. **Health Checks** - Docker wie czy app działa
5. **JSON Logs** - Structured logging dla łatwiejszego parsowania

---

## Debugging

```bash
# App nie startuje
docker compose logs app

# Nginx 502
docker compose restart app

# Wolne requesty
tail -f logs/nginx/access.log | jq '.request_time'

# Resource usage
docker stats
```

---

## 📖 Pełna Dokumentacja

**Wszystkie szczegóły w:** `20_production_deployment.ipynb`

- Dlaczego nginx?
- Jak działają workers?
- Co to multi-stage build?
- Przykłady debugowania
- Next steps (Gunicorn, SSL, Prometheus, Kubernetes)

---

## Development vs Production

| Aspekt | Development | Production (ten setup) |
|--------|-------------|------------------------|
| Proxy | Brak | ✅ Nginx |
| Workers | 1 | ✅ 2 |
| Logs | stdout | ✅ JSON files |
| Health checks | Brak | ✅ Docker + nginx |

---

**Pytania?** Zobacz notebook `20_production_deployment.ipynb`