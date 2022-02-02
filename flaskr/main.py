import os
import time
import flask
from flask import Flask, request, render_template, redirect
from test import predict_emotion, record_to_file
from db import *
from plot import *
# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

# load the instance config, if it exists, when not testing
app.config.from_pyfile('config.py', silent=True)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass
@app.route('/', methods=["GET", "POST"])
def main_menu():
    if request.method == "POST":
        username = flask.request.values.get('uname')#get the username from form
        password = flask.request.values.get('pwd')#get the password from form
        if login(username, password) != "Login Failed": #check if uname/pwd are valid
            # uid = get_new_uid(username)
            return redirect('/predict/'+username)
    return render_template("login.html")
@app.route('/new_user', methods=["GET", "POST"])
def new_user():
    if request.method == "POST":
        firstname = flask.request.values.get('fname')#get the first name from form
        lastname = flask.request.values.get('lname')#get the last name from form
        username = flask.request.values.get('uname')  # get the username from form
        password = flask.request.values.get('pwd')  # get the password from form
        add_user(firstname, lastname, username, password)
        return redirect('/')
    return render_template("new_user.html")
@app.route('/predict/<username>', methods=["GET", "POST"])
def predict(username):
    if request.method == "POST":
        normal = 0
        manic = 0
        depressed = 0
        elated = 0
        down = 0
        emotion = predict_emotion()
        if emotion == 'normal':
            normal += 1
        elif emotion == 'manic':
            manic += 1
        elif emotion == 'depressed':
            depressed += 1
        elif emotion == 'elated':
            elated += 1
        elif emotion == 'down':
            down += 1
        emotions = []
        emotions.append(normal)
        emotions.append(manic)
        emotions.append(depressed)
        emotions.append(elated)
        emotions.append(down)
        timedate = time.strftime('%Y-%m-%d %H:%M:%S')
        description = flask.request.form.get("prediction")
        add_entry(username, description, emotions, timedate)
        return redirect('/result/' + username)
    return render_template("form.html", username=username)
@app.route('/result/<username>', methods=["GET"])
def result(username):
    eid, normal, manic, depressed, elated, down, description, date = get_user_entry(username)
    plot_map(normal, manic, depressed, elated, down, description, date)
    return redirect('/predict/'+username)