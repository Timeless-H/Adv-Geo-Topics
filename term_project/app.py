from flask import Flask, render_template
import csv, json

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('templates/interface.html')

if __name__ == '__main__':
    app.run(debug=True)
