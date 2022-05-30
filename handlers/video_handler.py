from telebot import TeleBot, types
import content
from log import logger
from handlers.buttons import manage_data


def handle(bot: TeleBot):
    @bot.message_handler(content_types=['video', 'animation'])
    def video(message: types.Message):
        try:
            msg_info = None
            if message.content_type == 'video':
                msg_info = bot.get_file(message.video.file_id)
            if message.content_type == 'animation':
                msg_info = bot.get_file(message.animation.file_id)  
                 
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
                msg_info.file_path.replace('videos/', '').replace('animations/', ''),
                downloaded_file
            )

            if content.set_save_media_time(message.from_user.username, message.chat.id):
                bot.send_message(
                    message.chat.id,
                    'Ваш контент был успешно сохранен',
                    reply_markup=manage_data
                )

        except Exception as e:
            logger.exception("Ошибка отправки видео: %s" % e)  
