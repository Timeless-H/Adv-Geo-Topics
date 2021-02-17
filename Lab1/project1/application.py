import os, requests, json
import psycopg2

from flask import Flask, session, request, render_template, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
# orm: object relational mapping: allows the interaction btwn python n SQL db

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
# engine = create_engine(os.getenv("DATABASE_URL")) # manages communication btwn python and db
# db = scoped_session(sessionmaker(bind=engine)) # manages multiple users simultaneously
conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
db = conn.cursor()


@app.route("/")
def index():
    if session.get("login") is None:
        session["login"] = False
    if session.get("login") == True:
        return redirect(url_for('search'))
    return render_template('login_page.html')


@app.route('/login_page', methods=["GET", "POST"])
def login_page():

    if session.get("login") == False:
        msg = None
        print(" session is false ")
        # check the existence of POST, username and password in user submitted form
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            print(username, password)

            db.execute("SELECT * FROM accounts WHERE username = %s and password =%s", (username,password))
            user = db.fetchall()
            if user == []:
                msg = "Wrong login credentials"
            else:
                session["login"] = True
                session["username"] = username
                return redirect(url_for('search'))
        else:
            # msg = "Please fill all details"
            return redirect(url_for('login_page'))
    else:
        return redirect(url_for('search'))
    # return render_template("login_page.html")


@app.route('/sign_up_page', methods=["GET", "POST"])
def sign_up_page():
    msg = ''

    if request.method == 'POST': # and (username is not None and password is not None and email is not None):
        username = request.form.get("username")
        password = request.form.get('password')
        email = request.form.get('email')
        print(username, password, email)

        db.execute("SELECT * FROM accounts WHERE username = (%s)", (username,))
        user = db.fetchall()
        print(user)
        if user == []:
            db.execute("INSERT INTO accounts (username, password, email) VALUES (%s,%s,%s)", (username, password, email))
            conn.commit()
            msg = 'You have successfully registered! Please login now.'

        else:
            msg = "Username already exist!"

    return render_template("sign_up_page.html", msg=msg)


@app.route('/logout')
def logout():
    session["login"] = False
    return render_template("login_page.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    result = []
    if request.method == "POST":
        isbn = request.form.get('isbn',None)
        author = request.form.get('author',None)
        title  = request.form.get('title',None)
        print(isbn, author, title)

        if isbn:
            db.execute("SELECT * FROM books WHERE isbn ILIKE %s",(isbn,))
            result = db.fetchall()
        elif author:
            db.execute("SELECT * FROM books WHERE author ILIKE %s", (author,))
            result = db.fetchall()
        elif title:
            db.execute("SELECT * FROM books WHERE title ILIKE %s", (title,))
            result = db.fetchall()
        else:
            msg = 'Please feel at least one field.'
    # elif request.method == 'GET' and ('isbn' not in request.form and 'author' not in request.form and 'title' not in request.form):
    #     db.execute("SELECT * FROM books LIMIT 10")
    #     result = db.fetchall()
        # print(result[1])

    return render_template('search.html',result=result)


# Book_Detail
@app.route("/book_page/<book_id>",methods=["POST", "GET"])
def book_page(book_id):
    """details of the book"""
    session["book_id"] = book_id
    # print(book_id)
    db.execute("SELECT * FROM books WHERE id = %s",(book_id,))
    result = db.fetchone()
    # print(result)
    db.execute("SELECT review, rating FROM review WHERE book_id = %s", (book_id,))
    if db.fetchall() is not None:
        user_reviews = db.fetchall()
    # user_id = db.execute("SELECT id FROM accounts WHERE username = %s", (session["username"])).fetchone()
    # review = db.execute("SELECT review, rating FROM review WHERE book_id = %s AND user_id = %s",(book_id, user_id)).fetchone()
    # if request.method == "POST" and not review:
    #     review_text = request.form.get('user_review')
    #     rating_val = request.form.get('user_rating')


    return render_template('book_page.html', book_id=session["book_id"], result=result, user_reviews=user_reviews)

# Rate and # REVIEW:
@app.route("/rate_review", methods=["POST", "GET"])
def rate_review():
    if request.method == "POST":
        book_id = session.get('book_id')
        user_id = session.get('username')
        review = request.form.get('message')
        rating = request.form.get('rating')
        print(book_id, user_id, review, rating)

        # if book_id is not None and user_id is not None:
        db.execute("SELECT id FROM accounts WHERE username = (%s)", (user_id,))
        # if db.fetchall() != []:
        num_user_id = db.fetchone()

        db.execute("SELECT * FROM review WHERE book_id = %s AND user_id=%s",(book_id,num_user_id[0]))
        print(db.fetchone())
        if db.fetchone() is not None:
             msg = "You can't do anymore rating"
             return redirect(url_for('book_page',book_id=book_id))
        db.execute("INSERT INTO review (book_id,user_id,review,rating) VALUES (%s,%s,%s,%s)",(book_id,num_user_id,review,rating))
        conn.commit()

    return render_template('rate_review.html')

# API Routing
@app.route("/api/<isbn>", methods=["GET"])
def api(isbn):
    print(isbn)
    db.execute("SELECT * FROM books WHERE isbn = %s", (isbn,))
    if db.fetchall() == None:
        return jsonify({"error": "Invalid ISBN"}), 404
    # data = json.load('https://www.googleapis.com/books/v1/volumes?q=ISBN:{{isbn}}')
    res = requests.get('https://www.googleapis.com/books/v1/volumes', params={"q": "ISBN:{{isbn}}"})
    # print(res.json())
    volumeInfo = res.json()["items"][0]["volumeInfo"]
    ISBN_X = res.json()["items"][0]["volumeInfo"]['industryIdentifiers']

    result = {'title':volumeInfo['title'], 'author':volumeInfo['authors'], 'publishedDate':volumeInfo['publishedDate'], 'ISBN_10':ISBN_X[0]['identifier'], 'ISBN_13':ISBN_X[1]['identifier'], 'ratingsCount':volumeInfo.get('ratingsCount', 0), 'averageRating':volumeInfo.get('averageRating', 0)}
    return jsonify(result)
