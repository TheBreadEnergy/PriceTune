import nested_admin
from config.config import settings
from django import forms
from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import path
from mptt.forms import TreeNodeChoiceField

from .models import Favicon, GroupProduct, Market, MessageTelegram, OriginCountry, Product, ProductPrice
from .utils import publish_to_all

admin.site.site_header = settings.NAME_SHOP
admin.site.site_title = settings.NAME_SHOP
admin.site.index_title = f"Добро пожаловать в {settings.NAME_SHOP}"


# Admin registrations
@admin.register(MessageTelegram)
class MessageTelegramAdmin(admin.ModelAdmin):
    ordering = ["created"]
    list_display = ("name", "value", "updated")
    search_fields = (
        "name",
        "value",
    )


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


class ProductForm(forms.ModelForm):
    group = TreeNodeChoiceField(queryset=GroupProduct.objects.all())

    class Meta:
        model = Product
        fields = "__all__"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm  # Подключаем форму с древовидным виджетом
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


class SubGroupProductForm(forms.ModelForm):
    class Meta:
        model = GroupProduct
        fields = "__all__"
        widgets = {
            "description_end": forms.Textarea(attrs={"rows": 4, "cols": 40}),
        }


class Sub2GroupInline(nested_admin.NestedTabularInline):
    form = SubGroupProductForm
    model = GroupProduct
    fk_name = "parent"
    extra = 0
    verbose_name = "Подгруппа второго уровня"
    verbose_name_plural = "Подгруппы второго уровня"
    ordering = ["idx"]
    exclude = ["message"]


class SubGroupInline(nested_admin.NestedTabularInline):
    form = SubGroupProductForm
    inlines = [Sub2GroupInline]
    model = GroupProduct
    fk_name = "parent"
    extra = 0
    verbose_name = "Подгруппа"
    verbose_name_plural = "Подгруппы"
    ordering = ["idx"]
    exclude = ["message"]


@admin.register(GroupProduct)
class GroupProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [SubGroupInline]
    extra = 0
    ordering = ["created"]
    exclude = ["parent"]
    list_display = ("name", "favicon", "updated")
    search_fields = ("name",)

    def get_queryset(self, request):
        """
        Переопределяем queryset, чтобы выводить только верхние группы, у которых нет родителя.
        """
        qs = super().get_queryset(request)
        return qs.filter(parent__isnull=True)
