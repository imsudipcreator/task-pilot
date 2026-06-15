from database import Database
from handlers import start, help, todo, remind, ai, unknown
from utils import restore_reminders
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os

load_dotenv()


if __name__ == "__main__":
    # Initialize Application
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    # Initialize Database
    db = Database()
    db.init_db()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("todo", todo))
    app.add_handler(CommandHandler("remind", remind))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai))

    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    restore_reminders(app.job_queue)

    print("Bot started")
    app.run_polling(poll_interval=1)
