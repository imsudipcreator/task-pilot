import sqlite3
import time


class Database:
    def __init__(self) -> None:
        self.db_path = "data/bot.db"

    def init_db(self) -> None:
        # self.cursor.execute(
        #     """
        #     CREATE TABLE IF NOT EXISTS users (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         user_id INTEGER NOT NULL UNIQUE,
        #         username TEXT NOT NULL,
        #         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        #     )
        # """
        # )
        # self.conn.commit()
        # self.conn.close()

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    username TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    todo_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    remind_at INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            conn.commit()

    # ---------------------- User Methods ----------------------

    def is_registered(self, user_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))

            return cursor.fetchone() is not None

    def register_user(self, user_id: int, username: str) -> str:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO users
                (user_id, username)
                VALUES (?, ?)
                """,
                (user_id, username),
            )
        return "User registered successfully"

    # ---------------------- Todo Methods ----------------------

    def add_todo(self, user_id: int, todo_text: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO todos (user_id, todo_text)
                VALUES (?, ?)
                """,
                (user_id, todo_text),
            )
            conn.commit()
            return cursor.lastrowid

    def get_todos(self, user_id: int) -> list[tuple[int, str]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, todo_text FROM todos WHERE user_id = ?", (user_id,)
            )
            return cursor.fetchall()

    def mark_done(self, todo_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM todos WHERE id = ?",
                (todo_id,),
            )
            conn.commit()
        return cursor.rowcount != 0

    # ---------------------- Reminder Methods ----------------------
    def add_reminder(self, user_id: int, message: str, remind_at: int) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO reminders (user_id, message, remind_at)
                VALUES (?, ?, ?)
                """,
                (user_id, message, remind_at),
            )
            conn.commit()
            return cursor.lastrowid

    def get_reminders(self, user_id: int) -> list[tuple[int, str, int]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, message, remind_at FROM reminders WHERE remind_at > ? AND user_id = ?",
                (int(time.time()), user_id),
            )
            return cursor.fetchall()

    def get_pending_reminders(self) -> list[tuple[int, str, int]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, user_id, message, remind_at FROM reminders WHERE remind_at > ?",
                (int(time.time()),),
            )
            return cursor.fetchall()

    def delete_reminder(self, reminder_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM reminders WHERE id = ?",
                (reminder_id,),
            )
            conn.commit()
            return cursor.rowcount != 0
