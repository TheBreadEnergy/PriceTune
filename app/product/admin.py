from django.contrib import admin

from .models import Favicon, GroupProduct, Market, MessageTelegram, OriginCountry, Product, ProductPrice


# Admin registrations
@admin.register(MessageTelegram)
class MessageTelegramAdmin(admin.ModelAdmin):
    ordering = ["-created"]
    list_display = ("value", "created", "updated")
    search_fields = ("value",)


@admin.register(Favicon)
class FaviconAdmin(admin.ModelAdmin):
    ordering = ["-created"]
    list_display = ("name", "value", "created", "updated")
    search_fields = (
        "name",
        "value",
    )

    def __str__(self):
        return f"{self.name} ({self.value})"

    ordering = ["-created"]
    list_display = ("name", "value", "created", "updated")
    search_fields = (
        "name",
        "value",
    )


@admin.register(OriginCountry)
class OriginCountryAdmin(admin.ModelAdmin):
    ordering = ["-created"]
    list_display = ("name", "favicon_display", "created", "updated")
    search_fields = ("name",)

    def favicon_display(self, obj):
        return f"{obj.favicon.name} ({obj.favicon.value})"

    favicon_display.short_description = "Favicon"
    ordering = ["-created"]
    list_display = ("name", "favicon", "created", "updated")
    search_fields = ("name",)


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    ordering = ["-created"]
    list_display = ("name", "price_multiplier", "env", "created", "updated")
    search_fields = ("name", "env")


class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPriceInline]
    ordering = ["-created"]
    list_display = (
        "name",
        "idx",
        "is_hot",
        "is_new",
        "waiting_delivery",
        "country",
        "favicon_display",
        "price",
        "created",
        "updated",
    )
    search_fields = ("name",)
    list_filter = ("is_hot", "is_new", "waiting_delivery")

    def favicon_display(self, obj):
        return f"{obj.favicon.name} ({obj.favicon.value})"

    favicon_display.short_description = "Favicon"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if "price" in form.changed_data:
            ProductPrice.objects.create(product=obj, value=obj.price, market=Market.objects.first())

    ordering = ["-created"]
    list_display = (
        "name",
        "idx",
        "is_hot",
        "is_new",
        "waiting_delivery",
        "country",
        "favicon_display",
        "created",
        "updated",
    )
    search_fields = ("name",)
    list_filter = ("is_hot", "is_new", "waiting_delivery")

    def favicon_display(self, obj):
        return f"{obj.favicon.name} ({obj.favicon.value})"

    favicon_display.short_description = "Favicon"
    ordering = ["-created"]
    list_display = ("name", "idx", "is_hot", "is_new", "waiting_delivery", "country", "favicon", "created", "updated")
    search_fields = ("name",)
    list_filter = ("is_hot", "is_new", "waiting_delivery")


@admin.register(GroupProduct)
class GroupProductAdmin(admin.ModelAdmin):
    ordering = ["-created"]
    list_display = ("name", "idx", "favicon_display", "message", "created", "updated")
    search_fields = ("name",)

    def favicon_display(self, obj):
        return f"{obj.favicon.name} ({obj.favicon.value})"

    favicon_display.short_description = "Favicon"
    ordering = ["-created"]
    list_display = ("name", "idx", "favicon", "message", "created", "updated")
    search_fields = ("name",)


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    ordering = ["-created"]
    list_display = ("product", "market", "value", "created", "updated")
    search_fields = ("market__name", "product__name")
