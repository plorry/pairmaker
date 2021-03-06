from operator import itemgetter
import time

INFO_MESSAGE = ('You\'ve been paired up! Reach out to each other on Slack to arrange a convenient '
    'time (not more than 30 minutes necessary) to connect.\nUse this time to get to know each '
    'other! Check in and see how you\'re doing; learn about each other.\nThere\'s no set agenda, '
    'and no notes or outcome required. Have fun, you two!')

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
    user_id = get_user_id(db, username)
    c.execute('DELETE FROM history WHERE user_1=? OR user_2=?', [user_id, user_id])
    c.execute('DELETE FROM users WHERE name=?', [username,])
    db.commit()

    return {'success': True, 'text': f'Okay, I removed {username}'}

def make_pair(db, id_tuple):
    count = get_history(db, id_tuple)
    now = int(time.time())

    print(f"History of user {id_tuple[0]} and {id_tuple[1]}: {count}")

    c = db.cursor()
    c.execute('UPDATE history SET count=?, last_pair=? WHERE user_1=? AND user_2=?',
        [count + 1, now, id_tuple[0], id_tuple[1]]
    )
    now = int(time.time())
    c.execute('UPDATE users SET last_pair=? WHERE id=? OR id=?', [now, id_tuple[0], id_tuple[1]])
    db.commit()

def get_lowest_user(db):
    c = db.cursor()
    c.execute('SELECT u.id, u.name, u.office FROM users u ORDER BY last_pair ASC, RANDOM()')
    f = c.fetchall()

    print(f)

    return f[0]

def get_ideal_partner(db, user_id, office):
    c = db.cursor()
    c.execute('SELECT u.id, u.name, (SELECT h.last_pair FROM history h WHERE (h.user_1=u.id AND h.user_2=?) OR (h.user_1=? AND h.user_2=u.id)) last FROM users u WHERE u.id != ? AND u.office !=? ORDER BY last ASC, u.last_pair ASC, RANDOM()', [user_id, user_id, user_id, office])
    f = c.fetchall()

    print(f)

    return f[0]

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

def pairup(db, user_1=None):
    if user_1 is None:
        u1 = get_lowest_user(db)
        print(u1)
    else:
        u1 = get_user_id(db, user_1)
    u2 = get_ideal_partner(db, u1[0], u1[2])
    print(u2)
    make_pair(db, mk_id_tuple(u1[0], u2[0]))

    return {'text': f'The next pairup is {u1[1]} and {u2[1]}!\n{INFO_MESSAGE}'}

def get_user_id(db, username):
    c = db.cursor()
    c.execute('SELECT id, name, office FROM users WHERE name=?', [username,])
    f = c.fetchall()

    print(f)

    return f[0]

def get_all_users(db):
    c = db.cursor()
    c.execute('SELECT * FROM users')

    return c.fetchall()

def user_list(db):
    c = db.cursor()

    c.execute('SELECT * FROM history')
    print(c.fetchall())


    c.execute('SELECT name, office FROM users')
    return {
        'text': '\n'.join([f'{u[0]} ({u[1]})' for u in c.fetchall()])
    }
