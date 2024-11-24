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

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
Бот для управления чатом.

Команды:

* `/start` - начать работу с ботом.
* `/ban` - банить пользователя, отправившего сообщение. Используйте эту команду в ответ на сообщение пользователя, которого вы хотите забанить.
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

bot.infinity_polling(none_stop=True)
