#!/bin/bash
set -euo pipefail

echo "[entrypoint] Initializing container..."

# Ensure data directory exists with proper permissions
mkdir -p /data
chown -R www-data:www-data /var/www/inv-web-mngr /data
chmod -R 755 /var/www/inv-web-mngr

# Attempt to download dummy data from S3 if not already present
if [ ! -f /data/dummy_data.json ] || [ ! -f /data/data_base.json ]; then
  echo "[entrypoint] Data files not found in /data. Attempting S3 download..."
  
  if [ -n "${S3_BUCKET:-}" ]; then
    echo "[entrypoint] Downloading from S3 bucket: ${S3_BUCKET}"
    aws s3 cp "${S3_BUCKET}/dummy_data.json" /data/dummy_data.json --no-sign-request 2>/dev/null || \
    aws s3 cp "${S3_BUCKET}/dummy_data.json" /data/dummy_data.json 2>/dev/null || \
    echo "[entrypoint] WARNING: Failed to download dummy_data.json from S3"
    
    aws s3 cp "${S3_BUCKET}/data_base.json" /data/data_base.json --no-sign-request 2>/dev/null || \
    aws s3 cp "${S3_BUCKET}/data_base.json" /data/data_base.json 2>/dev/null || \
    echo "[entrypoint] WARNING: Failed to download data_base.json from S3"
  else
    echo "[entrypoint] S3_BUCKET not set. Skipping S3 download."
  fi
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

# Set environment variable for the app
export INVENTORY_DATA_DIR=/data

echo "[entrypoint] Starting Apache in foreground mode..."
apachectl -D FOREGROUND
