import sqlite3 as sql
import time

con = sql.connect("players.db")


def save_to_db(nick, glucose, curr_time):
    cur = con.cursor()
    cur.execute(
        "INSERT INTO players(nick, glucose, time) VALUES(?, ?, ?)",
        (nick, glucose, curr_time),
    )
    con.commit()
    pass


def initialize_db():
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS players(nick, glucose, time)")
    pass


if __name__ == "__main__":
    initialize_db()

    while True:
        # TODO: nickname checker (is a string, has enough characters)
        nick = input("Nickname: ")
        if not isinstance(nick, str):
            print("nick must be a string")

        try:
            # TODO: glucose checker (is in obvious range)
            glucose = float(input("Glucose: "))
        except ValueError:
            print("glucose must be a float")

        save_to_db(nick, glucose, time.ctime())
