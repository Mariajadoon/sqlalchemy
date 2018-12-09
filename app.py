#%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"//api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>><br/>"
    )

@app.route("/api/v1.0/precipitation")
def prp():
    query = f"SELECT date, prcp FROM measurement"
    pd.read_sql_query(query, session.bind)
    results = df.to_dict(orient='records')
    return jsonify(results)

@app.route("/api/v1.0/stations")
def st():
    # Query all stations
    results = session.query(Measurement.station).all()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def prp():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017, 8, 23) - relativedelta(months=12)
    query = f"SELECT date, prcp FROM measurement WHERE date > {query_date}"
    pd.read_sql_query(query, session.bind)
    results = df.to_dict(orient='records')
    return jsonify(results)


@app.route("/api/v1.0/<start_date>/<end_date>")
def stend(start_date, end_date):
    query = f"SELECT * FROM table WHERE date > {start_date} AND date < {end_date}"
    df = pd.read_sql_query(query, session.bind)
    data = df.to_dict(orient='records')
    results = df.to_dict(orient='records')
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)