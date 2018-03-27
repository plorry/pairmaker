import sqlite3

def get_db():
    return sqlite3.connect('pairmaker.db')

def init_db(db):
    db.execute('CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, name text NOT NULL)')
    # db.execute('CREATE TABLE IF NOT EXISTS history ()')
    print('db initialized')
