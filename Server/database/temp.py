import sqlite3

db = sqlite3.connect('app.db')
cursor = db.cursor()

table_list = ["User", "Election", "Candidate"]

username = "Narendra Modi"

address = "0x53402e9C5077CD22dC2d3D7a10cCc1747a6feA12"

# db.execute("CREATE TABLE User ( ID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT NOT NULL, Password_hash TEXT NOT NULL, is_voted TEXT NOT NULL DEFAULT 'False', is_admin TEXT NOT NULL DEFAULT 'False', Public_key TEXT DEFAULT '' , Private_key TEXT DEFAULT '' )")
# db.commit()

# db.execute("INSERT INTO User (Username, Password_hash) values ('Admin@test.com','pbkdf2:sha256:150000$3M545WmW$1952fbc9da6f88e438dd5de45e0338c798996786e86be81e04612969cb688124')")
# db.commit()

# db.execute("INSERT INTO User (Username, Password_hash) values ('Public@test.com','pbkdf2:sha256:150000$j0HDzNrl$a617bdefcda2a64f10569d1cdd6576dd86f57372def825d58bf000c0bef319f9')")
# db.commit()

for i in range(1, 5):
    db.execute(
        "UPDATE Candidate SET Public_key = '', Private_key='' WHERE ID = {}".format(i))
    db.commit()

for i in range(1, 3):
    db.execute(
        "UPDATE User SET Public_key = '', Private_key='' WHERE ID = {}".format(i))
    db.commit()

db.execute(
    "UPDATE User SET Public_key = '0xF93b1B980a3C6FBa1Bd21D45D7D4d32f4Acc2B0e', Private_key='157d063e7e98504e33db7ec7d4f7331f8915acf6f8188bfb26dca9489af9f934' WHERE ID = 1")
db.commit()

# db.execute("ALTER TABLE User DROP COLUMN Private_key, Public_key")
# TEXT DEFAULT ''")

# db.execute("DELETE FROM Candidate WHERE ID = '2' ")

# data = db.execute("SELECT Public_key FROM User WHERE Username = '{}'".format(
#     username)).fetchone()


# data = ''.join(data)

# def get_candidate_key(username):
#     data = db.execute(
#         "SELECT Public_key FROM Candidate WHERE Candidate_name = '{}'".format(username)).fetchone()
#     data = ''.join(data)
#     return data

# for data in table_list:
#     query = "PRAGMA table_info('{}')".format(data)
#     cursor.execute(query)
#     data = cursor.fetchall()
#     print(data)

# db.execute("DROP TABLE Election")
# db.commit()

# def get_candidate(address):
#     data = db.execute(
#         "SELECT Candidate_name FROM Candidate WHERE Public_key = '{}'".format(address)).fetchone()
#     data = ''.join(data)
#     return data


# data = db.execute("SELECT * FROM User").fetchall()
# print(data)

# print(get_candidate_key(username))

# def convert(data_1, data_2):

#     res_dct = {}
#     temp_dct = {}
#     test_keys = [x[1] for x in data_1]
#     for x in data_2:
#         test_values = [x]
#         for j in range(len(test_values)):

#             for i in range(len(test_keys)):
#                 temp_dct[test_keys[i]] = test_values[j][i]
#                 print(temp_dct)

#             res_dct[x[0]] = temp_dct
#             temp_dct = {}
#             # print(res_dct)

#     return res_dct


# def view(table):

#     data_1 = db.cursor().execute("PRAGMA table_info({})".format(table)).fetchall()
#     data_2 = db.execute("SELECT * FROM {}".format(table)).fetchall()
#     # print(data_1, data_2)
#     print(convert(data_1, data_2))


# view("candidate")
# def set_voter_key(username, address, private_key):
#     db.execute(
#         "UPDATE User SET Public_key ='{}', Private_key = '{}' WHERE Username = '{}'".format(address, private_key, username))
#     db.commit()


# def get_private_key(username):
#     data = db.execute(
#         "SELECT Private_key FROM User WHERE Username = '{}'".format(username)).fetchone()
#     data = ''.join(data)
#     return data


# set_voter_key('Public@test.com', '0xEbc5278aD4684D795437780B5d078552A885579B',
#               '0x1d3951955b0b43a663230434573c52568df90446a639eaffcedc2872b13066e1')
# print(get_private_key('Public@test.com'))
