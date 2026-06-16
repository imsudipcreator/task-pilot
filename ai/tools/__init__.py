from .todo import get_todos, add_todo, mark_todo_done
from .time import get_current_time
from .remind import get_reminders, add_reminder, delete_reminder
from .web_search import web_search
from .wiki import search_wiki

tools = [
    get_todos,
    add_todo,
    mark_todo_done,
    get_current_time,
    get_reminders,
    add_reminder,
    delete_reminder,
    web_search,
    search_wiki,
]
