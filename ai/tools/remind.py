from database import Database
from langchain_core.runnables import RunnableConfig
from langchain.tools import tool
import time


@tool
def get_reminders(config: RunnableConfig):
    """
    Used to get all reminders from the database using user id
    Returns a list of reminders
    """
    print("[TOOL_CALLED] get_reminders")
    user_id = config["configurable"]["user_id"]

    db = Database()
    reminders = db.get_reminders(user_id)

    return reminders


@tool
def add_reminder(config: RunnableConfig, message: str, delay: int):
    """
    Used to add a reminder to the database using user id, and delay (in seconds from current time) and message
    e.g: if current time is 10:50AM and the user asks to remind him at 11:00AM, then delay is (11:00AM - 10:50AM) = 10 minutes = 10 * 60 = 600 seconds
    Returns the reminder id
    """
    print(f"[TOOL_CALLED] add_reminder with delay: {delay} and message: {message}")
    user_id = config["configurable"]["user_id"]

    db = Database()
    reminder_id = db.add_reminder(user_id, message, int(time.time()) + delay)

    return f"Reminder added successfully with id {reminder_id}"


@tool
def delete_reminder(reminder_id: int):
    """
    Used to delete a reminder from the database using reminder id
    Returns the reminder id
    """
    print("[TOOL_CALLED] delete_reminder")
    db = Database()
    if not db.delete_reminder(reminder_id):
        return f"Reminder {reminder_id} not found"
    return f"Reminder {reminder_id} deleted successfully"
