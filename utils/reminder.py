from database import Database
from telegram.ext import ContextTypes
from telegram.ext import JobQueue
import time


def schedule_reminder(
    job_queue: JobQueue, reminder_id: int, chat_id: int, remind_at: int, message: str
):
    delay = remind_at - int(time.time())

    if delay <= 0:
        return

    job_queue.run_once(
        send_reminder,
        when=delay,
        chat_id=chat_id,
        data={"id": reminder_id, "message": message},
    )


async def send_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    data = context.job.data
    message = data["message"]
    chat_id = context.job.chat_id

    await context.bot.send_message(chat_id=chat_id, text=f"Reminder: {message}")
    db = Database()
    if not db.delete_reminder(data["id"]):
        print(f"Failed to delete reminder {data['id']}")


def restore_reminders(job_queue: JobQueue) -> None:
    db = Database()
    reminders = db.get_pending_reminders()

    for reminder in reminders:

        reminder_id = reminder[0]
        chat_id = reminder[1]
        message = reminder[2]
        remind_at = reminder[3]

        schedule_reminder(job_queue, reminder_id, chat_id, message, remind_at)
