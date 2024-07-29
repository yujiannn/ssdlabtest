from flask import Flask, request, render_template_string, redirect, url_for, session
import uuid
import bcrypt

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a secure secret key in a real application
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 60  # 1 minute timeout

# Hardcoded username and hashed password
USERNAME = 'student'
PASSWORD_HASH = bcrypt.hashpw('2202855'.encode('utf-8'), bcrypt.gensalt())

def verify_password(password):
    return bcrypt.checkpw(password.encode('utf-8'), PASSWORD_HASH)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and verify_password(password):
            session['username'] = USERNAME
            session['session_id'] = str(uuid.uuid4())
            session.permanent = True
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(LOGIN_PAGE_TEMPLATE, error='Invalid username or password.')
    return render_template_string(LOGIN_PAGE_TEMPLATE)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template_string(DASHBOARD_TEMPLATE, session_id=session['session_id'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

LOGIN_PAGE_TEMPLATE = '''
<!doctype html>
<title>Login</title>
<h1>Login</h1>
<form method=post>
    <input type=text name=username placeholder="Username" required>
    <input type=password name=password placeholder="Password" required>
    <input type=submit value=Login>
</form>
{% if error %}
<p style="color:red;">{{ error }}</p>
{% endif %}
'''

DASHBOARD_TEMPLATE = '''
<!doctype html>
<title>Dashboard</title>
<h1>Welcome!</h1>
<p>Your session ID: {{ session_id }}</p>
<a href="/logout">Logout</a>
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
