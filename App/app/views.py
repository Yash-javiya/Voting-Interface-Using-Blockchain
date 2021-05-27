from datetime import datetime
import json

import requests
from flask import abort, redirect, render_template, url_for, jsonify, request

from app import app

CONNECTED_ADDRESS = "http://127.0.0.1:8000"


@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return render_template("Public/error.html", error=e)


@app.route('/login', methods=['POST'])
def login():
    try:
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
                res = json.loads(requests.post(
                    '{}/login'.format(CONNECTED_ADDRESS), data=data).text)

                if res["status"]:
                    return redirect(url_for('dashboard'))
                else:
                    message = res["message"]
                    return render_template('index.html', message=message)
        else:
            return 403
    except Exception as e:
        return render_template("Public/error.html", error=e)


@app.route('/register', methods=['POST'])
def register():
    try:
        username = password = None
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if username is None:
                return render_template('index.html', message="Enter Username!!!!")
            elif password is None:
                return render_template('index.html', message="Enter Password!!!")
            elif not request.form.get('cpassword') == password:
                return render_template('index.html', message="Password dosen't match!!!")
            else:
                res = json.loads(requests.post(
                    '{}/registerUser'.format(CONNECTED_ADDRESS)).text)

            if res["status"]:
                return redirect(url_for('dashboard'))
            else:
                message = res["message"]
                return render_template('index.html', message=message)
        else:
            return 403
    except Exception as e:
        return render_template("Public/error.html", error=e)


@app.route('/logout')
def logout():
    try:
        return redirect(url_for('index'))
    except Exception as e:
        return render_template("Public/error.html", error=e)


def fetch_voter(username):
    try:
        data = {"username": username}
        voter = json.loads(requests.post(
            '{}/fetch_voter'.format(CONNECTED_ADDRESS), data=data).text)

        return voter
    except Exception as e:
        return render_template("Public/error.html", error=e)


def fetch_candidate(id):
    try:
        data = {"id": id}
        voter = json.loads(requests.post(
            '{}/fetch_cnadidate'.format(CONNECTED_ADDRESS), data=data).text)
        return voter
    except Exception as e:
        return render_template("Public/error.html", error=e)


def fetch_voters():
    try:
        voter = json.loads(requests.post(
            '{}/fetch_voters'.format(CONNECTED_ADDRESS)).text)
        return voter
    except Exception as e:
        return render_template("Public/error.html", error=e)


def fetch_candidates():
    try:
        data = {"table_name": "candidate"}
        candidate = json.loads(requests.post(
            '{}/view_data'.format(CONNECTED_ADDRESS), data=data).text)
        for i in range(1, 5):
            id = "{}".format(i)
            candidate[id]['File_name'] = "img/{}.svg".format(
                candidate[id]['Political_party'])
        return candidate
    except Exception as e:
        return render_template("Public/error.html", error=e)


@ app.route('/voter')
def voter():
    try:
        candidate = fetch_candidates()
        voter = fetch_voter("Public@test.com")
        return render_template('Public/templates/voting.html', Voter=voter, candidates=candidate)
    except Exception as e:
        return render_template("Public/error.html", error=e)


@ app.route('/regvote', methods=['POST'])
def regvote():
    try:
        if request.method == 'POST':

            voteparty = request.form['voteBtn']

            voter = fetch_voter("Public@test.com")

            candidate = fetch_candidates()

            for i in range(1, 5):
                id = "{}".format(i)
                if candidate[id]['Political_party'] == voteparty:
                    candidate = candidate[id]
                    break

            return render_template('Public/templates/confirmvote.html', candidate=candidate, Voter=voter)
        else:
            return 403
    except Exception as e:
        return render_template("Public/error.html", error=e)


@ app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    try:
        candidate = fetch_candidates()
        voter = fetch_voter("Public@test.com")
        return render_template('public/Dashboard.html',
                               title='Voting Interface',
                               Voter=voter, candidates=candidate)
    except Exception as e:
        return render_template("Public/error.html", error=e)


@ app.route('/change')
def change():
    try:
        return redirect(url_for('dashboard'))
    except Exception as e:
        return render_template("Public/error.html", error=e)


@ app.route('/submit', methods=['POST'])
def submitVote():
    try:
        vote_object = {
            'voterName': request.form["voterName"],
            'voterId': request.form["voterId"],
            'candidateName': request.form["candidateName"],
            'candidateParty': request.form["candidateParty"]
        }
        # new_tx_address = "{}/new_transaction".format(CONNECTED_ADDRESS)
        data = json.loads(requests.post(
            "{}/do_voting".format(CONNECTED_ADDRESS), data=vote_object).text)
        return viewVote(data)

    except Exception as e:
        return render_template("Public/error.html", error=e)


@ app.route('/viewVote/<message>', methods=["GET", "POST"], defaults={'message': ''})
def viewVote(message):
    return render_template('Public/templates/viewVote.html',
                           title='Voting Interface',
                           message_action=message)


# routes for admin
@ app.route('/admin')
@ app.route('/admin/login')
def adminLogin():
    try:
        # if request.method == 'POST':
        #     AdminId = request.form.get('adminId')
        #     Password = request.form.get('adminPwd')
        #     if Password == 'test@123' and AdminId == 'Admin':
        #         return render_template('admin/dashboard.html')
        #     else:
        #         message = 'Incorrect id or password'
        #         return render_template('admin/login.html', message=message)
        # abort(403, 'Acess Denide contect organizer!!!')
        data = json.loads(requests.post(
            '{}/get_election_data'.format(CONNECTED_ADDRESS)).text)
        return render_template('Admin/Dashboard.html', data=data)
    except Exception as e:
        return render_template("Admin/error.html", error=e)


