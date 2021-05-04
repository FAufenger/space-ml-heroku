import os
import numpy as np
from models import create_classes
import requests
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy

from sklearn.preprocessing import StandardScaler, LabelEncoder

from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from tensorflow.keras.callbacks import ModelCheckpoint
# from array import array



model = load_model("neural_network.h5")

#################################################
# Flask/ DB setup Setup
#################################################
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///space_DB.sqlite"
# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# reflect an existing database into a new model
Base = automap_base()

engine = create_engine("sqlite:///space_DB.sqlite")

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
asteroid_impacts = Base.classes.asteroid_impacts
asteroid_orbits = Base.classes.asteroid_orbits
star_classification = Base.classes.star_classification
ufo_sightings = Base.classes.ufo_sightings
X_train = Base.classes.X_train

star_decipher = Base.classes.star_decipher

db = SQLAlchemy(app)
Stardecipher = create_classes(db)

# app = Flask(__name__)


#################################################
# Routes
#################################################

#### Front End ####

@app.route("/")
@app.route("/home")
def welcome():

    return render_template("index.html")


@app.route("/asteroids")
def asteroids():
    return render_template("asteroids.html")


@app.route("/stars")
def stars():

    # y = list(lastInput.values())
    # z = np.array([[y[5], y[3], y[2], y[0], y[1], y[4]]])
     # encoded_predictions = model.predict_classes(z)

    # session = Session(engine)
    # X_train_results = session.query(X_train.Temperature, X_train.L, X_train.R,
    #                         X_train.A_M, X_train.Color, X_train.Spectral_Class).all()
    # session.close()
    
    # X_scaler = StandardScaler().fit(X_train_results)

    # x = requests.get('https://space-ml.herokuapp.com/api/v1.0/stars')
    # lastInput = x.json()[-1]

    # = list(lastInput.values())
    # z = [y[5], y[2], y[3], y[0], y[1], y[4]]
    # X_train_scaled = X_scaler.transform([z])
    # value = np.array(X_train_scaled)
    
    z = [1,2,3,4,5]
    value = np.array([z])
    
    encoded_predictions = model.predict_classes(value)
    #encoded_predictions = model.predict_classes(np.array([list(lastInput.values())]))

    if encoded_predictions == 3:
        prediction_text = 'Red Dwarf'
    elif encoded_predictions == 0:
        prediction_text = 'Brown Dwarf'
    elif encoded_predictions == 5:
        prediction_text = 'White  Dwarf'
    elif encoded_predictions == 2:
        prediction_text = 'Main Sequence'
    elif encoded_predictions == 4:
        prediction_text = 'Super Giants'
    elif encoded_predictions == 1:
        prediction_text = 'Hyper Giants'
    else:
        prediction_text == 'Oops, something went wrong.'

    return render_template("stars.html", prediction_text=prediction_text)

    #y = pd.DataFrame.from_dict(lastInput, orient='index').values
    # y = np.squeeze(pd.DataFrame.from_dict(lastInput, orient='index')[["Temperature", L, R, A]].values)
    
    #print(y)
    # print(lastInput)
    # print('------------------------------')
    # print(type(lastInput.items()))
    # print('cy below------------------------------')
    # ay= lastInput.values()
    # by = list(ay)
    # cy= np.array(by)
    # print(cy)
    # # z=list(lastInput.values())
    # # print(type(z))
    # print('------------------------------')
    # y= np.array(list(lastInput.items()))
    # print('------------------------------')
    
    # z=np.vstack(y)
    # print(type(y))
    # print('y type above------------------------------')
    # print(y)
    # #  a= np.concatenate([np.array(y[0]), np.array(y[1]), np.array(y[2]), np.array(y[3]), np.array(y[4]), np.array(y[5])], axis=0)
    # a= [y[0], y[1], y[2], y[3], y[4], y[5]]
    # print(a)
    # print('a above b below------------------------------')
    # b= np.array(a)
    # print(list(b))
    # print(b)
    # print(type(b))
    # ## Load the model
    
    #model = load_model("neural_network.h5")
    #model.fit()
    #prediction_text = label_encoder.inverse_transform(encoded_predictions)
    #print(f"Predicted classes: {encoded_predictions}")

@app.route("/ufos")
def ufos():
    return render_template("ufos.html")

    # Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():

    if request.method == "POST":
        Temperature = request.form["TemperatureValue"]
        L = request.form["LValue"]
        R = request.form["RValue"]
        A_M = request.form["AMValue"]
        Color = request.form["ColorValue"]
        Spectral_Class = request.form["SpectralClassValue"]

        starType = star_decipher(Temperature=Temperature, L=L, R=R, A_M=A_M, Color=Color, Spectral_Class=Spectral_Class)
        db.session.add(starType)
        db.session.commit()
        return redirect("/stars", code=302)

    return render_template("form.html")


#### Back End ####
@app.route("/api/v1.0/stars")
def stars2():
    # Create our session (link) from SQLite
    session = Session(engine)
    results = session.query(star_decipher.Temperature, star_decipher.L, star_decipher.R,
                            star_decipher.A_M, star_decipher.Color, star_decipher.Spectral_Class).all()
    session.close()

    return jsonify(results)



@app.route("/api/v1.0/asteroid_orbits")
def asteroid_orbital():
    session = Session(engine)
    results = session.query(asteroid_orbits.object_name, asteroid_orbits.object_classification,
        asteroid_orbits.epoch_TDB, asteroid_orbits.orbit_axis_AU, asteroid_orbits.orbit_eccentricity, 
        asteroid_orbits.orbit_inclination_deg, asteroid_orbits.perihelion_argument_deg, 
        asteroid_orbits.node_longitude_deg, asteroid_orbits.mean_anomoly_deg, asteroid_orbits.perihelion_distance_AU,
        asteroid_orbits.aphelion_distance_AU, asteroid_orbits.orbital_period_yr, 
        asteroid_orbits.minimum_orbit_intersection_distance_AU,
        asteroid_orbits.orbital_reference, asteroid_orbits.asteroid_magnitude).all()
    session.close()

    return jsonify(results)

@app.route("/api/v1.0/asteroid_impacts")
def asteroid_impacting():
    session = Session(engine)
    results = session.query(asteroid_impacts.object_name, asteroid_impacts.period_start, asteroid_impacts.period_end,
        asteroid_impacts.possible_impacts, asteroid_impacts.cumulative_impact_probability, asteroid_impacts.asteroid_velocity, asteroid_impacts.asteroid_magnitude,
        asteroid_impacts.asteroid_diameter_km, asteroid_impacts.cumulative_palermo_scale, asteroid_impacts.maximum_palermo_scale).all()
    session.close()
    return jsonify(results)

@app.route("/api/v1.0/ufos")
def ufo2():
    # Create our session (link) from SQLite
    session = Session(engine)
    results = session.query(ufo_sightings.date_occured, ufo_sightings.time_occured, ufo_sightings.city,
        ufo_sightings.state, ufo_sightings.country, ufo_sightings.shape, ufo_sightings.duration_seconds, 
        ufo_sightings.duration_hours_min, ufo_sightings.comments, ufo_sightings.date_posted, ufo_sightings.latitude, 
        ufo_sightings.longitude).all()
    session.close()

    #all_stars = list(np.ravel(results))
    
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)