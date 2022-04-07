import os
import sys
import logging
import shutil
import datetime
from dotenv import load_dotenv
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from flask import render_template
#from flask_sqlalchemy import SQLAlchemy
import models


status = None

#logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S', filename='app.log', format='[%(asctime)s][%(levelname)s] %(message)s', level=logging.DEBUG)
logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S', format='[%(asctime)s][%(levelname)s] %(message)s', level=logging.DEBUG, stream=sys.stdout)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chiave segreta ma non molto'    #usata da alcuni moduli quindi la creo anche se per ora non serve
load_dotenv(os.path.join( os.getenv('HOME', '.'), '.env')) #load extra env variables from custom .env file (not in repo)
models.setup_db(app)
logging.debug(f'config: {app.config}')    
logging.debug(f'env: {os.environ}')


@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/index')
def index():
    content = 'test content'
    return render_template("index.html", data=content, title='Pint of colors - index')

@app.route('/save', methods = ['POST'])
def save():
    try:
        if request.method == 'POST':
            logging.debug(f'saving data: {request.form}')
            user = request.form['user']
            color_name = request.form['color_name']
            color_value = request.form['color_value']
            
            c = models.Color(user, color_name, color_value)
            c.insert()

            return {'result':'ok'}
        else:
            return {'result':'error'}
    except Exception as e:
        logging.exception('error saving data')
        return {'result':'error'}

@app.route('/create')
def create():
    try:
        models.db_drop_and_create()
        return 'db created'
    except:
        logging.exception('error creating db')
        return 'error creating db'

@app.route('/log')
def log():
    logtype = 'server'
    content = ''
    try:
        platform = os.getenv('WEB_PLATFORM')
        if platform == 'PYTHONANYWHERE_MYSQL':
            logname = f'{os.getenv("LOGNAME")}.pythonanywhere.com.{logtype}.log'
            f = open(f'/var/log/{logname}', 'r')
            content = f.readlines()
            f.close()
    except:
        logging.exception('error reading log')
        content = 'error reading log'
    
    return render_template("log.html", data=content, title='Pint of colors - log')

@app.route('/ping')
def ping():
    return 'Pong'

if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    host = "127.0.0.1"
    debug = True
    logging.info(f'starting {host}:{port} with debug={debug}')
    app.run(host=host, port=port, debug = debug)
    