@ app.route('/admin/election', methods=['GET', 'POST'])
def election():
    try:
        data = json.loads(requests.post(
            '{}/get_election_data'.format(CONNECTED_ADDRESS)).text)

        if data['state'] == 'Election Not Started':
            url = '/admin/start_election'
            value = 'Start Election'
            type = 'success'
        elif data['state'] == 'Election Running':
            url = '/admin/end_election'
            value = 'End Election'
            type = 'danger'
        elif data['state'] == 'Election Ended':
            url = '/admin/show_result'
            value = 'Show Result'
            type = 'primary'

        button = {
            "url": url,
            "value": value,
            "type": type
        }

        data["button"] = button

        return render_template("Admin/templates/election.html", data=data)
    except Exception as e:
        return render_template("Admin/error.html", error=e)


def election_message(message):
    try:
        data = json.loads(requests.post(
            '{}/get_election_data'.format(CONNECTED_ADDRESS)).text)

        if data['state'] == 'Election Not Started':
            url = '/admin/start_election'
            value = 'Start Election'
            type = 'success'
        elif data['state'] == 'Election Running':
            url = '/admin/end_election'
            value = 'End Election'
            type = 'danger'
        elif data['state'] == 'Election Ended':
            url = '/admin/show_result'
            value = 'Show Result'
            type = 'primary'

        button = {
            "url": url,
            "value": value,
            "type": type
        }

        data["button"] = button

        return render_template("Admin/templates/election.html", data=data, message=message)
    except Exception as e:
        return render_template("Admin/error.html", error=e)


@ app.route('/admin/action')
def action():
    try:
        candidates = fetch_candidates()
        voters = fetch_voters()

        return render_template("Admin/templates/action.html", voters=voters, candidates=candidates)
    except Exception as e:
        return render_template("Admin/error.html", error=e)


def action_message(message):
    try:
        candidates = fetch_candidates()
        voters = fetch_voters()
        return render_template("Admin/templates/action.html", voters=voters, candidates=candidates, message_action=message)
    except Exception as e:
        return render_template("Admin/error.html", error=e)


@ app.route('/admin/genrate/<table>', methods=['POST'])
def genrate(table):
    try:
        if request.method == 'POST':
            if table == 'voter':
                data = {"username": request.form[table]}
                voter = json.loads(requests.post(
                    '{}/genrate_voter_id'.format(CONNECTED_ADDRESS), data=data).text)
                return action_message(voter)
            elif table == 'candidate':
                data = {"username": request.form[table]}
                candidate = json.loads(requests.post(
                    '{}/genrate_candidate_id'.format(CONNECTED_ADDRESS), data=data).text)
                return action_message(candidate)
        else:
            return 403
    except Exception as e:
        return render_template("Admin/error.html", error=e)


@ app.route('/admin/add/<table>', methods=['POST'])
def add(table):
    try:
        if request.method == 'POST':
            if table == 'voter':
                data = {"username": request.form[table]}
                voter = json.loads(requests.post(
                    '{}/add_voter'.format(CONNECTED_ADDRESS), data=data).text)
                return action_message(voter)
            elif table == 'candidate':
                data = {"username": request.form[table]}
                candidate = json.loads(requests.post(
                    '{}/add_candidate'.format(CONNECTED_ADDRESS), data=data).text)
                return action_message(candidate)
        else:
            return 403
    except Exception as e:
        return render_template("Admin/error.html", error=e)


@ app.route('/admin/update/<table>', methods=['POST'])
def update(table):
    try:
        if request.method == 'POST':
            if table == 'voter':
                data = {"username": request.form[table]}
                voter = json.loads(requests.post(
                    '{}/update_voter'.format(CONNECTED_ADDRESS), data=data).text)
                return voter
            elif table == 'candidate':
                data = {"username": request.form[table]}
                candidate = json.loads(requests.post(
                    '{}/update_cadidate'.format(CONNECTED_ADDRESS), data=data).text)
                return candidate
        else:
            return 403
    except Exception as e:
        return render_template("Admin/error.html", error=e)


@ app.route('/admin/delete/<table>', methods=['POST'])
def delete(table):
    try:
        if request.method == 'POST':
            if table == 'voter':
                data = {"username": request.form[table]}
                voter = json.loads(requests.post(
                    '{}/delete_voter'.format(CONNECTED_ADDRESS), data=data).text)
                return voter
            elif table == 'candidate':
                data = {"username": request.form[table]}
                candidate = json.loads(requests.post(
                    '{}/delete_candidate'.format(CONNECTED_ADDRESS), data=data).text)
                return candidate
        else:
            return 403
    except Exception as e:
        return render_template("Admin/error.html", error=e)


@ app.route('/admin/start_election', methods=['POST'])
def start_election():
    try:
        message = json.loads(requests.post(
            '{}/start_election'.format(CONNECTED_ADDRESS)).text)
        return election_message(message)
    except Exception as e:
        return render_template("Admin/error.html", error=e)


@ app.route('/admin/end_election', methods=['POST'])
def end_election():
    try:
        message = json.loads(requests.post(
            '{}/end_election'.format(CONNECTED_ADDRESS)).text)
        return election_message(message)
    except Exception as e:
        return render_template("Admin/error.html", error=e)


@ app.route('/admin/show_result', methods=['POST'])
def show_result():
    try:
        message = json.loads(requests.post(
            '{}/show_result'.format(CONNECTED_ADDRESS)).text)
        return election_message(message)
    except Exception as e:
        print(e)
        return render_template("Admin/error.html", error=e)
