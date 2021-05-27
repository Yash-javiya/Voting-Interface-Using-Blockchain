from flask import jsonify
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import sqlite3
from sqlite3 import Error


def get_db():
    try:
        return sqlite3.connect("./database/app.db")
    except Error as e:
        print(e)
        return 500


def login(user, password):
    db = get_db()
    login = db.execute(
        "SELECT * FROM User WHERE Username = '{}'".format(user)).fetchone()
    if login is None:
        return bool(False), "User Dosen't Exists"
    else:
        if login[3] == 'True':
            return bool(False), "Already Voted"
        elif not check_password_hash(login[2], password):
            return bool(False), "Incorrect Password"
        else:
            return bool(True), "Sucessfully Loggged in"


def register(user, password):
    db = get_db()
    if db.execute("SELECT id FROM User WHERE Username = ?", (user)).fetchone() is not None:
        return bool(False), "User already Exists"
    else:
        db.execute(
            "INSERT INTO User (Username, Password_hash) VALUES (?, ?)",
            (user, generate_password_hash(password)),
        )
        db.commit()
        return bool(True), "User Successfully Registered"


def convert(data_1, data_2):
    res_dct = {}
    temp_dct = {}
    test_keys = [x[1] for x in data_1]
    for x in data_2:
        test_values = [x]
        for j in range(len(test_values)):

            for i in range(len(test_keys)):
                temp_dct[test_keys[i]] = test_values[j][i]

            res_dct[x[0]] = temp_dct
            temp_dct = {}

    return res_dct


def view(table):
    db = get_db()
    data_1 = db.cursor().execute("PRAGMA table_info({})".format(table))
    data_2 = db.execute("SELECT * FROM {}".format(table)).fetchall()
    return convert(data_1, data_2)


def get_voter(username):
    db = get_db()
    data_1 = db.cursor().execute("PRAGMA table_info('User')").fetchall()
    data_2 = db.execute(
        "SELECT * FROM User WHERE Username = '{}'".format(username)).fetchall()
    return convert(data_1, data_2)


def get_candidate(address):
    db = get_db()
    data = db.execute(
        "SELECT Candidate_name FROM Candidate WHERE Public_key = '{}'".format(address)).fetchone()
    data = ''.join(data)
    return data


def voted(address):
    db = get_db()
    db.execute(
        "UPDATE User SET is_voted = 'True' WHERE Public_key = '{}'".format(address))
    db.commit()


def get_voter_key(username):
    db = get_db()
    data = db.execute(
        "SELECT Public_key FROM User WHERE Username = '{}'".format(username)).fetchone()
    data = ''.join(data)
    return data


def set_voter_key(username, address, private_key):
    db = get_db()
    db.execute(
        "UPDATE User SET Public_key ='{}', Private_key = '{}' WHERE Username = '{}'".format(address, private_key, username))
    db.commit()


def get_candidate_key(username):
    db = get_db()
    data = db.execute(
        "SELECT Public_key FROM Candidate WHERE Candidate_name = '{}'".format(username)).fetchone()
    data = ''.join(data)
    return data


def set_candidate_key(username, address, private_key):
    db = get_db()
    db.execute(
        "UPDATE Candidate SET Public_key ='{}', Private_key = '{}' WHERE Candidate_name = '{}'".format(address, private_key, username))
    db.commit()


def get_all_voters():
    db = get_db()
    data_1 = db.cursor().execute("PRAGMA table_info('User')").fetchall()
    data_2 = db.execute("SELECT * FROM User").fetchall()
    return convert(data_1, data_2)


def get_all_candidate():
    db = get_db()
    data_1 = db.cursor().execute("PRAGMA table_info('Candidate')").fetchall()
    data_2 = db.execute("SELECT * FROM Candidate").fetchall()
    return convert(data_1, data_2)


def get_private_key(username):
    db = get_db()
    data = db.execute(
        "SELECT Private_key FROM User WHERE Username = '{}'".format(username)).fetchone()
    data = ''.join(data)
    return data
