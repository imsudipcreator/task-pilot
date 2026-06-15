from telegram import Update
from telegram.ext import ContextTypes
from database import Database


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db = Database()
    message = db.register_user(
        update.effective_user.id,
        update.effective_user.first_name,
    )
    await update.message.reply_text(message)
