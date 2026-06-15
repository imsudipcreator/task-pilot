from database import Database
from telegram import Update
from telegram.ext import ContextTypes
from decorators import registered_only


@registered_only
async def todo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or context.args[0] == "help":
        help_text = """
        Usage: 
        /todo help - Show this message
        /todo add <todo> - Add a new todo
        /todo list - List all todos
        /todo done <id> - Mark a todo as done
        /todo delete <id> - Delete a todo
        """
        await update.message.reply_text(help_text)
        return

    sub_command = context.args[0]

    db = Database()
    if sub_command == "add":
        if len(context.args) < 2:
            await update.message.reply_text("Please provide a todo text")
            return
        todo_text = " ".join(context.args[1:])
        db.add_todo(update.effective_user.id, todo_text)
        await update.message.reply_text(f"Added todo: {todo_text}")

    elif sub_command == "list":
        todos = db.get_todos(update.effective_user.id)
        if not todos:
            await update.message.reply_text("No todos found")
            return
        todo_list = "\n".join(
            [f"{i+1}. {todo[1]} (id: {todo[0]})" for i, todo in enumerate(todos)]
        )
        await update.message.reply_text(todo_list)

    elif sub_command == "done":
        if len(context.args) < 2:
            await update.message.reply_text("Please provide a todo to mark as done")
            return
        todo_id = int(context.args[1])
        if not db.mark_done(todo_id):
            await update.message.reply_text(f"TODO {todo_id} not found")
            return
        await update.message.reply_text(f"TODO {todo_id} is done")

    else:
        await update.message.reply_text("Invalid subcommand. Use /todo help")
