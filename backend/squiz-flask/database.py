import sqlite3
import os


def connect():
    """Makes connection to database.

    Returns: Tuple(connection, cursor)
    """
    new_db = not os.path.exists("database.db")
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    if new_db:
        cur.execute(
            "CREATE TABLE games "
            "("
            "id INTEGER PRIMARY KEY, "
            "username TEXT, "
            "game TEXT, "
            "correct INTEGER, "
            "inputed INTEGER, "
            "result INTEGER, "
            "time INTEGER"
            ")"
        )
        con.commit()
    return con, cur


def close(con: sqlite3.Connection, cur: sqlite3.Cursor):
    cur.close()
    con.close()

class connection:
    def __enter__(self):
        self.con, self.cur = connect()
        return self.cur
    def __exit__(self, *args, **kwargs):
        self.con.commit()
        close(self.con, self.cur)