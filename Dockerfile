FROM python:3.12.2

WORKDIR /opt/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'config.settings'
ENV PIP_ROOT_USER_ACTION=ignore

RUN groupadd -r django && useradd -d /opt/app -r -g django django \
    && chown django:django -R /opt/app/

# Устанавливаем poetry
COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-root --without dev

# Копируем папку envs
COPY envs /opt/envs

# Копируем все файлы проекта из папки app
COPY app/ /opt/app

# Сбор статических файлов, используя виртуальное окружение, созданное Poetry
RUN mkdir /opt/app/static && mkdir /opt/app/uploads && poetry run python ./manage.py collectstatic --noinput

# Открываем порт для доступа к приложению
EXPOSE 8000

# Создаем volume для хранения статических и загруженных файлов
VOLUME /opt/app/static
VOLUME /opt/app/uploads

# Изменяем владельца папок на пользователя django
RUN chown -R django:django /opt/app/static
RUN chown -R django:django /opt/app/uploads

# Меняем пользователя на django для запуска приложения
USER django

# Используем Gunicorn для запуска приложения
CMD ["poetry", "run", "gunicorn", "-c", "gunicorn_conf.py", "config.wsgi:application"]
