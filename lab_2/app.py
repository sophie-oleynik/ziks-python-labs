from flask import Flask, render_template, request, session, redirect, url_for, g
from markupsafe import escape

# Connect to Local Database
import sqlite3
conn = sqlite3.connect(".\database.db", check_same_thread=False)
c = conn.cursor()


app = Flask(__name__)
app.secret_key = b"APP_SECRET_KEY"

# 1. auth user (login, password, role)
# 2. user roles
# 3. secured notes for users with diff roles

@app.route('/')
def index():
    if 'login' in session:
        return render_template('index.html', name=session['login'], role=session['role'])
    return redirect(url_for('login'))


@app.route('/data')
def data():
    if 'login' in session:
        cmd = 'SELECT * FROM Notes ;'
        c.execute(cmd)
        data = []
        for (id, content, access_role) in c.fetchall():
            data.append({"id": id, "content": content, "access_role": access_role})
        return { 'status': 'OK', "data": data }
    return {'status': 'ERROR'}


@app.route('/data/<id>')
def dataById(id):
    if 'login' in session:
        cmd = 'SELECT * FROM Notes WHERE id=' + id + ';'
        c.execute(cmd)
        data = []
        for (id, content, access_role) in c.fetchall():
            if access_role >= int(session['role']):
                data.append({"id": id, "content": content,
                            "access_role": access_role})
            else:
                addLog('Access to data ' + str(id) + ' Denied for ' + session['login'], 'data')
                return {'status': 'ERROR', 'message': 'Access Denied'}
        return {'status': 'OK', "data": data}
    return {'status': 'ERROR'}


@app.route('/logs')
def logs():
    if 'login' in session:
        return render_template('logs.html')
    return redirect(url_for('login'))


@app.route('/data/logs')
def getLogs():
    if 'login' in session:
        cmd = 'SELECT * FROM Logs ;'
        c.execute(cmd)
        data = []
        for (id, message, type) in c.fetchall():
            data.append({"id": id, "message": message,
                         "type": type})
        return {'status': 'OK', "data": data}
    return {'status': 'ERROR'}


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = request.json
        cmd = 'SELECT id, login, password, role_id FROM Users WHERE login="%s' % form['login'] + '";'
        c.execute(cmd)
        users = c.fetchall()
        # error if user already exist
        if len(users) > 0:
            addLog('Registration error: ' + users[0][1] + ' already exist', 'auth')
            return {"status": "ERROR", "message": "User already registered"}
        # else add user to database and log in
        session['login'] = form['login']
        cmd = 'INSERT INTO Users(login, password, role_id) VALUES ("%s' % form['login'] + '", "%s' % form['password'] + '", "%x' % int(form['role_id']) + '");'
        c.execute(cmd)
        conn.commit()
        session['role'] = form['role_id']
        addLog('Registration Success: user ' + form['login'] + ' created', 'auth')
        addLog('Login Success: user ' + form['login'] + ' loged in', 'auth')
        return {"status": "OK"}
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.json
        cmd = 'SELECT id, login, password, role_id FROM Users WHERE login="%s' % form[
            'login'] + '" AND password="%s' % form['password'] + '";'
        c.execute(cmd)
        users = c.fetchall()
        # log user if found one
        if len(users) > 0:
            session['login'] = form['login']
            session['role'] = users[0][3]
            addLog('Login Success: user ' + form['login'] + ' loged in', 'auth')
            return {"status": "OK"}
        # error if no user is found
        addLog('Login error: user ' + form['login'] + ' not found', 'auth')
        return {"status": "ERROR", "message": "User not found"}
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('login', None)
    session.pop('role', None)
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


# Close Database connection
@app.teardown_appcontext
def close_connection(exception):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()


def addLog(message, type):
    cmd = 'INSERT INTO Logs(message, type) VALUES ("%s' % message + \
        '", "%s' % type + '");'
    c.execute(cmd)
    conn.commit()
