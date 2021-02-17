from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# notes = []  # no longer needed coz of sessions.

@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("notes") is None:  # if session notes doesnt exist, initialize it
        session["notes"] = []  # this line allows for none overlapping of user content or info
    # the above if statement prevents the session notes from resetting everytime the index function is called
    if request.method == "POST":
        note = request.form.get("note")
        session["notes"].append(note)  # likewise this line
    return render_template("index.html", notes=session["notes"]) # take this html file and render it out


'''Sessions allow the storing/processing of different user info separately. e.g. the login
duration session of two separate people (at the same time)

say we wanna create a website that stores user info - in this case reading notes
session allows that User A doesnt see User B's notes and vice versa'''
