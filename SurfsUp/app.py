# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base=automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
from flask import Flask, jsonify

app=Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route('/')
def home():
    """List all the available API Routes"""
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"This API provides analysis for a period of one year for dates from 2016-08-23 to 2017-08-23.<br/>"
        f"<br>Please note the following Available Routes:<br/>"
        f"(Direct links have also been provided where possible)<br/>"
        f"<br>/api/v1.0/precipitation<br/>"
        f"""<a href = "http://127.0.0.1:5000/api/v1.0/precipitation" > Precipitation Analysis </a> <br/>"""
        f"<br>/api/v1.0/stations<br/>"
        f"""<a href = "http://127.0.0.1:5000/api/v1.0/stations" > Stations Data </a> <br/>"""
        f"<br>/api/v1.0/tobs<br/>"
        f"""<a href = "http://127.0.0.1:5000/api/v1.0/tobs" > Temperature Observations </a> <br/>"""
        f"<br>/api/v1.0/&lt;start_date&gt;<br/>"
        f"Please enter the date in the format yyyy-mm-dd<br/>"
        f"<br>/api/v1.0/&lt;start_date&gt;/&lt;end_date&gt;<br/>"
        f"Please enter the date in the format yyyy-mm-dd<br/><br>For Example: Min, Max, and Average temperatures for dates from 2016-08-23 to 2017-08-23 <br/>"
        f"""<a href = "http://127.0.0.1:5000/api/v1.0/2016-08-23/2017-08-23" > Min, Max, and Average temperatures </a> <br/>"""
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last 12 months"""
    # calculate the date one year ago from the last data point in the database
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago_date = most_recent_date - dt.timedelta(days=366)

    # query precipitation data for last 12 months
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago_date).all()

    # create a dictionary from the results
    prcp_data = {}
    for date, prcp in results:
        prcp_data[date] = prcp

    return jsonify(prcp_data)

# define stations route
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # query all stations
    results = session.query(Station.station, Station.name).all()

    # create a list of dictionaries from the results
    stations_list = []
    for station, name in results:
        stations_list.append({'station': station, 'name': name})

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago_date = most_recent_date - dt.timedelta(days=366)
    most_active_station_id=session.query(Measurement.station, func.count(Measurement.station))\
            .group_by(Measurement.station)\
            .order_by(func.count(Measurement.station).desc())\
            .first()[0]
    results=session.query(Measurement.date,Measurement.tobs)\
                    .filter(Measurement.station==most_active_station_id)\
                    .filter(Measurement.date >= one_year_ago_date)\
                    .order_by(Measurement.date)\
                    .all()
    
    # create a list of dictionaries from the results
    tobs_list = []
    for date, tobs in results:
        tobs_list.append({'date': date, 'tobs': tobs})
        
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date."""
    start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date)\
            .all()
    # Convert the query results to a list
    start_list = []
    for result in start_results:
        start_dict = {}
        start_dict['Minimum Temperature'] = result[0]
        start_dict['Average Temperature'] = result[1]
        start_dict['Maximum Temperature'] = result[2]
        start_list.append(start_dict)
    return jsonify(start_list)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range."""
    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date)\
            .filter(Measurement.date <= end_date)\
                .all()
    # Convert the query results to a list of dictionaries
    start_list = []
    for result in start_end_results:
        start_dict = {}
        start_dict['Minimum Temperature'] = result[0]
        start_dict['Average Temperature'] = result[1]
        start_dict['Maximum Temperature'] = result[2]
        start_list.append(start_dict)
    return jsonify(start_list)

if __name__ == '__main__':
    app.run(debug=True)