import os
import csv

from flask import Flask, session, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL")) # manages communication btwn python and db
db = scoped_session(sessionmaker(bind=engine)) # manages multiple users simultaneously

def main():
    f = open("../books.csv")
    reader = csv.reader(f)
    db.execute("CREATE TABLE books (id SERIAL PRIMARY KEY, isbn VARCHAR(255) NOT NULL, title VARCHAR(255) NOT NULL, author VARCHAR(255) NOT NULL, year VARCHAR(50) NOT NULL)")
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added book titled {title} published by {author} in {year}")
    db.commit()

    db.execute("CREATE TABLE accounts (id SERIAL PRIMARY KEY, username VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL)")
    db.commit()
    print("user accounts table created")

    db.execute("CREATE TABLE review (id SERIAL PRIMARY KEY, book_id INT REFERENCES books, user_id INT REFERENCES accounts, review TEXT, rating INT DEFAULT 0)")
    db.commit()
    print("user review table created")
if __name__=="__main__":
    main()
