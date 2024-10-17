# Используем официальный образ Nginx как базовый
FROM nginx:latest

# Устанавливаем Certbot
RUN apt-get update && apt-get install -y certbot python3-certbot-nginx

# Копируем шаблон конфигурации Nginx, самоподписанные сертификаты и скрипт
COPY nginx.template.conf /etc/nginx/nginx.template.conf
COPY ssl/server.crt /etc/nginx/ssl/server.crt
COPY ssl/server.key /etc/nginx/ssl/server.key
COPY entrypoint.sh /entrypoint.sh

# Делаем скрипт исполняемым
RUN chmod +x /entrypoint.sh

# Запускаем контейнер с использованием нашего скрипта
ENTRYPOINT ["/entrypoint.sh"]
