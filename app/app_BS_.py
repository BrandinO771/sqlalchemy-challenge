## Step 2 - Climate App
'''

Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.
* Use FLASK to create your routes.
### Routes

* `/`
  * Home page.
  * List all routes that are available.

* `/api/v1.0/precipitation`
  * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
  * Return the JSON representation of your dictionary.

* `/api/v1.0/stations`
  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * query for the dates and temperature observations from a year from the last data point.
  * Return a JSON list of Temperature Observations (tobs) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.  
  
  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.  
  
  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

'''


import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify
import os 
import re
import datetime 
#################################################
# Database Setup
#################################################
# Path to sqlite
database_path = "../Resources/hawaii.sqlite"

# Create an engine that can talk to the database
engine = create_engine(f"sqlite:///{database_path}")

#engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Base.classes.keys() 
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
################################################
app = Flask(__name__)

#################################################
# Create our session (link) from Python to the DB
#session = Session(engine)
# seesions are opened within our defined functions below 

#################################################
# Flask Routes
#################################################

'============================================================================================='
''' * `/`                           HOME PAGE 
  * Home page.
  * List all routes that are available.'''

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f" Aloha Welcome to the Hawaii Weather API<br/>"
        f"<br/>"
        f"<br/>"
        f"The Available Routes Are Listed Below:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f" The below link route will list all of our [stations] from the dataset:<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        F" The Below link insert a date after the forward slash /   like YYYY-MM-DD to get average weather data for dates greater than and equal to this date:<br/>"
        f"<br/>"      
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        F" The Below link insert a date like YYYY-MM-DD/YYYY-MM-DD to get average weather data for this date period:<br/>"
        f"<br/>"       
        f"/api/v1.0/<start>/<end><br/>"
        f"<br/>"
        f"     PLEASE NOTE: Data is only available for the following date range ( 2010-01-01  AND  2017-08-18  )<br/>"
        f"<br/>"
        f"  Have a nice day mahalo for visiting the Hawaii API "
    )



'============================================================================================='
'''                             PRECIPITATION 

* `/api/v1.0/precipitation`
  * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
  * Return the JSON representation of your dictionary.
'''

@app.route("/api/v1.0/precipitation/<key>")
def precipitation(key):
    #////////////// Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all"""
    #///////////// Query Conditions
    results = session.query(Measurement.date, Measurement.station, Measurement.prcp).\
        filter(Measurement.date == key).all()
    session.close()
    #//////////// Convert list of tuples into normal list
    #all_results = list(np.ravel(results))
    all_results = []

    for  date, station, prcp, in results:
        prcp_dic = {}
        prcp_dic["date"] = date 
        prcp_dic["station"] = station # can also do  = station, name
        prcp_dic["precipation"] = prcp
        all_results.append(prcp_dic)

    return jsonify(all_results)




'============================================================================================='
'''                               STATIONS 

 #* `/api/v1.0/stations`
#   * Return a JSON list of stations from the dataset.'''

@app.route("/api/v1.0/stations")
def station_list():
    #////////////// Create our session (link) from Python to the DB
    session = Session(engine)
      #///////////// Query Conditions
    results = session.query(Station.station, Station.name).all()
    #//////////// Convert list of tuples into normal list
    #all_results = list(np.ravel(results))
    
    all_results = []

    for station, name in results:
        stations_dic = {}
        stations_dic["station id"] = station # can also do  = station, name
        stations_dic["station name"] = name
        all_results.append(stations_dic)

    session.close()
    return jsonify(all_results)




'============================================================================================='
'''                               TEMP TOBS LIST 
# * `/api/v1.0/tobs`
#   * query for the dates and temperature observations from a year from the last data point.
#   * Return a JSON list of Temperature Observations (tobs) for the previous year.'''
@app.route("/api/v1.0/tobs")
def temp_list():
    #////////////// Create our session (link) from Python to the DB
    session = Session(engine)
    #///////////// Query Conditions
    end_date = session.query(func.max(Measurement.date)).all()

    #////HERE EXTRACT DATE INFO TO PLUG INTO  start_date = datetime.date function below 
    break_date = re.split("-", end_date[0][0])
    year = int(break_date[0])
    month = int(break_date[1])
    day = int(break_date[2])

    # //////////CALCULATE OUR START DATE WITH DATETIME FUNC
    start_date = datetime.date(year, month, day) - datetime.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).\
         filter(Measurement.date >= str(start_date), Measurement.date < end_date[0][0]).all()

    session.close()
    #//////////// Convert list of tuples into normal list
    all_results = list(  np.ravel( results )  )
    return jsonify(all_results)

