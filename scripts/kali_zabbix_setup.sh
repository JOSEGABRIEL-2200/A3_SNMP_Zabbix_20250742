#!/usr/bin/env bash
# =====================================================================
# kali_zabbix_setup.sh - Asignacion 3: servidor Zabbix 7.0 LTS en Docker (Kali)
# Jose Gabriel Feliz Maria - 2025-0742
# Crea ~/zabbix-a3 con docker-compose.yml y .env (clave de PostgreSQL aleatoria,
# solo legible por el usuario) y levanta: PostgreSQL 16, Zabbix server y Zabbix web.
# La interfaz web queda solo en 127.0.0.1:8080 (se abre desde el mismo Kali).
# =====================================================================
set -euo pipefail

DIR="$HOME/zabbix-a3"
mkdir -p "$DIR"
cd "$DIR"

cat > docker-compose.yml <<'YML'
services:
  postgres:
    image: postgres:16-alpine
    container_name: zbx-postgres
    environment:
      POSTGRES_USER: zabbix
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: zabbix
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped

  zabbix-server:
    image: zabbix/zabbix-server-pgsql:alpine-7.0-latest
    container_name: zbx-server
    environment:
      DB_SERVER_HOST: postgres
      POSTGRES_USER: zabbix
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: zabbix
    depends_on:
      - postgres
    restart: unless-stopped

  zabbix-web:
    image: zabbix/zabbix-web-nginx-pgsql:alpine-7.0-latest
    container_name: zbx-web
    environment:
      ZBX_SERVER_HOST: zabbix-server
      DB_SERVER_HOST: postgres
      POSTGRES_USER: zabbix
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: zabbix
      PHP_TZ: America/Santo_Domingo
    ports:
      - "127.0.0.1:8080:8080"
    depends_on:
      - postgres
      - zabbix-server
    restart: unless-stopped

volumes:
  pgdata:
YML

# Clave aleatoria de la base de datos (no se publica: queda solo en este Kali)
if [ ! -f .env ]; then
  ( umask 077; printf 'DB_PASSWORD=%s\n' "$(openssl rand -hex 16)" > .env )
fi

sudo systemctl enable --now docker

if sudo docker compose version >/dev/null 2>&1; then
  sudo docker compose up -d
elif command -v docker-compose >/dev/null 2>&1; then
  sudo docker-compose up -d
else
  sudo apt-get update
  sudo apt-get install -y docker-compose
  sudo docker-compose up -d
fi

# Herramientas SNMP para las pruebas (snmpwalk / snmpget / snmpset)
command -v snmpwalk >/dev/null 2>&1 || sudo apt-get install -y snmp

sudo docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'
echo
echo "Listo. Espera 1-2 minutos y abre Firefox en: http://localhost:8080"
