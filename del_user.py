#!/usr/bin/python3

import sys
import sqlite3

def main():

    while True:
        username = input("User To delete: ").strip()
        if username != "":
            break

    if (input(f"Delete {username} : ").lower().strip()[0] == "y"):
        pass
    else:
        sys.exit()

    query_db(f"DELETE FROM user WHERE username == '{username}'")
    query_db(f"DELETE FROM chats WHERE sender == '{username}'")
    query_db(f"DELETE FROM chats WHERE recipient == '{username}'")
    query_db(f"DELETE FROM profile WHERE username == '{username}'")
    query_db(f"DELETE FROM read WHERE sender == '{username}'")
    query_db(f"DELETE FROM read WHERE recipient == '{username}'")
    query_db(f"DELETE FROM posts WHERE username == '{username}'")
    query_db(f"DELETE FROM likes WHERE username == '{username}'")

    print("User Deleted")



def query_db(text):
    conn = sqlite3.connect("/home/Hardope/mysite/messenger.db")
    cursor = conn.cursor()
    cursor.execute(f"{text}")
    value = cursor.fetchall()
    conn.commit()
    return value

if __name__ == "__main__":
    main()