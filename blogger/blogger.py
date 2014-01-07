import sqlite3

from flask import Flask,request,session, g ,redirect,url_for, \
                  abort, render_template,flash

#Basic configuration
DATABASE = 'blogger.db'
DEBUG= True
SECRET_KEY='my_precious'
USERNAME = 'admin'
PASSWORD = 'admin'

#Create and initialize from config
app = Flask(__name__)
app.config.from_object(__name__)


def db_connect():
   """Connects and initializes the database."""
   rv = sqlite3.connect(app.config['DATABASE'])
   rv.row_factory = sqlite3.Row
   return rv

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

@app.teardown_appcontext
def close_db(error):
   """Closes the database at the end of the request."""
   if hasattr(g, 'sqlite_db'):
       g.sqlite_db.close()

@app.route('/')
def index():
    """Searches the database for entries, then displays them."""
    db = get_db()
    cur = db.execute('select title, body from entries order by id desc')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login/authentication/session management."""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """User logout/authentication/session management."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_entry():
    """Add new post to database."""
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, body) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

if __name__ == "__main__":
  db_init()
  app.run(debug=True)
