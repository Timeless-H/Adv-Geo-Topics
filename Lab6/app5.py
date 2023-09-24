from flask import Flask, render_template
import csv, json
from geojson import Feature, FeatureCollection, Point

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('map_page.html')

if __name__ == '__main__':
    app.run(debug=True)