'============================================================================================='
# /// TRIED TO REFACTOR AND HAVE ALL LISTST COMPILED HERE - DID NOT WORK ? - SAD :(
# def calc_stuff(list_vals ):

#     all_results = []

#     for i in list_vals:
#         temps_dic = {}
#         temps_dic["1_Minimum Temp"] = i[0]
#         temps_dic["2_Average Temp"] = round( (i[1]),2) # can also do  = station, name
#         temps_dic["3_Maximum Temp"] = i[2]
#         all_results.append(temps_dic)

#     return jsonify(all_results)


'============================================================================================='
'''                          TEMP STATS FOR START DATE AND GREATER

# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.  
#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.  
#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.'''

@app.route("/api/v1.0/<key_check>")
def date_temps(key_check):
    #////////////// Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all"""
    #///////////// Query Conditions
    calc_state = 0
    all_results = []
    import datetime
    date_string = key_check
    date_format = '%Y-%m-%d'

    try:
        #////////// CHECK IF OUR DATE IS VALID 
        key_a = datetime.datetime.strptime(date_string, date_format)
        calc_state = 1

    except ValueError:
         return f"Incorrect data format, Enter date like this,  YYYY-MM-DD  so I can display your values "

        #////////////// PERFORM QUERY
    if calc_state == 1 :
        sel =   [ 
                func.min(Measurement.tobs), 
                func.avg(Measurement.tobs),
                func.max(Measurement.tobs)
                ] 
        results = session.query(*sel).\
        filter(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= str(key_a)).all()
        #/////////// JSON APPEARS TO ALPHA NUMERIC SORT DICTIONARY RESULTS TO FORCE ORDER NUMBER LIKE BELOW

        #calc_stuff(results)
        #//////////////PLACE IN A NICE DICTIONARY AND OUTPUT 
        for i in results:
            temps_dic = {}
            temps_dic["1_Minimum Temp"] = i[0]
            temps_dic["2_Average Temp"] = round( (i[1]),2) # can also do  = station, name
            temps_dic["3_Maximum Temp"] = i[2]
            all_results.append(temps_dic)

    session.close()
    return jsonify(all_results)





'============================================================================================='
'                         TEMP STATS FOR START DATE AND END DATES         '


@app.route("/api/v1.0/<key_check1>/<key_check2>")
def date_range_temps(key_check1 , key_check2):
    #////////////// Create our session (link) from Python to the DB
    session = Session(engine)
    #///////////// Query Conditions
    import datetime
    calc_state = 0
    all_results = []

    date_string  = key_check1
    date_string2 = key_check2
    date_format = '%Y-%m-%d'

    if calc_state == 0 :
        try:
            # CHECK IF OUR DATE IS VALID 
            key_a = datetime.datetime.strptime(date_string, date_format)
            calc_state = 1
            # print(date_obj)
        except ValueError:
            return f"Incorrect data format, Enter [YOUR FIRST DATE] like this:    YYYY-MM-DD  so I can display your requested values"

    if calc_state == 1 :
        try:
            # CHECK IF OUR DATE IS VALID 
            key_b = datetime.datetime.strptime(date_string2, date_format)
            calc_state = 2

        except ValueError:
            return f"Incorrect data format, Enter [YOU SECOND DATE] like this:  YYYY-MM-DD  so I can display your requested values" 

    #if key_a and key_b :
    if calc_state == 2 :
        sel =   [ 
                func.min(Measurement.tobs), 
                func.avg(Measurement.tobs),
                func.max(Measurement.tobs)
                ] 
        results = session.query(*sel).\
        filter(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= str(key_a), Measurement.date < str(key_b)).all()

        #   JSON APPEARS TO ALPHA NUMERIC SORT DICTIONARY RESULTS TO FORCE ORDER NUMBER LIKE BELOW
 
        for i in results:
            temps_dic = {}
            temps_dic["1_Minimum Temp"] = i[0]
            temps_dic["2_Average Temp"] = round( (i[1]),2) # can also do  = station, name
            temps_dic["3_Maximum Temp"] = i[2]
            all_results.append(temps_dic)

        session.close()
        return jsonify(all_results)




if __name__ == "__main__":
    app.run(debug=True)





# @app.route("/api/v1.0/justice-league/real_name/<real_name>")
# def justice_league_by_real_name(real_name):
#     """Fetch the Justice League character whose real_name matches
#        the path variable supplied by the user, or a 404 if not."""

#     canonicalized = real_name.replace(" ", "").lower()
#     for character in justice_league_members:
#         search_term = character["real_name"].replace(" ", "").lower()

#         if search_term == canonicalized:
#             return jsonify(character)

#     return jsonify({"error": f"Character with real_name {real_name} not found."}), 404


