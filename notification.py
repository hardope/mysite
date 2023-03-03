import sqlite3

def main():
     while True:
          users1 = query_db("SELECT DISTINCT sender FROM chats")
          users2 = query_db("SELECT DISTINCT recipient FROM chats")
          users = list(set([user[0] for user in users1] + [user[0] for user in users2]))
          for i in users:
               notify = []
               data0 = query_db("SELECT recipient FROM chats WHERE sender == '{}'".format(i))
               data1 = query_db("SELECT sender FROM chats WHERE recipient == '{}'".format(i))
               data = list(set([user[0] for user in data0] + [user[0] for user in data1]))
               for user in data:
                    count = count_messages(user, i)
                    try:
                         read = query_db("SELECT * FROM read WHERE sender == '{}' AND recipient == '{}'".format(i, user))[0][0]
                    except:
                         read = 0
                    if count > read:
                         notify.append(user)
               new_notify = ""
               for val in notify:
                    new_notify+=(f"{val},")
               try:
                    query_db(f"SELECT * FROM notification WHERE username == '{i}'")[0]
                    query_db(f"UPDATE notification SET new == '{new_notify}' WHERE username == '{i}'")
               except:
                    query_db(f"INSERT INTO notification VALUES ('{i}', '{new_notify}')")
          print("Load")
               

def query_db(text):
    conn = sqlite3.connect("messenger.db")
    cursor = conn.cursor()
    cursor.execute(f"{text}")
    value = cursor.fetchall()
    conn.commit()
    return value

def count_messages(user1, user2):
     return (query_db(f"SELECT COUNT (*) FROM chats WHERE sender == '{user1}' AND recipient == '{user2}' OR recipient == '{user1}' AND sender == '{user2}'")[0][0])

main()