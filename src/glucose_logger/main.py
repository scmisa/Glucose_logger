import sqlite3 as sql
import time
import tkinter as tk

con = sql.connect("players.db")
root = tk.Tk()


# Show the data in the database in another tkinter window
def show_data():
    top = tk.Toplevel()
    top.title("Data")
    cur = con.cursor()
    cur.execute("SELECT * FROM players")
    data = cur.fetchall()
    for row in data:
        label = tk.Label(top, text=row)
        label.pack()


def save_to_db(nick, glucose, curr_time):
    cur = con.cursor()
    cur.execute(
        "INSERT INTO players(nick, glucose, time) VALUES(?, ?, ?)",
        (nick, glucose, curr_time),
    )
    con.commit()

    # Check if the "Show data" button should be displayed
    cur.execute("SELECT COUNT(*) FROM players")
    count = cur.fetchone()[0]
    if count > 0 and show_button.winfo_ismapped() == 0:
        show_button.pack()

    # Refresh the data window if it is open
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel) and widget.title() == "Data":
            widget.destroy()
            show_data()
            break


def initialize_db():
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS players(nick, glucose, time)")


def check_glucose(glucose):
    try:
        glucose_value = float(glucose)
        if glucose_value < 20 or glucose_value > 600:
            return "Glucose is not in range"
    except ValueError:
        return "Glucose is not a number"
    return None


def check_nick(nick):
    if nick == "":
        return "Nickname is empty"
    elif len(nick) < 2:
        return "Nickname is too short"
    else:
        return None


def validate_inputs(*args):
    nick = nick_var.get()
    glucose = glucose_var.get()

    nick_error = check_nick(nick)
    glucose_error = check_glucose(glucose)

    if nick_error:
        nick_error_label.config(text=nick_error)
    else:
        nick_error_label.config(text="")

    if glucose_error:
        glucose_error_label.config(text=glucose_error)
    else:
        glucose_error_label.config(text="")

    if nick_error or glucose_error:
        save_button["state"] = "disabled"
    else:
        save_button["state"] = "active"


def main():
    global \
        save_button, \
        nick_var, \
        glucose_var, \
        nick_error_label, \
        glucose_error_label, \
        show_button

    root.geometry("500x300")
    root.title("Glucose Logger")

    label = tk.Label(root, text="Glucose Logger", font=("Arial", "20"))
    label.pack(padx=20, pady=20)

    label_nick = tk.Label(root, text="Nickname: ", font=("Arial", "8"))
    label_nick.pack()

    nick_var = tk.StringVar()
    nick_var.trace("w", validate_inputs)
    input_nick = tk.Entry(root, textvariable=nick_var)
    input_nick.pack()

    nick_error_label = tk.Label(root, text="", font=("Arial", "8"), fg="red")
    nick_error_label.pack()

    label_g = tk.Label(root, text="Glucose: ", font=("Arial", "8"))
    label_g.pack()

    glucose_var = tk.StringVar()
    glucose_var.trace("w", validate_inputs)
    input_glucose = tk.Entry(root, textvariable=glucose_var)
    input_glucose.pack()

    glucose_error_label = tk.Label(root, text="", font=("Arial", "8"), fg="red")
    glucose_error_label.pack()

    save_button = tk.Button(
        root,
        text="Save",
        command=lambda: save_to_db(nick_var.get(), glucose_var.get(), time.ctime()),
        state="disabled",
    )
    save_button.pack()

    # Initialize the "Show data" button but don't pack it yet
    show_button = tk.Button(root, text="Show data", command=show_data)

    # Check if database is empty
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM players")
    count = cur.fetchone()[0]
    label_no_data = None

    if count > 0:
        show_button.pack()
        if label_no_data:
            label_no_data.destroy()
    else:
        label_no_data = tk.Label(root, text="No data in database")
        label_no_data.pack()

    root.mainloop()


if __name__ == "__main__":
    initialize_db()
    main()
