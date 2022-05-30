from subprocess import call
from telebot import types


manage_data = types.ReplyKeyboardMarkup( resize_keyboard=True )
btn_send_data = types.KeyboardButton("Отправить данные")
btn_remove_data = types.KeyboardButton("Удалить данные")
manage_data.row(btn_send_data, btn_remove_data)

btn_cancel = types.KeyboardButton('Отмена 🚫')

confirm_send = types.ReplyKeyboardMarkup( resize_keyboard=True )
btn_confirm_send = types.KeyboardButton('Отправить ✅')
confirm_send.row(btn_confirm_send, btn_cancel)

confirm_remove = types.ReplyKeyboardMarkup( resize_keyboard=True )
btn_confirm_remove = types.KeyboardButton('Удалить ❌')
confirm_remove.row(btn_confirm_remove, btn_cancel)

remove_markup = types.ReplyKeyboardRemove()

# send_data_keyboard = types.InlineKeyboardMarkup()
# btn_send_yes = types.InlineKeyboardButton(text='Отправить', callback_data='send_yes')
# send_data_keyboard.row(btn_send_yes)

# remove_data_keyboard = types.InlineKeyboardMarkup()
# btn_remove_yes = types.InlineKeyboardButton(text='Удалить', callback_data='remove_yes')
# remove_data_keyboard.row(btn_remove_yes)
