# Import Required Modules

import sqlite3
from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
import os
import sys

# Initialize Flask app
app = Flask(__name__)

# Make session data permanent to keep users logged in
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key = "Messenger"

# SUbmit sitemap to search engines
@app.route("/sitemap")
def site():
    return render_template("sitemap.xml")

# Display and store new comments
@app.route("/comment/<query>", methods=["GET", "POST"])
def comment(query):
    if not session.get("messenger"):
        return redirect("/login")
    if auth(session['messenger']) is not True:
        return redirect("/login")
    if request.method == "GET":
        # fetch comments and parse collected data
        pid = int(query)
        comments = query_db(f"SELECT * FROM comments WHERE pid == {pid} ORDER BY time DESC")
        new_comments = []
        for i in comments:
            new = list(i)
            # fetch likes for each post
            value = likes(i[1])
            for i in value:
                new.append(i)
            p_comments = query_db(f"SELECT COUNT(*) FROM comments WHERE pid == {new[1]}")
            new.append(p_comments[0][0])
            new_comments.append(new)
        # fetch current post
        try:
            # If current post is a main post
            c_post = query_db(f"SELECT * FROM posts where id == {pid}")[0]
            current_post = [c_post[1], c_post[2], c_post[0]]
        except:
            #if current post is a comment
            c_post = query_db(f"SELECT * FROM comments WHERE id = {pid}")[0]
            current_post = [c_post[2], c_post[3], c_post[1]]

        return render_template("comment.html", username=session['messenger'], comments=new_comments, current_post=current_post)

    else:
        # collect and store comments from form
        new_comment = request.form.get('comment').strip()
        query_db(f"INSERT INTO comments VALUES ({int(query)}, {get_id()}, '{session['messenger']}', '{new_comment}', CURRENT_TIMESTAMP)")
        return redirect(f'/comment/{query}')

# change username
@app.route("/change_username", methods=["GET", "POST"])
def c_username():
    if not session.get("messenger"):
        return redirect("/login")
    if auth(session['messenger']) is not True:
        return redirect("/login")

    if request.method == "GET":
        return render_template("change.html", username=session['messenger'], error="")
    else:
        # fetch, authenticate and update username
        username = session["messenger"]
        new_username = request.form.get("new_username").strip()

        # Authenticate Data
        try:
            # make sure New username is not Taken by another user
            a = query_db(f"SELECT * FROM users WHERE username == '{new_username}'")
            a = a[0][1]
            return render_template("change.html", username=session['messenger'], error="Username Already Taken")
        except:
            # Update Data
            query_db(f"UPDATE users SET username = '{new_username}' WHERE username == '{username}'")
            query_db(f"UPDATE messages SET sender = '{new_username}' WHERE sender == '{username}'")
            query_db(f"UPDATE messages SET recipient = '{new_username}' WHERE recipient == '{username}'")
            query_db(f"UPDATE profile SET username = '{new_username}' WHERE username == '{username}'")
            query_db(f"UPDATE read SET sender = '{new_username}' WHERE sender == '{username}'")
            query_db(f"UPDATE read SET recipient = '{new_username}' WHERE recipient == '{username}'")
            query_db(f"UPDATE posts SET username = '{new_username}' WHERE username == '{username}'")
            try:
                # rename picture to new username if it exists
                os.rename(f"/home/Hardope/mysite/static/{username}.jpg", f"/home/Hardope/mysite/static/{new_username}.jpg")
            except:
                pass
            session['messenger'] = new_username
            # change session value to new username
            return redirect(f"/profile/{new_username}")

# change password
@app.route("/ch_password", methods=["GET", "POST"])
def ch_password():
    if not session.get("messenger"):
        return redirect("/login")
    if auth(session['messenger']) is not True:
        return redirect("/login")
    if request.method == "GET":
        return render_template("ch_password.html", username=session['messenger'], error="")
    else:
        # collect, authenticate and update data
        username = session["messenger"]
        password = request.form.get("password")
        new_password = request.form.get("new_password")
        try:
            # update data if original password is correct
            a = query_db(f"SELECT * FROM users WHERE username == '{username}' AND password == '{password}'")
            a = a[0][1]
            query_db(f"UPDATE users SET password = '{new_password}' WHERE username == '{username}'")
            return redirect("/")
        except:
            return render_template("ch_password.html", username=session['messenger'], error="Wrong Password")

