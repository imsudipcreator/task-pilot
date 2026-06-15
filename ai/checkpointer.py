from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


def create_checkpointer():
    conn = sqlite3.connect("data/checkpoints.db", check_same_thread=False)
    return SqliteSaver(conn)
