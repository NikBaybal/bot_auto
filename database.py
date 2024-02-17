#можно использвать не асинхронный,тк БД используется только в режме админа
import sqlite3

conn = sqlite3.connect('files/users.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(id INT,username TEXT, first_name TEXT, block INT); """)

def add_user(user_id, username, first_name):
    check_user = cur.execute('SELECT * FROM users WHERE id=?', (user_id,))
    if check_user.fetchone() is None:
        cur.execute(f"""INSERT INTO users VALUES('{user_id}', '{username}', '{first_name}', 0); """)
    conn.commit()


def show_users():
    users_list = cur.execute('SELECT * FROM users').fetchall()
    message = ''
    for users in users_list:
        message += f"{users[0]}, @{users[1]}, {users[2]}, {users[3]}\n"
    conn.commit()
    return message


def count():
    s = cur.execute("SELECT COUNT(*) FROM users;").fetchone()
    conn.commit()
    return s[0]


def get_id():
    s = cur.execute("SELECT id FROM users;").fetchall()
    conn.commit()
    return s


def get_username(id):
    s = cur.execute(f"SELECT username FROM users WHERE id = {id}").fetchone()
    conn.commit()
    return s[0]


def add_user_to_block(id):
    cur.execute(f'UPDATE users SET block = ? WHERE id = ?', (1, id))
    conn.commit()


def check_user_in_block(id):
    users = cur.execute(f'SELECT block FROM users WHERE id = {id}').fetchone()
    conn.commit()
    return users[0]


def unlock_user(id):
    cur.execute(f'UPDATE users SET block=? WHERE id = ?',(0, id))
    conn.commit()

