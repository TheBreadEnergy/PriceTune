from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import path

from .models import Favicon, GroupProduct, Market, MessageTelegram, OriginCountry, Product, ProductPrice
from .utils import publish_to_all


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

    change_form_template = "admin/product/change_form_product.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/publish/",
                self.admin_site.admin_view(self.publish),
                name="product-publish",
            ),
        ]
        return custom_urls + urls

    def publish(self, request, object_id, *args, **kwargs):
        product = get_object_or_404(Product, pk=object_id)

        # Проверка наличия группы и её сообщения Telegram
        if not product.group:
            self.message_user(request, "У продукта не назначена группа.", level=messages.ERROR)
            return redirect("admin:product_product_change", object_id=object_id)

        if not product.group.message and not product.group.parent and not product.group.parent.message:
            self.message_user(request, "У группы продукта не назначено сообщение Telegram.", level=messages.ERROR)
            return redirect("admin:product_product_change", object_id=object_id)

        publish_to_all(product)
        return redirect("admin:product_product_change", object_id=object_id)


@admin.register(GroupProduct)
class GroupProductAdmin(admin.ModelAdmin):
    ordering = ["created"]
    list_display = ("name", "favicon", "updated")
    search_fields = ("name",)
