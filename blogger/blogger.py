#impors
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
                  abort, render_template, flash

#Configure database
DATABASE= 'flaskr.db'
DEBUG = True
SECRET_KEY='my-precious'
USERNAME = 'admin'
PASSWORD = 'admin'

#create flask app
app = Flask(__name__)
app.config.from_object(__name__)

def db_init():
   """Creates database tables based on schema.sql. """
   with app.app_context():
       db = get_db()
       with app.open_resource('model/schema.sql', mode='r') as f:
           db.cursor().executescript(f.read())
       db.commit()
   

def get_db():
   """Opens a new database connection."""
   if not hasattr(g, 'sqlite-db'):
      g.sqlite_db = db_connect()
   return g.sqlite_db

def db_connect():
   """Connects and initializes the database."""
   rv = sqlite3.connect(app.config['DATABASE'])
   rv.row_factory = sqlite3.Row
   return rv


if __name__ == '__main__':
    db_init()


