from datetime import datetime
import json

import requests
from flask import abort, redirect, render_template, request, url_for

from app import app

CONNECTED_ADDRESS = "http://127.0.0.1:8000"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/voterlogin', methods=['POST'])
def voterlogin():
    username = password = None
    if request.method == 'POST':
        data = {
            "username": request.form.get('username'),
            "password": request.form.get('password')
        }
        if data["username"] is None:
            return render_template('index.html', message="Enter Username!!!!")
        elif data["password"] is None:
            return render_template('index.html', message="Enter Password!!!")
        else:
            res = requests.post(
                '{}/login'.format(CONNECTED_ADDRESS), data=data)
            return res.text
    else:
        return 403


@app.route('/login/<int:code>')
def login(code):
    if code == 204:
        message = "User Dosen't Exists!!!"
        return render_template('index.html', message=message)
    elif code == 203:
        message = 'Incorrect Password'
        return render_template('index.html', message=message)
    elif code == 202:
        return redirect(url_for('dashboard'))
    else:
        return 401


# @app.route('/register', methods=['POST'])
# def register():
#     username = password = None
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         if username is None:
#             return render_template('index.html', message="Enter Username!!!!")
#         elif password is None:
#             return render_template('index.html', message="Enter Password!!!")
#         elif not request.form.get('cpassword') == password:
#             return render_template('index.html', message="Password dosen't match!!!")
#         else:
#             r = requests.post('{}/addUser'.format(CONNECTED_ADDRESS))
#             return r.text
#     else:
#         return 403


# @app.route('/regi/<int:code>')
# def regi(code):
#     if code == 205:
#         message = "User Already Exists!!!"
#         return render_template('', message=message)
#     elif code == 202:
#         message = 'Sucessfully Loggged in'
#         return render_template('', message=message)
#     else:
#         return 401


@app.route('/logout')
def logout():
    return render_template('index.html')


# routes for voter
Voter = {
    'Name': 'yash javiya',
    'Id': '123'
}

candidates = [
    {
        'No': '1',
        'CandidateName': 'Modi',
        'Symbol': 'Lotus',
        'PartyName': 'BJP'
    },
    {
        'No': '2',
        'CandidateName': 'Rahul',
        'Symbol': 'Hand sign',
        'PartyName': 'Congress'
    },
    {
        'No': '3',
        'CandidateName': 'Nota',
        'Symbol': '!',
        'PartyName': 'Nota'
    }
]

votes = []


@app.route('/voter')
def voter():
    return render_template('voter/voting.html', Voter=Voter, candidates=candidates)


@app.route('/regvote', methods=['POST'])
def regvote():
    if request.method == 'POST':
        candidate = []
        voteparty = request.form['voteBtn']
        for x in candidates:
            if x.get("PartyName") == voteparty:
                candidate = x.copy()

        return render_template('voter/confirmvote.html', candidate=candidate, Voter=Voter)
    abort(403, 'Acess Denide contect organizer!!!')
    return render_template(url_for('voterlogin'))


@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    fetch_votes(123)
    return render_template('voter/dashboard.html',
                           title='Voting Interface')


@app.route('/mine')
def mine():
    requests.get("{}/mine".format(CONNECTED_ADDRESS))
    return redirect('/dashboard')


@app.route('/submit', methods=['POST'])
def submitVote():
    vote_object = {
        'voterName': request.form["voterName"],
        'voterId': request.form["voterId"],
        'candidateName': request.form["candidateName"],
        'candidateParty': request.form["candidateParty"]
    }

    new_tx_address = "{}/new_transaction".format(CONNECTED_ADDRESS)

    requests.post(new_tx_address,
                  json=vote_object,
                  headers={'Content-type': 'application/json'})

    return redirect("{}/mine".format(CONNECTED_ADDRESS))


@app.route('/viewVote', methods=["GET", "POST"])
def viewVote():
    fetch_votes(123)
    return render_template('voter/viewVote.html',
                           title='Voting Interface',
                           votes=votes,
                           readable_time=timestamp_to_string)


def timestamp_to_string(epoch_time):
    return datetime.fromtimestamp(epoch_time).strftime('%H:%M')


def fetch_votes(voterId):
    get_chain_address = "{}/chain".format(CONNECTED_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global votes
        votes = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)


# routes for admin
@app.route('/admin', methods=['POST'])
def admin():
    if request.method == 'POST':
        AdminId = request.form.get('adminId')
        Password = request.form.get('adminPwd')
        if Password == 'test@123' and AdminId == 'Admin':
            return render_template('admin/dashboard.html')
        else:
            message = 'Incorrect id or password'
            return render_template('admin/login.html', message=message)
    abort(403, 'Acess Denide contect organizer!!!')
    return render_template('index.html')

# # routes for organizer
# @app.route('/organizer', methods=['POST'])
# def organizer():

#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         if (password == '123' and username == 'test'):
#             return redirect(url_for('org_dashboard'))
#         else:
#             message = ('Incorrect Username or Password !!!!!')
#             return render_template('index.html', message=message)
#     else:
#         return render_template('index.html')

# @app.route('/orgdashboard')
# def org_dashboard():
#     organizer = {
#         'Name': 'yash javiya',
#         'Id': '123'
#     }
#     return render_template('organizer/dashboard.html', organizer=organizer)
