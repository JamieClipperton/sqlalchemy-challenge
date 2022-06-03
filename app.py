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
    return (
        f"All available routes:<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
    )

#Percipitations
@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year_data = dt. date(2017,8,23) - dt.timedelta(days=365)
    prcp_values = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year_data).\
        order_by(Measurement.date).all()
    prcp_val_list = dict(prcp_values)
    return jsonify(prcp_val_list)

#Stations
@app.route("/api/v1.0/stations")
def stations():
    stat_list = session.query(Station.station, Station.name).all()
    all_stat = list(stat_list)
    return jsonify(all_stat)

#TOBS Route
@app.route("/api/v1.0/tobs")
def tobs():
    last_year_data = dt. date(2017,8,23) - dt.timedelta(days=365)
    tobs_value = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= last_year_data).\
        order_by(Measurement.date).all()
    tobs_lst = list(tobs_value)
    return jsonify(tobs_lst)


#Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
    start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()
    start_list = list(start_day)
    return jsonify(start_list)

#Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    start_end = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        group_by(Measurement.date).all()
    start_end_lst = list(start_end)
    return jsonify(start_end_lst)

#Define Behavior
if __name__ == '_main_':
    app.run(debug=True)
