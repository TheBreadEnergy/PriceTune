#!/bin/sh

# Проверяем наличие сертификатов Let's Encrypt
if [ -f "/etc/letsencrypt/live/${SERVER_NAME}/fullchain.pem" ]; then
    SSL_CERTIFICATE="/etc/letsencrypt/live/${SERVER_NAME}/fullchain.pem"
    SSL_CERTIFICATE_KEY="/etc/letsencrypt/live/${SERVER_NAME}/privkey.pem"
else
    SSL_CERTIFICATE="/etc/nginx/ssl/server.crt"
    SSL_CERTIFICATE_KEY="/etc/nginx/ssl/server.key"
fi

# Выводим значение переменной SSL_CERTIFICATE для проверки
echo "SSL_CERTIFICATE is set to: $SSL_CERTIFICATE"
echo "SSL_CERTIFICATE_KEY is set to: $SSL_CERTIFICATE_KEY"

# Подставляем значения вручную в конфигурацию Nginx
sed -e "s|\${SERVER_NAME}|${SERVER_NAME}|g" \
    -e "s|\${SSL_CERTIFICATE}|${SSL_CERTIFICATE}|g" \
    -e "s|\${SSL_CERTIFICATE_KEY}|${SSL_CERTIFICATE_KEY}|g" \
    /etc/nginx/nginx.template.conf > /etc/nginx/nginx.conf

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
        sed -e "s|\${SERVER_NAME}|${SERVER_NAME}|g" \
            -e "s|\${SSL_CERTIFICATE}|${SSL_CERTIFICATE}|g" \
            -e "s|\${SSL_CERTIFICATE_KEY}|${SSL_CERTIFICATE_KEY}|g" \
            /etc/nginx/nginx.template.conf > /etc/nginx/nginx.conf
        nginx -s reload
    fi
fi

# Бесконечный цикл для автоматического обновления сертификатов и перезагрузки Nginx
while :; do
    certbot renew --quiet
    nginx -s reload
    sleep 12h
done