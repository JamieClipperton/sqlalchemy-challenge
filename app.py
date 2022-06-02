#import flask
from flask import Flask, jsonify

#Setup
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)

#Save References to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create Session
session = Session(engine)

#Flask Setup
app = Flask(__name__)

#Flask Routes
@app.route("/")
def home():
    """List all available api routes"""
    return (
        f"Available Routes:"
    )
