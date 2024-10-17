#!/bin/sh

# Проверяем наличие сертификатов Let's Encrypt
if [ -f "/etc/letsencrypt/live/${SERVER_NAME}/fullchain.pem" ]; then
    SSL_CERTIFICATE="/etc/letsencrypt/live/${SERVER_NAME}/fullchain.pem"
    SSL_CERTIFICATE_KEY="/etc/letsencrypt/live/${SERVER_NAME}/privkey.pem"
else
    SSL_CERTIFICATE="/etc/nginx/ssl/server.crt"
    SSL_CERTIFICATE_KEY="/etc/nginx/ssl/server.key"
fi

# Подставляем значения в шаблон конфигурации
envsubst '${SERVER_NAME} ${SSL_CERTIFICATE} ${SSL_CERTIFICATE_KEY}' < /etc/nginx/nginx.template.conf > /etc/nginx/nginx.conf

# Запуск Nginx
nginx

# Попытка получить сертификат с помощью Certbot, если его еще нет
if [ ! -f "/etc/letsencrypt/live/${SERVER_NAME}/fullchain.pem" ]; then
    certbot certonly --webroot -w /var/lib/letsencrypt --non-interactive --agree-tos --email ${CERTBOT_EMAIL} -d ${SERVER_NAME}

    # Если сертификат успешно получен, обновляем конфигурацию и перезагружаем Nginx
    if [ -f "/etc/letsencrypt/live/${SERVER_NAME}/fullchain.pem" ]; then
        echo "Real certificate obtained, updating Nginx configuration..."
        SSL_CERTIFICATE="/etc/letsencrypt/live/${SERVER_NAME}/fullchain.pem"
        SSL_CERTIFICATE_KEY="/etc/letsencrypt/live/${SERVER_NAME}/privkey.pem"
        envsubst '${SERVER_NAME} ${SSL_CERTIFICATE} ${SSL_CERTIFICATE_KEY}' < /etc/nginx/nginx.template.conf > /etc/nginx/nginx.conf
        nginx -s reload
    fi
fi

# Бесконечный цикл для автоматического обновления сертификатов и перезагрузки Nginx
while :; do
    certbot renew --quiet
    nginx -s reload
    sleep 12h
done
