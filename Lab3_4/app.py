from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from urllib.parse import quote

app = Flask(__name__)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:perp@localhost:5432/my_map'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# engine = create_engine()


class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)


@app.route('/')
def index():
    url = "https://data.calgary.ca/resource/c2es-76ed.geojson"
    # url = "https://data.calgary.ca/resource/c2es-76ed.geojson?$where=issueddate > '2020-01-21' and issueddate < '2020-01-23'"
    return render_template('map_page1.html', url=url)

@app.route('/login_page', methods=['POST', 'GET'])
def login_page():
    url = "https://data.calgary.ca/resource/c2es-76ed.geojson"
    if request.method == 'POST':
        # username = request.form['username']
        # password = request.form['password']
        from_date = datetime.strptime(request.form['from_date'], '%Y-%m-%d')
        to_date = datetime.strptime(request.form['to_date'], '%Y-%m-%d')
        if from_date == to_date:
            url = "https://data.calgary.ca/resource/c2es-76ed.geojson?issueddate={}-{}-{}T00:00:00.000".format(from_date.year, from_date.month, from_date.day)
        else:
            url = "https://data.calgary.ca/resource/c2es-76ed.geojson?$where=issueddate > '{}-{}-{}' and issueddate < '{}-{}-{}'".format(from_date.year, from_date.month, from_date.day, to_date.year, to_date.month, to_date.day)
        # print("from: {} \t to: {}".format(from_date, to_date))
    return render_template('map_page1.html', url=url)



if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)