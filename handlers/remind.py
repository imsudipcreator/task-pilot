import time
from utils.reminder import schedule_reminder
from database import Database
from utils import parse_time_str
from telegram import Update
from telegram.ext import ContextTypes
from decorators import registered_only


@registered_only
async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or context.args[0] == "help":
        help_text = """
        Usage: 
        /remind help - Show this message
        /remind after <time> <message> - Set a reminder
        /remind list - List all reminders
        /remind delete <id> - Delete a reminder
        """
        await update.message.reply_text(help_text)
        return

    sub_command = context.args[0]
    db = Database()

    if sub_command == "after":
        if len(context.args) < 3:
            await update.message.reply_text("Usage: /remind after <time> <message>")
            return
        time_str = context.args[1]
        message = " ".join(context.args[2:])

        try:
            delay = parse_time_str(time_str)
        except:
            await update.message.reply_text("Invalid time format")
            return

        remind_at = int(time.time()) + delay

        reminder_id = db.add_reminder(update.effective_user.id, message, remind_at)

        schedule_reminder(
            context.job_queue, reminder_id, update.effective_chat.id, remind_at, message
        )
        await update.message.reply_text(f"Reminder set successfully for {time_str}")

    elif sub_command == "list":
        reminders = db.get_reminders(update.effective_user.id)
        if not reminders:
            await update.message.reply_text("No reminders found")
            return
        for reminder in reminders:
            await update.message.reply_text(reminder[1])
        return
    elif sub_command == "delete":
        if len(context.args) < 2:
            await update.message.reply_text("Usage: /remind delete <id>")
            return
        reminder_id = int(context.args[1])
        if not db.delete_reminder(reminder_id):
            await update.message.reply_text(f"Reminder {reminder_id} not found")
            return
        await update.message.reply_text(f"Reminder {reminder_id} deleted successfully")
        return
    else:
        await update.message.reply_text("Invalid subcommand. Use /remind help")
