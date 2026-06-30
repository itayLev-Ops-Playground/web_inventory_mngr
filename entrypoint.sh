#!/bin/bash
set -euo pipefail

mkdir -p /data
chown -R www-data:www-data /var/www/inv-web-mngr /data
chmod -R 755 /var/www/inv-web-mngr

if [ -f /tmp/dummy_data.json ]; then
  cp /tmp/dummy_data.json /data/dummy_data.json
fi

if [ -f /tmp/data_base.json ]; then
  cp /tmp/data_base.json /data/data_base.json
fi

export INVENTORY_DATA_DIR=/data

apachectl -D FOREGROUND
