from telegram import Update
from telegram.ext import ContextTypes


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """Use the bot by following the commands:
    /start - Register yourself in the bot
    /help - Get this message
    /qr <text> - Generate a QR code for the given text
        
    /todo <command>
        add <todo> - Add a new todo
        list - List all todos
        done <id> - Mark a todo as done
        delete <id> - Delete a todo

    /remind <command>
        after <time> <message> - Set a reminder
        list - List all reminders
        delete <id> - Delete a reminder
    
    Time Format:
        10s - 10 seconds
        1m - 1 minute
        1h - 1 hour
        1d - 1 day
        1w - 1 week
        1mo - 1 month
        1y - 1 year
    """
    await update.message.reply_text(help_text)
