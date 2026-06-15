from functools import wraps
from database import Database
from telegram import Update
from telegram.ext import ContextTypes


def registered_only(func):
    @wraps(func)
    async def wrapper(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        user_id = update.effective_user.id
        db = Database()
        if not db.is_registered(user_id):
            await update.message.reply_text("Please register first with /start")
            return
        return await func(update, context, *args, **kwargs)

    return wrapper
