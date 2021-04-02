from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import sqlite3
from sqlite3 import Error


def get_db(db):
    try:
        return sqlite3.connect("./database/"+db+".db")
    except Error as e:
        print(e)
        return 500


def login(user, password):
    db = get_db('user')
    if db.execute("SELECT * FROM user WHERE username = ?", (user,)).fetchone() is None:
        return 204  # User Dosen't Exists
    else:
        login = db.execute(
            "SELECT * FROM user WHERE username = ?", (user,)).fetchone()
        if check_password_hash(login[2], password):
            data = {
                'voterID': '{}'.format(login[1]),
                'voterName': '{}'.format(login[0])
            }
            return 202  # , data  # Sucessfully Loggged in
        else:
            return 203  # Incorrect Password


def register(user, password):
    db = get_db('user')
    if db.execute("SELECT id FROM user WHERE username = ?", (user,)).fetchone() is not None:
        return 205  # User already Exists
    else:
        db.execute(
            "INSERT INTO user (username, password_hash) VALUES (?, ?)",
            (user, generate_password_hash(password)),
        )
        db.commit()
        return 202  # User Successfully Registered
