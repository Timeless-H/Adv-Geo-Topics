from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    headline = "Hello, world!"
    # python arg "headline" passed onto an html variable "headline"
    return render_template("index.html", headline=headline) # take this html file and render it out

'''the advantage of templating is that, the same template can be used multiple
times with different input. e.g.'''

@app.route("/bye")
def bye():
    headline = "Goodbye!"
    # python arg "headline" passed onto an html variable "headline"
    return render_template("index.html", headline=headline) # take this html file and render it out
