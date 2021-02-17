from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    names = ["Bobby", "Alice", "Moses"]
    return render_template("index.html", names=names) # take this html file and render it out