# Update profile Information
@app.route("/me/<query>", methods=["GET", "POST"])
def me(query):
    if not session.get("messenger"):
        return redirect("/login")
    if auth(session['messenger']) is not True:
        return redirect("/login")
    if request.method == "GET":
        # send current data to be updated by user
        try:
            data = query_db(f"SELECT * FROM profile WHERE username is '{query}' LIMIT 1")
            about = data[0][2]
            if data[0][1].lower() == "male":
                gender = 0
            else:
                gender = 1
        except:
            about = ""
            gender = 3
        pic = session['messenger'].replace(" ", "_") + ".jpg"
        try:
            # check if current user has a profile picutre
            with open(f"/home/Hardope/mysite/static/{pic}", "r") as file:
                img = 1
        except:
            img = 0
        return render_template('edit.html', username=session['messenger'], about=about, gender=gender, pic=pic, img=img)
    else:
        # collect, authenticate and update new data
        about = request.form.get("about")
        about = about.strip()
        gender = request.form.get("gender")
        try:
            # Collect and update picture if provided
            file = request.files['pic']
            if not file:
                raise ValueError
            name = session['messenger'].replace(" ", "_")
            file = file.save(f"/home/Hardope/mysite/static/{name}.jpg")
        except:
            pass
        if gender == "male":
            gender = "Male"
        elif gender == "female":
            gender = "Female"
        else:
            gender == "None"

        try:
            check = query_db(f"SELECT * FROM profile WHERE username == '{session['messenger']}'")
            if check == []:
                raise ValueError
            query_db(f"UPDATE profile SET about = '{about}', gender = '{gender}' WHERE username == '{session['messenger']}'")
        except:
            query_db(f"INSERT INTO profile VALUES ('{session['messenger']}', '{gender}', '{about}')")
        return redirect(f"/profile/{session['messenger']}")

# No page wround route
@app.route("/<query>")
def no_page(query):
    return render_template("nopage.html")

# View profile
@app.route("/profile/<query>")
def detail(query):
    if not session.get("messenger"):
        return redirect("/login")
    if auth(session['messenger']) is not True:
        return redirect("/login")

    # collect user data
    data = query_db(f"SELECT * FROM profile WHERE username is '{query}' LIMIT 1")
    pic = query.replace(" ", "_") + ".jpg"
    p_posts = query_db(f"SELECT * FROM posts WHERE username == '{query}' ORDER BY time DESC")
    f_posts = []
    for i in p_posts:
        new = list(i)
        # fetch likes for each post
        value = likes(i[0])
        for i in value:
            new.append(i)
        p_comments = query_db(f"SELECT COUNT(*) FROM comments WHERE pid == {new[0]}")
        new.append(p_comments[0][0])
        f_posts.append(new)
    try:
        # check if profile picture is present
        with open(f"/home/Hardope/mysite/static/{pic}", "r") as file:
            img = 1
    except:
        img = 0
    return render_template('profile.html', username=session['messenger'], data=data, user=query, pic=pic, img=img, posts=f_posts)

# About website
@app.route("/about")
def about():
    if not session.get("messenger"):
        return redirect("/login")
    if auth(session['messenger']) is not True:
        return redirect("/login")
    return render_template("about.html", username=session['messenger'])

# provide Information
@app.route("/news")
def news():
    if not session.get("messenger"):
        return redirect("/login")
    if auth(session['messenger']) is not True:
        return redirect("/login")
    return render_template("news.html", username=session['messenger'])

# search for users
@app.route("/search", methods=["POST"])
def search():
    if not session.get("messenger"):
        return redirect("/login")
    if auth(session['messenger']) is not True:
        return redirect("/login")
    else:
        # Collect and parse data
        search = request.form.get("search")
        users = []
        image = []
        result = query_db(f"SELECT * FROM users WHERE username LIKE '%{search}%'")
        for i in result:
            if i[1] == session['messenger']:
                continue
            users.append(i[1])
        users = sorted(set(users))
        for i in users:
            pic = i.replace(" ", "_") + ".jpg"
            try:
                with open(f"/home/Hardope/mysite/static/{pic}", "r") as file:
                    img = 1
            except:
                img = 0
            image.append([pic, img])
        length = len(users) - 1
        return render_template("index.html", username=session['messenger'], users=users, picture=image, length=length)

