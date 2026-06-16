# ═══════════════════════════════════════════════════════════
# Multi-stage Dockerfile dla FastAPI (Production)
# ═══════════════════════════════════════════════════════════
#
# Dwa etapy:
# 1. builder - instalacja dependencies
# 2. runtime - lekki obraz do uruchomienia
#
# Build:
# docker build -t fastapi-app .
#
# Run:
# docker run -p 8000:8000 fastapi-app
# ═══════════════════════════════════════════════════════════

# ───────────────────────────────────────────────────────────
# Stage 1: Builder (instalacja dependencies)
# ───────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Zainstaluj build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Skopiuj requirements i zainstaluj
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# ───────────────────────────────────────────────────────────
# Stage 2: Runtime (production image)
# ───────────────────────────────────────────────────────────
FROM python:3.11-slim

# Metadane
LABEL maintainer="your-email@example.com"
LABEL description="FastAPI Production Container"

# Zmienne środowiskowe
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/appuser/.local/bin:$PATH

WORKDIR /app

# Skopiuj zainstalowane packages z buildera
COPY --from=builder /root/.local /home/appuser/.local

# Skopiuj kod aplikacji
COPY main.py .

# Utwórz non-root user (security best practice)
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Przełącz się na non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Expose port
EXPOSE 8000

# Uruchom uvicorn
# --host 0.0.0.0 - listen na wszystkich interfejsach
# --port 8000 - port aplikacji
# --workers 2 - 2 worker processes (CPU cores * 2 + 1)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

# ═══════════════════════════════════════════════════════════
# Notatki
# ═══════════════════════════════════════════════════════════
#
# Multi-stage build:
# - Stage 1 (builder): instalacja dependencies (duży obraz)
# - Stage 2 (runtime): tylko runtime + kod (mały obraz)
# - Finalny obraz ~150MB zamiast ~500MB
#
# Non-root user:
# - appuser (uid 1000) zamiast root
# - Security best practice
# - Uniemożliwia exploity z root access
#
# Health check:
# - Docker sprawdza czy app działa
# - Interval: co 30s
# - Timeout: 10s na response
# - Retries: 3 próby zanim uzna za unhealthy
#
# Workers:
# - 2 workers = obsługa 2 requestów jednocześnie
# - Dla CPU-bound: CPU cores
# - Dla I/O-bound: CPU cores * 2 + 1
# - W docker-compose można skalować replicas
#
# ═══════════════════════════════════════════════════════════