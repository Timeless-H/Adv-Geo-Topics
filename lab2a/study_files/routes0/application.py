from flask import Flask

app = Flask(__name__)  # i wanna create a web app and i want it to be a flask
# web application, and its name to be this current file

'''flask is designed in terms of routes, where a route is part of the URL you
type-in in order to determine which page you wanna request

@app.route and the function directly below it is called the decorator
basically the function is what executes when the .route"/" (default webpage)
is accessed'''

@app.route("/")  # default page of the website when accessed for the 1st time
def index():
    return "Hello, world!"

@app.route("/david")  # the david page of the website when accessed through the default page
def david():
    return "Hello, David!"
