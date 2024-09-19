import telepot

def send_telegram_message(telegram_token, telegram_chat_id, message):
    bot = telepot.Bot(telegram_token)
    bot.sendMessage(telegram_chat_id, message)