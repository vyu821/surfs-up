# dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# set up database engine
engine = create_engine('sqlite:///hawaii.sqlite')

# reflect the database into our classes
Base = automap_base()
Base.prepare(engine, reflect = True)

# save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# session link from python to our database
session = Session(engine)

#create new Flask app instance
app = Flask(__name__)

# flask routes
# root, starting point, welcome route
@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    <br/> Available Routes:
    <br/> /api/v1.0/precipitation
    <br/> /api/v1.0/stations
    <br/> /api/v1.0/tobs
    <br/> /api/v1.0/temp/start/end
    ''')

# percipitation route
@app.route('/api/v1.0/precipitation')
def precipitation():

    # calculates the date one year ago from most recent date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query to get date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    # created dictionary with date as key and precipitation as values
    precip = {date: prcp for date, prcp in precipitation}

    return jsonify(precip)

# stations route
@app.route('/api/v1.0/stations')
def stations():

    # query to get all stations in our database
    results = session.query(Station.station).all()
    # unravel results into 1d array, then convert into a list
    stations = list(np.ravel(results))

    return jsonify(stations = stations)

# temperature observations route
@app.route("/api/v1.0/tobs")
def temp_monthly():
        
    # calculates the date one year ago from most recent date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query the primary stations for all temperature observations from previous year
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
    # unravel results into 1d array, then convert into a list
    temps = list(np.ravel(results))

    return jsonify(temps = temps)

# summary statistics route, with starting and ending dates
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start = None, end = None):

    # list for query to select min, max, avg temps
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
     
    if not end:
        
        # query to get temp info using starting date
        results = session.query(*sel).filter(Measurement.date <= start).all()
        # unravel results into 1d array, then convert into a list
        temps = list(np.ravel(results))

        return jsonify(temps)

    # query to get temp info using starting/ending dates
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    # unravel results into 1d array, then convert into a list
    temps = list(np.ravel(results))

    return jsonify(temps = temps)


