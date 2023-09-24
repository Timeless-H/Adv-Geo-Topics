# linking multipe routes (webpages) to each other, but doing it via template inheritance (layout.html)
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html") # take this html file and render it out


@app.route("/more")
def more():
    names = ["Bobby", "Alice", "Charlie"]
    return render_template("more.html", names=names) # take this html file and render it out
