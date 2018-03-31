from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
from config import password

# flask setup
app = Flask(__name__)
# database setup
Base = automap_base()

engine = create_engine(f"postgresql+psycopg2://akufoy:{password}@rds-postgresql-bon-temps.capxvife87l2.us-east-2.rds.amazonaws.com/bon_temps")
Base.prepare(engine, reflect=True)
bon_temps = Base.classes.bon_temps

session = Session(engine)

# template rendering
@app.route("/")
def home():
    return render_template("index.html")

# route - leaflet
@app.route("/api/leaflet_data")
def leaflet_data():
    results = session.query(bon_temps.venues, bon_temps.address, bon_temps.lat, bon_temps.lon).all()
    # massage into json
    bon_temps_data = {"results": []}
    for result in results:
        bon_temps_data["results"].append({
        "venue": result[0],
        "address": result[1],
        "lat": result[2],
        "lon": result[3]
        })

    return jsonify(bon_temps_data)

if __name__ == "__main__":
    app.run(debug=True)