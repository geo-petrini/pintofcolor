import os
import sys
import logging
import shutil
import datetime
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from flask import render_template
#from flask_sqlalchemy import SQLAlchemy
import models


status = None

#logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S', filename='app.log', format='[%(asctime)s][%(levelname)s] %(message)s', level=logging.DEBUG)
logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S', format='[%(asctime)s][%(levelname)s] %(message)s', level=logging.DEBUG, stream=sys.stdout)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chiave segreta ma non molto'    #usata da alcuni moduli quindi la creo anche se per ora non serve

models.setup_db(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///wordcount_dev'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#db = SQLAlchemy(app)


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
        models.db_drop_and_create()
        return 'db created'
    except:
        logging.exception('error creating db')
        return 'error creating db'

@app.route('/ping')
def ping():
    return 'Pong'



    

if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="127.0.0.1", port=port, debug = True)
    

