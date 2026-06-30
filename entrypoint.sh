#!/bin/bash
set -euo pipefail

echo "[entrypoint] Initializing container..."

# Ensure data directory exists with proper permissions
mkdir -p /data
chown -R www-data:www-data /var/www/inv-web-mngr /data
chmod -R 755 /var/www/inv-web-mngr

# Download data files from S3 HTTPS URLs if not already present
if [ ! -f /data/dummy_data.json ]; then
  echo "[entrypoint] dummy_data.json not found. Attempting download from S3..."
  curl -fsSL "https://inv-web-mngr-data.s3.us-east-1.amazonaws.com/dummy_data.json" \
    -o /data/dummy_data.json 2>/dev/null || \
    echo "[entrypoint] WARNING: Failed to download dummy_data.json"
fi

if [ ! -f /data/data_base.json ]; then
  echo "[entrypoint] data_base.json not found. Attempting download from S3..."
  curl -fsSL "https://inv-web-mngr-data.s3.us-east-1.amazonaws.com/data_base.json" \
    -o /data/data_base.json 2>/dev/null || \
    echo "[entrypoint] WARNING: Failed to download data_base.json"
fi

# Handle temporary data files if provided (e.g., via COPY in runtime)
if [ -f /tmp/dummy_data.json ]; then
  echo "[entrypoint] Restoring dummy_data.json from /tmp..."
  cp /tmp/dummy_data.json /data/dummy_data.json
  rm -f /tmp/dummy_data.json
fi

if [ -f /tmp/data_base.json ]; then
  echo "[entrypoint] Restoring data_base.json from /tmp..."
  cp /tmp/data_base.json /data/data_base.json
  rm -f /tmp/data_base.json
fi

# Ensure data directory is owned by Apache user
chown -R www-data:www-data /data
chmod -R 755 /data

# Verify data files exist (create empty ones if download failed)
if [ ! -f /data/dummy_data.json ]; then
  echo "[entrypoint] Creating empty dummy_data.json"
  echo "[]" > /data/dummy_data.json
fi

if [ ! -f /data/data_base.json ]; then
  echo "[entrypoint] Creating empty data_base.json"
  echo "[]" > /data/data_base.json
fi

chown www-data:www-data /data/*.json
chmod 644 /data/*.json

# Set environment variable for the app
export INVENTORY_DATA_DIR=/data

echo "[entrypoint] Starting Apache in foreground mode..."
apachectl -D FOREGROUND
