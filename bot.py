from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Токен вашего бота
TOKEN = "7964615989:AAG7-mlJqJubVGfa4g3Q0bAI3Pjgv-1RmUU"

# ID учителя (можно получить через команду /start)
TEACHER_ID = "1012202621"


# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if str(user.id) == TEACHER_ID:
        update.message.reply_text("Добро пожаловать, преподаватель! Вы готовы принимать задания.")
    else:
        update.message.reply_text("Привет! Отправь свое домашнее задание, и я передам его преподавателю.")


# Обработка текстовых сообщений (сдача ДЗ)
def handle_homework(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    message = f"Новое ДЗ от {user.full_name} (@{user.username}):\n\n{update.message.text}"
    bot = Bot(TOKEN)
    bot.send_message(chat_id=TEACHER_ID, text=message)


# Оценка ДЗ (от преподавателя ученику)
def evaluate(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) != TEACHER_ID:
        update.message.reply_text("Эта команда доступна только преподавателю.")
        return

    try:
        args = context.args
        user_id, comment = args[0], " ".join(args[1:])
        bot = Bot(TOKEN)
        bot.send_message(chat_id=user_id, text=f"Преподаватель оценил вашу работу: {comment}")
        update.message.reply_text("Оценка отправлена.")
    except IndexError:
        update.message.reply_text("Использование: /evaluate <ID_ученика> <оценка/комментарий>")


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("evaluate", evaluate))

    # Обработчик сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_homework))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
