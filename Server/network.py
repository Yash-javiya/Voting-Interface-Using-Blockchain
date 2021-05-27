import json
import time
from hashlib import sha256

import requests
from flask import Flask, redirect, request, url_for, json, Response

# from blockchain import Block, Blockchain
from db import login, register, view, get_voter, voted, get_all_voters, get_all_candidate, get_candidate_key, get_private_key, get_candidate
from Web3 import Manager, Action, Function


app = Flask(__name__)

CONNECTED_ADDRESS = "http://127.0.0.1:5000"


@app.route('/')
def home():
    return "server is up and running!!!!"


@app.route('/login', methods=['POST'])
def loginUser():
    if request.method == "POST":
        function = Function()
        if function.state() == 1:
            user = request.form.get('username')
            password = request.form.get('password')

            status, message = login(user, password)

            data = {'status': status,
                    'message': message}
        elif function.state() == 0:
            data = {'status': False,
                    'message': 'Election not started Yet!!!'}
        elif function.state() == 2:
            data = {'status': False,
                    'message': 'Election Over!!!'}

        return Response(json.dumps(data))
    else:
        return 403


@ app.route("/registerUser", methods=['POST'])
def registerUser():
    if request.method == "POST":
        user = request.form.get('username')
        password = request.form.get('password')

        status, message = register(user, password)

        data = {'status': status,
                'message': message}

        return Response(json.dumps(data))
    else:
        return 403


@ app.route("/view_data", methods=['POST'])
def view_data():
    if request.method == "POST":
        Table_name = request.form.get('table_name')
        data = view(Table_name)
        return Response(json.dumps(data))
    else:
        return 403


@ app.route("/fetch_voter", methods=['POST'])
def fetch_voter():
    if request.method == "POST":
        username = request.form.get('username')
        data = get_voter(username)
        return Response(json.dumps(data))
    else:
        return 403


@app.route("/fetch_voters", methods=['POST'])
def fetch_voters():
    if request.method == "POST":
        data = get_all_voters()
        return Response(json.dumps(data))
    else:
        return 403


@app.route("/genrate_voter_id", methods=['POST'])
def genrate_voter_id():
    if request.method == "POST":
        username = request.form.get('username')
        action = Action()
        data = action.voter_generate_id(username)
        return Response(json.dumps(data))
    else:
        return 403


@app.route("/genrate_candidate_id", methods=['POST'])
def genrate_candidate_id():
    if request.method == "POST":
        username = request.form.get('username')
        action = Action()
        data = action.candidate_generate_id(username)
        return Response(json.dumps(data))
    else:
        return 403


@app.route("/add_voter", methods=['POST'])
def add_voter():
    if request.method == "POST":
        username = request.form.get('username')
        action = Action()
        data = action.voter_add_to_eth_net(username)
        return Response(json.dumps(data))
    else:
        return 403


@app.route("/add_candidate", methods=['POST'])
def add_candidate():
    if request.method == "POST":
        username = request.form.get('username')
        action = Action()
        data = action.candidate_add_to_eth_net(username)
        return Response(json.dumps(data))
    else:
        return 403


@app.route("/update_voter", methods=['POST'])
def update_voter():
    if request.method == "POST":
        return 200
    else:
        return 403


@app.route("/update_candidate", methods=['POST'])
def update_candidate():
    if request.method == "POST":
        return 200
    else:
        return 403


@app.route("/delete_voter", methods=['POST'])
def delete_voter():
    if request.method == "POST":
        return 200
    else:
        return 403


@app.route("/delete_candidate", methods=['POST'])
def delete_candidate():
    if request.method == "POST":
        return 200
    else:
        return 403


@app.route("/get_election_data", methods=['POST'])
def get_election_data():
    if request.method == "POST":
        function = Function()

        if function.state() == 0:
            state = 'Election Not Started'
        elif function.state() == 1:
            state = 'Election Running'
        elif function.state() == 2:
            state = 'Election Ended'
        else:
            state = ''

        total_voters = function.total_voter()

        total_vote_dropped = function.vote_dropped()

        data = {
            'total_voters': total_voters,
            'total_vote_dropped': total_vote_dropped,
            'state': state
        }
        return Response(json.dumps(data))
    else:
        return 403


@app.route("/start_election", methods=['POST'])
def start_election():
    manager = Manager()
    manager.start_vote()
    message = 'Election Started'
    return Response(json.dumps(message))


@ app.route("/end_election", methods=['POST'])
def end_election():
    manager = Manager()
    manager.end_vote()
    message = 'Election Ended'
    return Response(json.dumps(message))


@app.route("/do_voting", methods=['POST'])
def do_voting():
    if request.method == "POST":
        manager = Manager()
        candidate_name = request.form.get('candidateName')
        address = get_candidate_key(candidate_name)
        data = manager.do_vote(address)
        return Response(json.dumps(data))
    else:
        return 403


@app.route("/show_result", methods=['POST'])
def show_result():
    if request.method == "POST":
        manager = Manager()
        data = manager.get_result()
        address = data['_candidate']
        if hex(int(address, base=16)) == hex(0):
            message = 'No Candidate Won!!!'
        else:
            message = get_candidate(address) + 'Won !!!'

        return Response(json.dumps(message))
    else:
        return 403


# Uncomment this line if you want to specify the port number in the code
if __name__ == "__main__":
    app.run(debug=True)
