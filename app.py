import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"SQLAlchemy + Flask Test API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-23<br/>"
        f"/api/v1.0/2016-08-23/2017-08-23"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session
    session = Session(engine)

    """Return query of last year's date and precipitation"""
    # Query date and prcp
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date <= '2017-08-23').filter(Measurement.date >= '2016-08-23')

    # Close session
    session.close

    # Create dictionary from last year's date and prcp query and append it to a list
    all_date_prcp = []
    for date, prcp in results:
        date_prcp_dict = {}
        date_prcp_dict["date"] = date
        date_prcp_dict["prcp"] = prcp
        all_date_prcp.append(date_prcp_dict)

    # Turn list into json format
    return jsonify(all_date_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create session
    session = Session(engine)

    """Return query of list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()

    # Close session
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    # Turn list into json format
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create session
    session = Session(engine)

    """Return query of dates and tobs for the most active station in the last year"""
    # Perform query
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date <= '2017-08-18').filter(Measurement.date >= '2016-08-18').all()
    
    # Close session
    session.close()
    
    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    # Turn list into json format
    return jsonify(all_tobs)

if __name__ == "__main__":
    app.run(debug=True)