from database import Database
from langchain_core.runnables import RunnableConfig
from langchain.tools import tool


@tool
def get_todos(config: RunnableConfig):
    """
    Used to get all todos from the database using user id.
    Returns a list of todos.
    """
    print("[TOOL_CALLED] get_todos")
    user_id = config["configurable"]["user_id"]

    db = Database()
    todos = db.get_todos(user_id)

    return todos


@tool
def add_todo(config: RunnableConfig, todo_text: str):
    """
    Used to add a todo to the database using user id, and todo_text
    """
    print("[TOOL_CALLED] add_todo")
    user_id = config["configurable"]["user_id"]

    db = Database()
    todo_id = db.add_todo(user_id, todo_text)

    return f"Todo added successfully with id {todo_id}"


@tool
def mark_todo_done(todo_id: int):
    """
    Used to delete a todo (mark it done) from the database using todo_id
    """
    print("[TOOL_CALLED] mark_todo_done")

    db = Database()
    if not db.mark_done(todo_id):
        return f"Todo {todo_id} not found"

    return f"Todo {todo_id} is deleted successfully"
