import sqlite3

def get_db(db_name):
    return sqlite3.connect(f'{db_name}.db')

def init_db(db):
    db.execute('CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, name text NOT NULL, office text, last_pair integer default 0)')
    db.execute('CREATE TABLE IF NOT EXISTS history (\
        user_1 integer NOT NULL, user_2 integer NOT NULL, count integer DEFAULT 0, last_pair INTEGER DEFAULT 0, \
        FOREIGN KEY (user_1) REFERENCES users(id), \
        FOREIGN KEY (user_2) REFERENCES users(id))')
    print('db initialized')
