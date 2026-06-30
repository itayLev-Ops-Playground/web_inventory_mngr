FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    INVENTORY_DATA_DIR=/data

WORKDIR /var/www

RUN apt-get update && apt-get install -y \
    apache2 \
    libapache2-mod-wsgi-py3 \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    unzip \
    git \
    && apt-get clean

COPY . /var/www/inv-web-mngr

RUN python3 -m venv /var/www/inv-web-mngr/venv \
    && /var/www/inv-web-mngr/venv/bin/pip install --upgrade pip \
    && /var/www/inv-web-mngr/venv/bin/pip install -r /var/www/inv-web-mngr/requirements.txt

RUN cp /var/www/inv-web-mngr/inv-web-mngr.conf /etc/apache2/sites-available/inv-web-mngr.conf \
    && a2enmod wsgi \
    && a2ensite inv-web-mngr \
    && a2dissite 000-default.conf || true

RUN mkdir -p /data /tmp/inventory-data \
    && cp /var/www/inv-web-mngr/data/dummy_data.json /tmp/inventory-data/dummy_data.json \
    && cp /var/www/inv-web-mngr/data/data_base.json /tmp/inventory-data/data_base.json \
    && chown -R www-data:www-data /var/www/inv-web-mngr /data /tmp/inventory-data \
    && chmod -R 755 /var/www/inv-web-mngr

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 80
VOLUME ["/data"]

CMD ["/usr/local/bin/entrypoint.sh"]
