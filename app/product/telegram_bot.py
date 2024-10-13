import logging

from telegram import Bot, error

logger = logging.getLogger("django")


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
        try:
            await self.bot.edit_message_text(chat_id=self.chat_id, message_id=message_id, text=new_text)
        except error.BadRequest as e:
            if "Message is not modified" in str(e):
                logger.info(f"Сообщение с ID {message_id} не изменено: новое содержание идентично текущему.")
            else:
                logger.error(f"Ошибка при редактировании сообщения с ID {message_id}: {str(e)}", exc_info=True)
        except Exception as e:
            logger.error(f"Неизвестная ошибка при редактировании сообщения с ID {message_id}: {str(e)}")
