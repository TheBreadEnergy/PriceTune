from telegram import Bot

from app.config.config import settings


class TelegramBot:
    def __init__(self, token: str, chat_id: int):
        """
        Инициализация бота с токеном и ID чата.

        :param token: Токен Telegram бота.
        :param chat_id: ID чата, в который будут отправляться и редактироваться сообщения.
        """
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    async def edit_message(self, message_id: int, new_text: str):
        """
        Асинхронно редактирует сообщение по его идентификатору.

        :param message_id: Идентификатор сообщения, которое нужно отредактировать.
        :param new_text: Новый текст для сообщения.
        """
        await self.bot.edit_message_text(chat_id=self.chat_id, message_id=message_id, text=new_text)


telegram_bot = TelegramBot(token=settings.TELEGRAM_BOT_TOKEN, chat_id=settings.TELEGRAM_CHAT_ID)
