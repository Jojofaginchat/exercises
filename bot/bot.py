import config
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler

CALLBACK_GOOD = 'good'
CALLBACK_BAD = 'bad('
CALLBACK_OK = 'ok'


def generate_keyboard():
    keyboard = [
        [InlineKeyboardButton('Хорошо', callback_data=CALLBACK_GOOD),
        InlineKeyboardButton('Норм', callback_data=CALLBACK_OK),
        InlineKeyboardButton('Плохо', callback_data=CALLBACK_BAD)]
    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_regulate(update: Update, context):
    query = update.callback_query
    current_callback = query.data

    chat_id1 = update.effective_message.chat_id

    query.edit_message_text(
        text=update.effective_message.text
    )

    if current_callback == CALLBACK_GOOD:
        context.bot.send_message(
            chat_id=chat_id1,
            text='это замечательно!'
        )

    elif current_callback == CALLBACK_OK:
        context.bot.send_message(
            chat_id=chat_id1,
            text='отлично'
        )

    elif current_callback == CALLBACK_BAD:
        context.bot.send_message(
            chat_id=chat_id1,
            text='мне жаль, солнце('
        )


def hello(update: Update, context):
    context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text=update.effective_message.text
    )


def start(update: Update, context):
    user_name = update.effective_user.first_name
    context.bot.send_message(
        chat_id=update.effective_message.chat_id,
        text=f'Привет, {user_name}!\nКак твои дела?',
        reply_markup=generate_keyboard()
    )


def main():
    my_update = Updater(
        token=config.TOKEN,
        base_file_url=config.PROXI,
        use_context=True
    )

    keyboard_handler = CallbackQueryHandler(callback=keyboard_regulate, pass_chat_data=True)
    my_handler = MessageHandler(Filters.all, hello)
    start_handler = CommandHandler('start', start)

    my_update.dispatcher.add_handler(start_handler)
    my_update.dispatcher.add_handler(my_handler)
    my_update.dispatcher.add_handler(keyboard_handler)

    my_update.start_polling()
    my_update.idle()


if __name__ == '__main__':
    main()
