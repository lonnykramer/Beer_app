from sqlalchemy import func, create_engine
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import (
    Flask,
    render_template,
    redirect,
    jsonify,
    request)
from flask_sqlalchemy import SQLAlchemy
# from keras.models import load_model
# import tensorflow as tf
from sklearn import preprocessing
import numpy as np
import pickle

app = Flask(__name__)

# Database Set Up
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/beerdata2.sqlite"
db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)

# for t in Base.classes:
#     print(t)

beerdata = Base.classes.applicationdata2

# Home Route
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/engine.html")
def engine():
    return render_template("engine.html")

@app.route("/brewing.html")
def brewing():
    return render_template("brewing.html")

# this line active for heroku
# model = pickle.load(open('Beer/decision_tree_classifier_20200107.pkl', 'rb'))

# this line active for running local
model = pickle.load(open('decision_tree_classifier_20200107.pkl', 'rb'))

@app.route("/response", methods=["GET", "POST"])
def response():
    if request.method == "POST":
        abv = request.form.get("abv")
        ibu = request.form.get("ibu")
        mfeel = request.form.get("mfeel")
        color = request.form.get("color")
        if not abv and not ibu and not mfeel or not color:
            return "failure to input a response to all four categories"
        print(f"user input: {ibu}, {color}, {abv}, {mfeel}")
        modelinput = np.array([[int(ibu), int(color), int(abv), int(mfeel)]])
        response = model.predict(modelinput)
        print(f"the prediction class {response[0]}")
        modelresponse = response[0]
        print(modelresponse)
        # beerinfo(modelresponse)
        return render_template("results.html", id=modelresponse)
    return render_template("index.html")


# TODO put the route back here
@app.route("/beerinfo/<id>", methods=["GET"])
def beerinfo(id):
    print(f"beerinfo print fun {id}")
    sel = [
        beerdata.name,
        beerdata.ibu,
        beerdata.srm_category,
        beerdata.abv,
        beerdata.attenuation_level,
        beerdata.tagline,
        beerdata.food_pairing,
        beerdata.outcome
    ]
    qr = db.session.query(*sel).filter(beerdata.outcome == str(id)).all()
    print(f"we have {len(qr)} results")

    beers = []
    for result in qr:
        beer = {}
        beer['name'] = result[0]
        beer['ibu'] = result[1]
        beer['color'] = result[2]
        beer['abv'] = result[3]
        beer['attenuation_level'] = result[4]
        beer['tagline'] = result[5]
        beer['food_pairings'] = result[6]
        beers.append(beer)

    return jsonify(beers)


if __name__ == "__main__":
    app.run(debug=True)
