import os
import sys
import logging
import shutil
import datetime
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from flask import render_template
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy


status = None

#logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S', filename='app.log', format='[%(asctime)s][%(levelname)s] %(message)s', level=logging.DEBUG)
logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S', format='[%(asctime)s][%(levelname)s] %(message)s', level=logging.DEBUG, stream=sys.stdout)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chiave segreta ma non molto'    #usata da alcuni moduli quindi la creo anche se per ora non serve

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///wordcount_dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

socketio = SocketIO(app)


@app.route('/')
def home():
    return redirect(url_for('index'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/index')
def index():
    content = 'test content'
    return render_template("index.html", data=content, title='Mypage - index')


@app.route('/create')
def create():
    try:
        db.create_all()
        return 'db created'
    except:
        logging.exception('error creating db')
        return 'error creating db'

@app.route('/ping')
def ping():
    return 'Pong'


class Color(db.Model):
    __tablenane__ = 'colors'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255))
    color_name = db.Column(db.String(255))
    color_code = db.Column(db.String(8))
    ts = db.Column(db.DateTime)
    
    def __init__(self, user, color_name, color_code):
        self.user = user
        self.color_name = color_name
        self.color_code = color_code
        self.ts = datetime.datetime.now()
    

if __name__ == "__main__":
    #app.run("0.0.0.0", debug = True)
    socketio.run(app, debug=True, host='0.0.0.0')

