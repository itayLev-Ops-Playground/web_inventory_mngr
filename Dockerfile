FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    INVENTORY_DATA_DIR=/data \
    GITHUB_REPO=https://github.com/itayLev-Ops-Playground/web_inventory_mngr.git

WORKDIR /var/www

# Install system packages
RUN apt-get update && apt-get install -y \
    apache2 \
    libapache2-mod-wsgi-py3 \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    unzip \
    git \
    awscli \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Clone the application from GitHub
RUN git clone ${GITHUB_REPO} /var/www/inv-web-mngr

# Create virtual environment and install Python dependencies
RUN python3 -m venv /var/www/inv-web-mngr/venv \
    && /var/www/inv-web-mngr/venv/bin/pip install --upgrade pip \
    && /var/www/inv-web-mngr/venv/bin/pip install -r /var/www/inv-web-mngr/requirements.txt

# Configure Apache virtual host
RUN cp /var/www/inv-web-mngr/inv-web-mngr.conf /etc/apache2/sites-available/inv-web-mngr.conf \
    && a2enmod wsgi \
    && a2ensite inv-web-mngr \
    && a2dissite 000-default.conf || true

# Create data directory and prepare for S3 download
RUN mkdir -p /data /tmp/inventory-data

# Copy entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Expose HTTP port
EXPOSE 80

# Define persistent data volume
VOLUME ["/data"]

# Set entrypoint for data initialization and Apache startup
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
