import telebot
from config import token

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")


@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно mute администратора.")
        else:
            bot.restrict_chat_member(chat_id, user_id, can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False)
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был muted.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите mute.")

@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Администратора нельзя mute.")
        else:
            bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был разглушен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите unmute.")


@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
Бот для управления чатом.

Команды:

* `/start` - начать работу с ботом.
* `/ban` - банить пользователя, отправившего сообщение. Используйте эту команду в ответ на сообщение пользователя, которого вы хотите забанить.
* 'mute' - замютит пользователя.
* 'unmute' - размютит пользователя.
* `/ban` автоматически банит пользователей, которые отправляют ссылки в группе.

Примечание: Бот будет работать только в группах, где он имеет права администратора.
"""
    bot.reply_to(message, help_text)



@bot.message_handler(func=lambda message: True)
def check_message(message):
    if "https://" in message.text:
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь @{message.from_user.username} был забанен за отправку ссылки.")

@bot.message_handler(content_types=['new_chat_members'])
def new_member(message):
    bot.send_message(message.chat.id, 'Я принял нового пользователя!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

bot.infinity_polling(none_stop=True)
