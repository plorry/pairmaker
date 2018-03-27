import pairmaker
import db_conn

from flask import Flask, abort, g, jsonify, request
app = Flask(__name__)

@app.route('/call', methods=['POST'])
def call():
    # Slack Webhook will just send a generic message body,
    # so we need to parse that and turn it into the
    # desired command + arguments
    with app.app_context():
        db = get_db()

    return jsonify({'success': True})

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = db_conn.get_db()
        db_conn.init_db()
    return db

@app.route('/user/add', methods=['POST'])
def add_user():
    print(request.json)

    username = request.json.get('username')
    r = pairmaker.add_user(g.db, username)

    return jsonify(r)

@app.route('/user/<username>/delete', methods=['DELETE'])
def remove_user(username):
    r = pairmaker.remove_user(g.db, username)
    return jsonify(r)

@app.route('/pairup', methods=['GET'])
def make_pair():
    pairmaker.make_pair(g.db)

@app.route('/user', methods=['GET'])
def user_list():
    users = pairmaker.user_list(g.db)
    return jsonify({'users': users})

if __name__ == '__main__':
    print('starting app')
    with app.app_context():
        g.db = db_conn.get_db()
        db_conn.init_db(g.db)
        app.run()
