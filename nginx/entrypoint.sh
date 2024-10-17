#!/bin/sh

# Замена переменной ${SERVER_NAME} в nginx.conf
sed -i "s|\${SERVER_NAME}|${SERVER_NAME}|g" /etc/nginx/nginx.conf

# Запуск Nginx с самоподписанным сертификатом
nginx

# Запуск Certbot для получения реального сертификата
certbot certonly --webroot -w /var/lib/letsencrypt --non-interactive --agree-tos --email ${CERTBOT_EMAIL} -d ${SERVER_NAME}

# Перезагрузка Nginx после получения сертификатов
nginx -s reload

# Бесконечный цикл для автоматического обновления сертификатов и перезагрузки Nginx
while :; do
    certbot renew --quiet
    nginx -s reload
    sleep 12h
done
