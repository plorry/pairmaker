from operator import itemgetter

def add_user(db, username):
    c = db.cursor()
    c.execute('SELECT * FROM users WHERE name=?', [username,])
    if c.fetchone():
        print('user exists')
        return {'success': False, 'message': f'{username} is already here'}

    print('new user - adding')
    c.execute('INSERT INTO users (name) VALUES (?)', [username,])
    db.commit()
    print('user added')
    return {'success': True}

def remove_user(db, username):
    c = db.cursor()
    c.execute('DELETE FROM users WHERE name=?', [username,])
    db.commit()

    return {'success': True}


def make_pair(db):
    pass

def user_list(db):
    c = db.cursor()
    c.execute('SELECT name FROM users')
    return list(map(itemgetter(0), c.fetchall()))
