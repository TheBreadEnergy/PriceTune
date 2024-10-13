from django.contrib import admin

from .models import Favicon, GroupProduct, Market, MessageTelegram, OriginCountry, Product, ProductPrice


# Admin registrations
@admin.register(MessageTelegram)
class MessageTelegramAdmin(admin.ModelAdmin):
    ordering = ["created"]
    list_display = ("value", "updated")
    search_fields = ("value",)


@admin.register(Favicon)
class FaviconAdmin(admin.ModelAdmin):
    ordering = ["created"]
    list_display = ("name", "value", "updated")
    search_fields = (
        "name",
        "value",
    )


@admin.register(OriginCountry)
class OriginCountryAdmin(admin.ModelAdmin):
    ordering = ["created"]
    list_display = ("name", "favicon", "updated")
    search_fields = ("name",)


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    ordering = ["created"]
    list_display = ("name", "updated")
    search_fields = ("name", "env")


class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPriceInline]
    ordering = ["created"]
    list_display = ("name", "country", "is_hot", "is_new", "waiting_delivery", "updated")

    search_fields = ("name",)
    list_filter = ("is_hot", "is_new", "waiting_delivery")


@admin.register(GroupProduct)
class GroupProductAdmin(admin.ModelAdmin):
    ordering = ["created"]
    list_display = ("name", "favicon", "updated")
    search_fields = ("name",)
