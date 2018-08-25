from flask import Flask, jsonify, request
import MySQLdb
db = MySQLdb.connect(user='root', passwd="123", db="messenger")
db.autocommit(True)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/messages', methods=['GET', 'POST'])
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