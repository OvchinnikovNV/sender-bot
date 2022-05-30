import os
from time import sleep
from telebot import TeleBot, types
import handlers.buttons as buttons
import content
from log import logger


def handle(bot: TeleBot):
    @bot.message_handler(content_types=['text'])
    def text(message: types.Message):
        if message.text == 'Отправить данные':
            bot.send_message(
                message.chat.id,
                get_confirm_msg(message, 'отправить'),
                reply_markup=buttons.confirm_send
            )
            return

        if message.text == 'Удалить данные':
            bot.send_message(
                message.chat.id,
                get_confirm_msg(message, 'удалить'),
                reply_markup=buttons.confirm_remove
            )
            return

        if message.text == 'Отправить ✅':
            send_user_data(bot, message)
            return

        if message.text == 'Удалить ❌':
            delete_user_data(bot, message)
            return

        if message.text == 'Отмена 🚫':
            bot.send_message(
                message.chat.id,
                'Действие отменено',
                reply_markup=buttons.manage_data
            )
            return

        try:
            content.save_text(
                message.from_user.username,
                message.chat.id,
                message.text
            )
            bot.send_message(
                message.chat.id,
                'Ваш текст успешно был записан',
                reply_markup=buttons.manage_data
            )
        except Exception as e:
            logger.exception("Ошибка отправки сообщения: %s" % e)

    
    # @bot.callback_query_handler(func=lambda call: True)
    # def confirming(call: types.CallbackQuery):
    #     if call.data == 'send_yes':
    #         send_user_data(bot, call.message)
    #     if call.data == 'remove_yes':
    #         delete_user_data(bot, call.message)


def send_user_data(bot: TeleBot, message: types.Message):
    if content.isEmptyContent( message.chat.username, message.chat.id ):
        bot.send_message(message.chat.id, "Для Вас нет сохраненных данных")
        return

    data = content.get_content(
        message.chat.username,
        message.chat.id
    )

    text = "Данные от @" + message.chat.username
    if data['text'] is not None:
        text += '\n\n' + data['text']

    caption_added = False
    media_group = []
    opened_files = []
    for photo in data['photos']:
        tmp = open(photo, 'rb')
        opened_files.append(tmp)
        if not caption_added:
            caption_added = True
            media_group.append(types.InputMediaPhoto(tmp, caption=text))
        else:
            media_group.append(types.InputMediaPhoto(tmp))

    for video in data['videos']:
        tmp = open(video, 'rb')
        opened_files.append(tmp)
        if not caption_added:
            caption_added = True
            media_group.append(types.InputMediaVideo(tmp, caption=text))
        else:
            media_group.append(types.InputMediaVideo(tmp))

    if len(media_group) > 0:
        bot.send_media_group(os.getenv('TO_CHAT_ID'), media_group)
    else:
        bot.send_message(os.getenv('TO_CHAT_ID'), text)

    for file in opened_files:
        file.close()

    content.remove_content(
        message.chat.username,
        message.chat.id
    )

    bot.send_message(
        message.chat.id,
        "Все Ваши данные были пересланы и удалены",
        reply_markup=buttons.remove_markup
    )


def delete_user_data(bot: TeleBot, message: types.Message):
    if content.isEmptyContent( message.chat.username, message.chat.id ):
        bot.send_message(message.chat.id, "Для Вас нет сохраненных данных")
        return

    content.remove_content(
        message.chat.username,
        message.chat.id
    )
    bot.send_message(
        message.chat.id,
        "Все Ваши данные были удалены",
        reply_markup=buttons.remove_markup
    )


def get_confirm_msg(message: types.Message, action: str) -> str:
    data = content.get_content(message.chat.username, message.chat.id)
    result = 'У Вас сохранено: '
    if data['text'] is not None:
        result += 'текст, '
    result += 'изображения - %d, ' % len(data['photos'])
    result += 'видео - %d.\n' % len(data['videos'])
    result += 'Вы действительно хотите ' + action + ' данные?'
    if action == 'отправить':
        result += ' После этого все данные будут удалены.'
    return result
