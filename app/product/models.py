import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, help_text="Уникальный идентификатор записи"
    )
    created = models.DateTimeField(auto_now_add=True, help_text="Время создания записи")
    updated = models.DateTimeField(auto_now=True, help_text="Время последнего обновления записи")

    class Meta:
        abstract = True


class MessageTelegram(BaseModel):
    value = models.BigIntegerField(unique=True, help_text="Уникальный идентификатор сообщения Telegram")

    class Meta:
        db_table = "message_telegram"
        verbose_name = "Сообщение Telegram"
        verbose_name_plural = "Сообщения Telegram"

    def __str__(self):
        return f"{self.value}"


class Favicon(BaseModel):
    name = models.CharField(max_length=255, help_text="Название favicon")
    value = models.CharField(max_length=255, help_text="favicon")

    class Meta:
        db_table = "favicon"
        verbose_name = "Иконка"
        verbose_name_plural = "Иконки"

    def __str__(self):
        return f"{self.name} ({self.value})"


class OriginCountry(BaseModel):
    name = models.CharField(max_length=255, help_text="Название страны")
    favicon = models.CharField(max_length=255, help_text="favicon")

    class Meta:
        db_table = "origin_country"
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return f"{self.name} ({self.favicon})"


class Market(BaseModel):
    name = models.CharField(max_length=255, help_text="Название магазина")
    price_multiplier = models.FloatField(default=1, help_text="Коэффициент ценообразования")
    env = models.CharField(max_length=255, null=True, blank=True, help_text="Название env для api")

    class Meta:
        db_table = "market"
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def __str__(self):
        return f"{self.name}"


class GroupProduct(BaseModel):
    idx = models.IntegerField(help_text="Индекс сортировки группового продукта")
    name = models.CharField(max_length=255, help_text="Название группы продукта")
    favicon = models.ForeignKey(
        Favicon, on_delete=models.SET_NULL, null=True, blank=True, help_text="Ссылка на favicon группового продукта"
    )
    message = models.ForeignKey(
        MessageTelegram,
        on_delete=models.SET_NULL,
        null=True,  # Позволяет быть NULL для подгрупп
        blank=True,  # Позволяет оставлять поле пустым в формах
        help_text="Ссылка на сообщение Telegram (только для главных групп)",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        help_text="Родительская группа (если есть)",
    )

    class Meta:
        db_table = "group_product"
        verbose_name = "Группа продукта"
        verbose_name_plural = "Группы продуктов"

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.parent is None and not self.message:
            raise ValidationError({"message": "Главные группы должны иметь связанное сообщение Telegram."})
        if self.parent is not None and self.message:
            raise ValidationError({"message": "Подгруппы не должны иметь связанного сообщения Telegram."})


class Product(BaseModel):
    idx = models.IntegerField(help_text="Индекс сортировки продукта")
    name = models.CharField(max_length=255, help_text="Название продукта")
    is_hot = models.BooleanField(default=False, help_text="Является ли цена горячей?")
    is_new = models.BooleanField(default=False, help_text="Является ли продукт новым?")
    waiting_delivery = models.BooleanField(default=False, help_text="Ожидает ли продукт доставки?")
    country = models.ForeignKey(
        OriginCountry, on_delete=models.SET_NULL, null=True, blank=True, help_text="Страна продукта"
    )
    favicon = models.ForeignKey(Favicon, on_delete=models.SET_NULL, null=True, blank=True, help_text="Favicon продукта")
    group = models.ForeignKey(
        GroupProduct, on_delete=models.PROTECT, related_name="products", help_text="Группа продукта"
    )

    class Meta:
        db_table = "product"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name}"


class ProductPrice(BaseModel):
    value = models.FloatField(help_text="Цена продукта")
    market = models.ForeignKey(Market, on_delete=models.CASCADE, help_text="Магазин, связанный с ценой продукта")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="Продукт, связанный с ценой")

    class Meta:
        db_table = "product_price"
        constraints = [models.UniqueConstraint(fields=["market", "product"], name="unique_product_market")]
        verbose_name = "Цена продукта"
        verbose_name_plural = "Цена продуктов"
