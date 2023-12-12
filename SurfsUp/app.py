# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import numpy as np
import pandas as pd
import datetime as dt
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Precipitation API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

# will return a list of the dates and the precipitation on those dates
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    year_ago_date = dt.date(2017, 8, 23) - dt.timedelta(days= 365)

    prec_data = session.query(measurement.date, measurement.prcp).order_by(measurement.date.asc()).\
    filter(measurement.date >= year_ago_date).all()

    session.close()

    precipitation = []
#gathering the dates and the precipitation for the last year
    for date, prcp in prec_data:
        precipitation_dict = {}
        precipitation_dict[date] = date
        precipitation_dict[prcp] = prcp
        precipitation.append(precipitation_dict)
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations = session.query(station.station, station.name, station.latitude, station.longitude, station.elevation).all()
    session.close()
#gathers all the station information and puts them into a dictionary
    station_info = []
    for station, name, latitude, longitude, elevation in stations:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_info.append(station_dict).all()
    return jsonify(station_info)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    year_ago_date = dt.date(2017, 8, 23) - dt.timedelta(days= 365)
    #getting the top stations information
    station_info = session.query(measurement.date, measurement.tobs).order_by(measurement.date.asc()).\
                            filter(measurement.date >= year_ago_date).\
                            filter(measurement.station == 'USC00519281').all()
    session.close()

    tobs_one_year = []
    for date, tobs in station_info:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_one_year.append(tobs_dict)
    return jsonify(tobs_one_year)

#@app.route("/api/v1.0/<start>")
#def start():

#@app.route("/api/v1.0/<start>/<end>")
#def end():

if __name__ == "__main__":
    app.run(debug=True)
