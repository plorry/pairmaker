from operator import itemgetter

def add_user(db, username, office):
    c = db.cursor()
    c.execute('SELECT * FROM users WHERE name=?', [username,])
    if c.fetchone():
        print('user exists')
        return {'success': False, 'text': f'{username} is already here'}

    print('new user - adding')
    c.execute('INSERT INTO users (name, office) VALUES (?, ?)', [username, office])
    db.commit()

    c.execute('SELECT id FROM users WHERE name=?', [username])
    new_id = c.fetchone()[0]

    for user in get_all_users(db):
        other_id = user[0]
        id_tuple = mk_id_tuple(new_id, other_id)

        if other_id != id_tuple:
            get_history(db, id_tuple)

    print('user added')
    return {'success': True, 'text': f'Added user {username} to user list'}

def mk_id_tuple(id1, id2):
    return (min(id1, id2), max(id1, id2))

def remove_user(db, username):
    c = db.cursor()
    c.execute('DELETE FROM users WHERE name=?', [username,])
    db.commit()

    return {'success': True, 'text': f'Okay, I removed {username}'}

def make_pair(db, id_tuple):
    count = get_history(db, id_tuple)

    c = db.cursor()
    c.execute('UPDATE history SET count=? WHERE user_1=? AND user_2=?',
        [count + 1, id_tuple[0], id_tuple[1]]
    )

def get_lowest_user(db):
    c = db.cursor()
    c.execute('SELECT id, SUM(history.count) as c FROM users INNER JOIN history ON history.user_1=users.id OR history.user_2=users.id ORDER BY c ASC LIMIT 1')

    return c.fetchone()[0]

def get_user_pair_count(db, user_id):
    c = db.cursor()
    c.execute('SELECT SUM(count) FROM history WHERE user_1=? OR user_2=?', [user_id, user_id])

    return c.fetchone()[0]

def get_history(db, id_tuple):
    c = db.cursor()
    c.execute('SELECT count FROM history WHERE user_1=? AND user_2=?', [id_tuple[0], id_tuple[1]])

    count = c.fetchone()

    if count is None:
        c.execute('INSERT INTO history (user_1, user_2) VALUES (?, ?)', [id_tuple[0], id_tuple[1]])
        db.commit()
        count = 0
    else:
        count = count[0]

    return count

def get_all_users(db):
    c = db.cursor()
    c.execute('SELECT * FROM users')

    return c.fetchall()

def user_list(db):
    c = db.cursor()
    c.execute('SELECT name, office FROM users')
    return {
        'text': ' '.join([f'{u[0]} ({u[1]})' for u in c.fetchall()])
    }
