from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "S2we43#bQ093HhopOPds221"

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT UNIQUE NOT NULL,
              password TEXT NOT NULL)""")
    conn.commit()
    conn.close()

init_db()

@app.route('/')
@app.route('/index.html')
@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index1.html', username=session['username'])
    return render_template("index.html")

@app.route('/register.html', methods=["GET", "POST"])
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register.html', error="Пользователь уже существует")
        
    
    return render_template('register.html')

@app.route('/login.html', methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['username'] = username
            return redirect(url_for('index1'))
        else:
            return "Неверное имя пользователя или пароль"
    return render_template('login.html')


@app.route('/index1')
@app.route('/index1.html')
def index1():
    if 'username' in session:
        return render_template('index1.html', username=session['username'])
    return redirect(url_for('login'))

@app.route("/logout.html")
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)