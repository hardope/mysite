import sqlite3

def query_db(text):
    conn = sqlite3.connect("/home/Hardope/mysite/messenger.db")
    cursor = conn.cursor()
    cursor.execute(f"{text}")
    value = cursor.fetchall()
    conn.commit()
    return value
users = query_db("SELECT username FROM users")
for i in users:
    i[0]
    query_db(f"INSERT INTO likes VALUES (1, '{i[0]}')")