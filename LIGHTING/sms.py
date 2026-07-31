# import telegram
# bot = telegram.Bot(token='6432256283:AAF-Wxt0GptNDwnTtMmxD9ADekMaQ-KUZ3g')
# bot.send_message(chat_id='cmcyn_bot', text="hellow")


from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


app = ApplicationBuilder().token("6432256283:AAF-Wxt0GptNDwnTtMmxD9ADekMaQ-KUZ3g").build()

app.add_handler(CommandHandler("hello", hello))

app.run_polling()