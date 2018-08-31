from flask import Flask, jsonify, request, make_response, redirect
import MySQLdb, requests
from decorators import session_lifecycle, logged_in

db = MySQLdb.connect(user='root', passwd="123", db="messenger")
db.autocommit(True)

app = Flask(__name__)


@app.route('/')
@session_lifecycle
def main():
    response = make_response(open('src/index.html').read())
    session = request.session

    return response


@app.route('/login', methods=['GET'])
@session_lifecycle
def login():
    print('redirecting')
    return redirect('https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=108510044966-mrapn31lbm6jdh58q0min0tcvo9he4q1.apps.googleusercontent.com&scope=email&redirect_uri=http://127.0.0.1:5000/google-redirect')


def find_user_by_email(email):
    cursor = db.cursor()
    cursor.execute('''
                SELECT id, login
                FROM users
                WHERE login=%s
            ''', (email,))
    return cursor.fetchall()[0]


@app.route('/google-redirect', methods=['GET'])
@session_lifecycle
def redirect_view():
    error = request.args.get('error')
    code = request.args.get('code')
    if error:
        print('error')
    else:
        response = requests.post('https://www.googleapis.com/oauth2/v4/token', json={
            'code': code,
            'client_id': '108510044966-mrapn31lbm6jdh58q0min0tcvo9he4q1.apps.googleusercontent.com',
            'client_secret': 'i2mc0JOBEZlAUNnF_A81Lxz7',
            'redirect_uri': 'http://127.0.0.1:5000/google-redirect',
            'grant_type': 'authorization_code'

        }).json()
        token = response['access_token']
        info = requests.get(f'https://www.googleapis.com/oauth2/v2/userinfo?access_token={token}').json()

        user = find_user_by_email(info['email'])
        request.session['username'] = user[1]

    return redirect('/')


@app.route('/api/logout', methods=['POST'])
@session_lifecycle
def logout():
    del request.session['username']
    print(request.session)
    return make_response('')


@app.route('/resources/<filename>', methods=['GET'])
def f(filename):
    return open(f'src/{filename}').read()


@app.route('/dist/<filename>', methods=['GET'])
def bundle(filename):
    return open(f'dist/{filename}').read()


@app.route('/api/messages', methods=['GET', 'POST'])
@session_lifecycle
@logged_in
def api_messages():
    if request.method == 'GET':
        cursor = db.cursor()
        cursor.execute('''
            SELECT messages.id, sender_id, content, created_at, login
            FROM messages
            JOIN users
            ON messages.sender_id = users.id
        ''')
        messages = cursor.fetchall()
        messages = [
            dict(zip(['id', 'sender_id', 'content', 'created_at', 'login'], message))
            for message in messages
        ]
        cursor.close()
        return jsonify(messages)
    elif request.method == 'POST':
        data = request.get_json()
        user_id = data['user_id']
        content = data['content']

        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO messages
            (sender_id, content, created_at)
            VALUES (%s, %s, NOW())
        ''', (user_id, content))
        cursor.close()
        return ''


app.run(port=5000)
