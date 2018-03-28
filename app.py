import pairmaker
import db_conn

from flask import Flask, abort, g, jsonify, request
app = Flask(__name__)

@app.route('/call', methods=['POST'])
def call():
    # Slack Webhook will just send a generic message body,
    # so we need to parse that and turn it into the
    # desired command + arguments
    r = {}

    with app.app_context():
        db = get_db()

        args = request.form.get('text').split(' ')
        command = args[1]

        if command == 'add':
            username = args[2]
            office = args[3]
            r = pairmaker.add_user(db, username, office)
        elif command == 'remove':
            username = args[2]
            r = pairmaker.remove_user(db, username)
        elif command == 'list':
            r = pairmaker.user_list(db)

    return jsonify(r)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = db_conn.get_db()
        db_conn.init_db(db)
    return db

if __name__ == '__main__':
    print('starting app')
    with app.app_context():
        g.db = db_conn.get_db()
        db_conn.init_db(g.db)
        app.run()
