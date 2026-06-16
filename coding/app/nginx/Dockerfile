# ═══════════════════════════════════════════════════════════
# Nginx Dockerfile
# ═══════════════════════════════════════════════════════════

FROM nginx:1.25-alpine

# Skopiuj custom config
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 (HTTP)
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

# ═══════════════════════════════════════════════════════════
# Notatki
# ═══════════════════════════════════════════════════════════
#
# alpine = mały obraz (~23MB vs ~140MB standard nginx)
# nginx:1.25 = stabilna wersja
#
# Health check:
# - wget --spider = fetch bez zapisywania
# - http://localhost/health = proxy do FastAPI health endpoint
#
# ═══════════════════════════════════════════════════════════