# Generated by Django 5.1.2 on 2024-10-12 22:26

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Favicon",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="Уникальный идентификатор записи",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, help_text="Время создания записи"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, help_text="Время последнего обновления записи"),
                ),
                (
                    "name",
                    models.CharField(help_text="Название favicon", max_length=255),
                ),
                ("value", models.CharField(help_text="favicon", max_length=255)),
            ],
            options={
                "verbose_name": "Favicon",
                "verbose_name_plural": "Favicons",
                "db_table": "favicon",
            },
        ),
        migrations.CreateModel(
            name="Market",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="Уникальный идентификатор записи",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, help_text="Время создания записи"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, help_text="Время последнего обновления записи"),
                ),
                (
                    "name",
                    models.CharField(help_text="Название магазина", max_length=255),
                ),
                (
                    "price_multiplier",
                    models.FloatField(default=1, help_text="Коэффициент ценообразования"),
                ),
                (
                    "env",
                    models.CharField(
                        blank=True,
                        help_text="Название env для api",
                        max_length=255,
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Магазин",
                "verbose_name_plural": "Магазины",
                "db_table": "market",
            },
        ),
        migrations.CreateModel(
            name="MessageTelegram",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="Уникальный идентификатор записи",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, help_text="Время создания записи"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, help_text="Время последнего обновления записи"),
                ),
                (
                    "value",
                    models.BigIntegerField(
                        help_text="Уникальный идентификатор сообщения Telegram",
                        unique=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Telegram Message",
                "verbose_name_plural": "Telegram Messages",
                "db_table": "message_telegram",
            },
        ),
        migrations.CreateModel(
            name="GroupProduct",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="Уникальный идентификатор записи",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, help_text="Время создания записи"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, help_text="Время последнего обновления записи"),
                ),
                (
                    "idx",
                    models.IntegerField(help_text="Индекс сортировки группового продукта"),
                ),
                (
                    "name",
                    models.CharField(help_text="Название группы продукта", max_length=255),
                ),
                (
                    "favicon",
                    models.ForeignKey(
                        help_text="Ссылка на favicon группового продукта",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.favicon",
                    ),
                ),
                (
                    "message",
                    models.ForeignKey(
                        help_text="Ссылка на сообщение Telegram",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.messagetelegram",
                    ),
                ),
            ],
            options={
                "verbose_name": "Группа продукта",
                "verbose_name_plural": "Группа продуктов",
                "db_table": "group_product",
            },
        ),
        migrations.CreateModel(
            name="OriginCountry",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="Уникальный идентификатор записи",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, help_text="Время создания записи"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, help_text="Время последнего обновления записи"),
                ),
                ("name", models.CharField(help_text="Название страны", max_length=255)),
                (
                    "favicon",
                    models.ForeignKey(
                        help_text="favicon страны",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.favicon",
                    ),
                ),
            ],
            options={
                "verbose_name": "Страна",
                "verbose_name_plural": "Страны",
                "db_table": "origin_country",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="Уникальный идентификатор записи",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, help_text="Время создания записи"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, help_text="Время последнего обновления записи"),
                ),
                ("idx", models.IntegerField(help_text="Индекс сортировки продукта")),
                (
                    "name",
                    models.CharField(help_text="Название продукта", max_length=255),
                ),
                (
                    "is_hot",
                    models.BooleanField(default=False, help_text="Является ли цена горячей?"),
                ),
                (
                    "is_new",
                    models.BooleanField(default=False, help_text="Является ли продукт новым?"),
                ),
                (
                    "waiting_delivery",
                    models.BooleanField(default=False, help_text="Ожидает ли продукт доставки?"),
                ),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        help_text="Страна продукта",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="product.origincountry",
                    ),
                ),
                (
                    "favicon",
                    models.ForeignKey(
                        blank=True,
                        help_text="Favicon продукта",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="product.favicon",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
                "db_table": "product",
            },
        ),
        migrations.CreateModel(
            name="ProductPrice",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="Уникальный идентификатор записи",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, help_text="Время создания записи"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, help_text="Время последнего обновления записи"),
                ),
                ("value", models.FloatField(help_text="Цена продукта")),
                (
                    "market",
                    models.ForeignKey(
                        help_text="Магазин, связанный с ценой продукта",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.market",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        help_text="Продукт, связанный с ценой",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Цена продукта",
                "verbose_name_plural": "Цена продуктов",
                "db_table": "product_price",
                "constraints": [models.UniqueConstraint(fields=("market", "product"), name="unique_product_market")],
            },
        ),
    ]
