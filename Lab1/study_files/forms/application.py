from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html") # take this html file and render it out

@app.route("/hello", methods=["POST"]) # submissions will be made via the 'post' method to function hello
def hello():
    name = request.form.get("name") # get the name field data from the form that the user will fill
    return render_template("hello.html", name=name) # pass the name arg to hello.html for use
