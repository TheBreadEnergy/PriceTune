import asyncio

from app.product.telegram_bot import telegram_bot


def publish_to_all(product):
    generate_message(product)


def generate_message(product):
    """
    Генерирует текст сообщения для Telegram на основе продукта и всей иерархии группы.
    """
    # Получение главной группы продукта
    main_group = product.group

    # Поиск самого верхнего родителя
    top_group = main_group.find_top_parent()

    # Проверка наличия сообщения у верхнего родителя
    if not top_group.message:
        raise ValueError("У самого верхнего родителя нет сообщения Telegram.")

    # Формирование заголовка для самого верхнего родителя
    zag = f"{top_group.favicon.value} {top_group.name} {top_group.favicon.value}"
    title_length = len(top_group.name) + 2  # Длина названия + 2 эмодзи
    filler_length = (50 - title_length) // 2
    message = f"{'•' * filler_length}{zag}{'•' * filler_length}" + "\n\n"

    # Рекурсивное добавление всех подгрупп и продуктов
    def add_group_and_products(group, message):
        # Добавление продуктов группы
        products = group.products.all().order_by("idx")  # Сортировка по idx
        for product in products:
            product_prices = product.productprice_set.select_related("market").order_by("market__name").all()
            for price in product_prices:
                message += f"{product.name} - {int(price.value)}{product.country.favicon if product.country else ''}\n"

        # Добавление подгрупп
        subgroups = group.children.all().order_by("idx")
        for subgroup in subgroups:
            # zag = (f"{subgroup.favicon.value if subgroup.favicon else ' '} "
            #        f"{subgroup.name} {subgroup.favicon.value if subgroup.favicon else ' '}")
            # title_length = len(subgroup.name) + (2 if subgroup.favicon else 0)
            # filler_length = (50 - title_length) // 2
            # message += f"\n{'•' * filler_length}{zag}{'•' * filler_length}" + "\n\n"
            message += "\n"
            # Рекурсивный вызов для добавления продуктов и подгрупп
            message = add_group_and_products(subgroup, message)

        return message

    # Добавляем подгруппы и продукты для всей иерархии начиная с top_group
    message = add_group_and_products(top_group, message)

    asyncio.run(telegram_bot.edit_message(top_group.message.value, message))
    return message
