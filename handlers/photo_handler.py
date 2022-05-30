from telebot import TeleBot, types
from handlers.buttons import manage_data
import content
from log import logger


def handle(bot: TeleBot):
    @bot.message_handler(content_types=['photo', 'document'])
    def photo(message: types.Message):
        try:
            if message.content_type == 'photo':
                msg_info = bot.get_file(message.photo[-1].file_id)
            if message.content_type == 'document':
                if not message.document.mime_type.startswith('image'):
                    return
                msg_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(msg_info.file_path)

            if content.count_user_media(message.from_user.username, message.chat.id) >= 10:
                bot.send_message(
                    message.chat.id,
                    'Сохранено уже 10 Ваших медиа файлов. Отправьте или удалите их.',
                    reply_markup=manage_data
                )
                return
            
            if message.caption:
                content.save_text(
                    message.from_user.username,
                    message.chat.id,
                    message.caption
                )

            content.save_image(
                message.from_user.username,
                message.chat.id,
                msg_info.file_path.replace('photos/', '').replace('documents/', ''),
                downloaded_file,
            )

            if content.set_save_media_time(message.from_user.username, message.chat.id):
                bot.send_message(
                    message.chat.id,
                    'Ваш контент был успешно сохранен',
                    reply_markup=manage_data
                )

        except Exception as e:
            logger.exception("Ошибка отправки изображения:\n%s" % e)  
