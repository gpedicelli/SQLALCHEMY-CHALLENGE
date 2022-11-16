from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """Return"""

    return(
        f'Welcome to my Page<br/>'
        f'Available Routes<br/>'
        f'/api/v1.0/precipitation<br/>'
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data as json"""
    # Query Last 12 Months 
    last_twelve_months = dt.date(2017,8,23) - dt.timedelta(days=365)
    p_results = session.query(Measurement.date, func.avg(Measurement.prcp)).\
                    filter(Measurement.date >= last_twelve_months).\
                    group_by(Measurement.date).all()

    # Close Session
    session.close()

    # Create dictionay of p_results 
    precip = {date:prcp for date, prcp in p_results}
    return jsonify(precip)





if __name__ == "__main__":
    app.run(debug=True)