# List of users available on the platform
@app.route("/users")
def index():
    if not session.get("messenger"):
        return redirect("/login")
    if auth(session['messenger']) is not True:
        return redirect("/login")
    else:
        users = []
        image = []
        result = query_db("SELECT * FROM users")
        for i in result:
            if i[1] == session['messenger']:
                continue
            users.append(i[1])
        user = sorted(set(users))
        for i in user:
            pic = i.replace(" ", "_") + ".jpg"
            try:
                with open(f"/home/Hardope/mysite/static/{pic}", "r") as file:
                    img = 1
            except:
                img = 0
            image.append([pic, img])
        length = len(users) - 1
        return render_template("index.html", username=session['messenger'], users=user, picture=image, length=length)

# Posts
@app.route("/")
def home():
    if not session.get("messenger"):
        return redirect("/login")
    if auth(session['messenger']) is not True:
        return redirect("/login")
    return render_template("posts.html", username=session['messenger'])

# List of users chatted with
@app.route("/chats")
def chats():
    if not session.get("messenger"):
        return redirect("/login")
    if auth(session['messenger']) is not True:
        return redirect("/login")
    else:
        a = 0
        users = []
        values = []
        image = []
        # fetch and parse data
        result = query_db(f"SELECT DISTINCT recipient FROM messages WHERE sender == '{session['messenger']}' ORDER BY time DESC")
        results = query_db(f"SELECT DISTINCT sender FROM messages WHERE recipient == '{session['messenger']}' ORDER BY time DESC")
        for i in result:
            users.append(i[0])
            length = query_db(f"SELECT COUNT (*) FROM messages WHERE sender == '{session['messenger']}' AND recipient == '{i[0]}' OR recipient == '{session['messenger']}' AND sender == '{i[0]}'")[0][0]
            try:
                comp = query_db(f"SELECT id FROM read WHERE sender == '{session['messenger']}' AND recipient == '{i[0]}'")[0][0]
            except:
                comp = 0
            if length > comp:
                values.append(f"{length - comp}")
            else:
                values.append("..")
            pic = i[0].replace(" ", "_") + ".jpg"
            try:
                with open(f"/home/Hardope/mysite/static/{pic}", "r") as file:
                    img = 1
            except:
                img = 0
            image.append([pic, img])
            a+=1
        if a < 1:
            return redirect("/users")
        return render_template("index1.html", username=session['messenger'], users=users, values=values, picture=image)

# chat page
@app.route("/chat/<query>")
def chat(query):
    if not session.get("messenger"):
        return redirect("/login")
    if auth(session['messenger']) is not True:
        return redirect("/login")
    else:
        return render_template("chat.html", username=session['messenger'], recipient=query)

# api to return posts to be loaded on web page using javascript
@app.route("/posts/<query>")
def post(query):
    if not session.get("messenger"):
        return redirect("/login")
    if auth(session['messenger']) is not True:
        return redirect("/login")
    else:
        if query == "new":
            return render_template("newpost.html", username=session['messenger'])
        # fetch and parse posts

        posts = query_db("SELECT * FROM posts ORDER BY id DESC")
        new_post = []
        pic_list = get_pic()
        for i in posts:
            new = list(i)
            value = likes(i[0])
            for i in value:
                new.append(i)
            comments = query_db(f"SELECT COUNT(*) FROM comments WHERE pid = {new[0]}")
            new.append(comments[0][0])
            if f"{new[0]}" in pic_list:
                new.append("True")
            else:
                new.append("False")
            new_post.append(new)
        return jsonify(new_post)

# new posts
@app.route("/new_post", methods=["POST"])
def new_post():
    # collect neew post from form and insert ti database
    post = request.form.get("post")
    post = post.replace("'", "''")
    username = session['messenger']
    pid = get_id()
    try:
        # Collect and update picture if provided
        file = request.files['pic']
        if not file:
            raise ValueError
        file = file.save(f"/home/Hardope/mysite/static/{pid}.jpg")
        with open("/home/Hardope/mysite/pic.txt", "a") as file:
            file.write(f"{pid}\n")
    except:
        pass
    query_db(f"INSERT INTO posts VALUES ({pid}, '{username}', '{post}', CURRENT_TIMESTAMP)")
    return redirect("/")
    query_db(f"INSERT INTO posts VALUES ({get_id()}, '{username}', '{post}', CURRENT_TIMESTAMP)")
    return redirect("/")

