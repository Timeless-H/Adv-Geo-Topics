from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Flight(db.Model):
    """docstring"""
    __tablename__ = "flights"
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    duration = db.Column(db.String, nullable=False)


class Passesnger(db.Model):
    """docstring"""
    __tablename__ = "passengers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    # flight_id as a foreign key that references flights.id column from flights table
    flight_id = db.Column(db.Integer, db.Foreign_key("flights.id"), nullable=False)
