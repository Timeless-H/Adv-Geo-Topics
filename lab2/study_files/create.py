from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)  # bind this db to this flask application

def main():
    db.create_all()  # create tables based on those in models.py file

if __name__ == "__main__":
    with app.app_context():
        main()
