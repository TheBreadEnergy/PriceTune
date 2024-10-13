import asyncio
import logging

from config.config import settings

from .models import GroupProduct, MarketTag
from .telegram_bot import TelegramBot

logger = logging.getLogger(__name__)


def publish_to_all(product):
    generate_message(product.group.find_top_parent().message)


def generate_header(group):
    """
    Генерирует заголовок для группы или подгруппы с учётом флага is_show_name.
    Если заголовок не нужен, возвращает пустую строку.
    """
    if group.is_show_name:
        header = (
            f"{group.favicon.value if group.favicon else ''} "
            f"{group.name} {group.favicon.value if group.favicon else ''}"
        )
        title_length = len(group.name) + (8 if group.favicon else 0)
        filler_length = (60 - title_length) // 2
        return f"{'•' * filler_length}{header}{'•' * filler_length}\n\n"
    return ""


def generate_message(message_telegram):
    """
    Генерирует текст сообщения для Telegram на основе всех корневых групп, связанных с сообщением, и всей их иерархии.
    """
    # Получение всех корневых групп, связанных с данным сообщением
    top_groups = GroupProduct.objects.filter(message=message_telegram, parent__isnull=True).order_by("idx")

    if not top_groups.exists():
        raise ValueError("Для данного сообщения нет связанных корневых групп.")

    # Начальное сообщение
    message = ""

    # Рекурсивное добавление всех подгрупп и продуктов для каждой корневой группы
    def add_group_and_products(group, message):
        # Добавляем ровно один отступ перед каждой новой группой
        if message and not message.endswith("\n\n"):
            message += "\n"  # Добавляем два переноса строки, если их нет

        # Добавление продуктов группы
        products = group.products.all().order_by("idx")
        for product in products:
            flags = ""
            if product.country:
                flags += product.country.favicon
            if product.is_hot:
                flags += "🔥"
            if product.waiting_delivery:
                flags += "🚚"
            product_prices = product.productprice_set.select_related("market").filter(market__tag=MarketTag.TELEGRAM)
            for price in product_prices:
                message += f"{"🆕" if product.is_new else ""}{product.name} - {int(price.value)}{flags}\n"

        # Добавление подгрупп
        subgroups = group.children.all().order_by("idx")
        for subgroup in subgroups:
            # Добавляем заголовок подгруппы
            message += generate_header(subgroup)
            # Рекурсивный вызов для добавления продуктов и подгрупп
            message = add_group_and_products(subgroup, message)

        # Добавление description_end, если оно есть
        if group.description_end:
            message += f"\n{group.description_end}\n"

        return message

    # Проходим по каждой корневой группе и добавляем её в сообщение
    for i, top_group in enumerate(top_groups):
        if i > 0 and not message.endswith("\n\n"):
            message += "\n"  # Добавляем отступ между корневыми группами
        message += generate_header(top_group)  # Формируем заголовок для корневой группы
        message = add_group_and_products(top_group, message)

    # Отправка сообщения в Telegram
    logger.info(message)
    telegram_bot = TelegramBot(token=settings.TELEGRAM_BOT_TOKEN, chat_id=settings.TELEGRAM_CHAT_ID)
    asyncio.run(telegram_bot.edit_message(message_telegram.value, message))

    return message
