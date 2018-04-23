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
        channel_name = request.form.get('channel_id')
        db = get_db(channel_name)

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
        elif command == 'pairup':
            r = pairmaker.pairup(db) if len(args) == 2 else pairmaker.pairup(db, args[3])

    return jsonify(r)

def get_db(channel_name):
    db = getattr(g, f'_database_{channel_name}', None)
    if db is None:
        db = db_conn.get_db(channel_name)
        setattr(g, f'_database_{channel_name}', db)
        db_conn.init_db(db)
    return db

if __name__ == '__main__':
    print('starting app')
    with app.app_context():
        g.db = db_conn.get_db()
        db_conn.init_db(g.db)
        app.run()