# api to collect and refresh messages
@app.route("/api/<query>")
def api(query):
    if not session.get("messenger"):
        return redirect("/login")
    if auth(session['messenger']) is not True:
        return redirect("/login")
    else:
        # collect and parse data
        length = query_db(f"SELECT COUNT (*) FROM messages WHERE sender == '{session['messenger']}' AND recipient == '{query}' OR recipient == '{session['messenger']}' AND sender == '{query}'")
        messages = query_db(f"SELECT * FROM messages WHERE sender == '{session['messenger']}' AND recipient == '{query}' OR recipient == '{session['messenger']}' AND sender == '{query}'")
        length = length[0][0]
        check = query_db(f"SELECT id FROM read WHERE sender == '{session['messenger']}' AND recipient == '{query}'")
        if len(check) > 0:
            query_db(f"UPDATE read SET id = {length} WHERE sender == '{session['messenger']}' AND recipient == '{query}'")
        else:
            query_db(f"INSERT INTO read VALUES({length}, '{session['messenger']}', '{query}')")
        return jsonify(messages)

#log in
@app.route("/login", methods=["GET", "POST"])
def login():
    # fetch log in details and validate information
    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        try:
            users = query_db(f"SELECT * FROM users WHERE username == '{username}' AND password == '{password}'")
        except:
            return render_template("login.html", error="Invalid Username Or Password")
        if len(users) < 1:
            return render_template("login.html", error="Invalid Username Or Password")
        else:
            session['messenger'] = username
            return redirect("/")
    else:
        return render_template("login.html", error="")

# register new user
@app.route("/register", methods=['POST', 'GET'])
def register():
    # collect and authenticate data then create user
    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        confirm = request.form.get('confirm').strip()


        if password == confirm:
            pass
        else:
            return render_template("register.html", error="Password does not match confirmation")
        users = query_db(f"SELECT * FROM users WHERE username == '{username}'")
        if not users:
            pass
        else:
            return render_template("register.html", error="Username Unavailable")
        try:
            available_id = query_db("SELECT id FROM users ORDER BY id DESC LIMIT 1")[0][0]
        except:
            available_id = 0

        query_db(f"INSERT INTO users (id, username, password) VALUES ({int(available_id + 1)}, '{username}', '{password}')")
        session['messenger'] = username
        return redirect("/users")
    else:
        return render_template("register.html", error="")

# send new message
@app.route("/messages/<query>", methods=['POST'])
def messages(query):
    if not session.get("messenger"):
        return redirect("/login")
    if auth(session['messenger']) is not True:
        return redirect("/login")
    else:
        # collect data and insert into database
        recipient, message = query.strip().split(':')
        message = message.replace("'", "''")
        for i in ['#', '?', '/']:
            message.replace(i, f"/n{i}")
        query_db("INSERT INTO messages VALUES ('{0}', '{1}', '{2}', CURRENT_TIMESTAMP)".format(session['messenger'], recipient, message))
        return "Sent"

# logout
@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session['messenger'] = None
    return redirect('/login')

# api to like posts
@app.route("/like/<query>", methods=['POST', 'GET'])
def like(query):
    username = session['messenger']
    query_db(f"INSERT INTO likes VALUES ({int(query)}, '{username}')")
    return "liked"

# api to unlike posts
@app.route("/unlike/<query>", methods=['POST', 'GET'])
def unlike(query):
    username = session['messenger']
    query_db(f"DELETE FROM likes WHERE id == {int(query)} AND username == '{username}'")
    return "unliked"

# fetch likes from database
def likes(query):
    username = session['messenger']
    num = int(query)
    likes = query_db(f"SELECT * FROM likes WHERE id == {num}")
    a = "🖤"
    b = False
    for i in likes:
        if i[1] == username:
            a = "❤️"
            b = True
            break
    return ([f"{len(likes)}{a}", b])

# query the database using sqlite3 and return the result
def query_db(text):
    conn = sqlite3.connect("/home/Hardope/mysite/messenger.db")
    cursor = conn.cursor()
    cursor.execute(f"{text}")
    value = cursor.fetchall()
    conn.commit()
    return value

# authenticate user
def auth(user):
    a = query_db(f"SELECT * FROM users WHERE username == '{user}'")
    try:
        a = a[0][1]
        return True
    except:
        return False

# get available id for posts
def get_id():
    id = 0
    try:
        with open("/home/Hardope/mysite/id.txt") as file:
            data = file.read()
            id = int(data) + 1
        with open("/home/Hardope/mysite/id.txt", 'w') as file:
            file.write(f"{id}")
    except:
        id+=1
        with open("/home/Hardope/mysite/id.txt", 'w') as file:
            file.write(f"{id}")

    return id

def get_pic():
    with open("/home/Hardope/mysite/pic.txt") as file:

        data = file.read()
        data = data.replace("\n", " ")
        data = data.split(" ")
        data = data[:-1]
        return data
