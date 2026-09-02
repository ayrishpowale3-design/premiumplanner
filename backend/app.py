from flask import Flask, send_from_directory, request, jsonify
import sqlite3
import os
import pandas as pd
import random
import urllib.parse
import urllib.request
import json

app = Flask(__name__)

FRONTEND_FOLDER = os.path.join(os.path.dirname(__file__), "../frontend")

DATABASE = "travelplanner.db"
# ---------------- DATASETS ----------------

DATASET_FOLDER = os.path.join(os.path.dirname(__file__), "datasets")

HOTEL_FILE = os.path.join(DATASET_FOLDER, "google_hotel_data_clean_v2.csv")
PLACE_FILE = os.path.join(DATASET_FOLDER, "Top Indian Places to Visit.csv")

try:
    hotels_df = pd.read_csv(HOTEL_FILE)
    places_df = pd.read_csv(PLACE_FILE)

    print("Datasets Loaded Successfully")
    print("Hotels:", len(hotels_df))
    print("Places:", len(places_df))

except Exception as e:
    print("Dataset Loading Error:", e)

# ---------------- DATABASE ----------------


def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        email TEXT UNIQUE,
        mobile TEXT,
        password TEXT
    )
    """)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS trip_history(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    source TEXT,

    destination TEXT,

    start_date TEXT,

    end_date TEXT,

    budget INTEGER,

    travellers INTEGER,

    interest TEXT,

    transport TEXT,

    hotel TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")
    conn.commit()
    conn.close()


create_database()


# ---------------- PAGES ----------------


@app.route("/")
def index():
    return send_from_directory(FRONTEND_FOLDER, "index.html")


@app.route("/login.html")
def login_page():
    return send_from_directory(FRONTEND_FOLDER, "login.html")


@app.route("/register.html")
def register_page():
    return send_from_directory(FRONTEND_FOLDER, "register.html")


@app.route("/home.html")
def home_page():
    return send_from_directory(FRONTEND_FOLDER, "home.html")


# ======== NEW ROUTE ========


@app.route("/plantrip.html")
def plantrip_page():
    return send_from_directory(FRONTEND_FOLDER, "plantrip.html")


# ===========================


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_FOLDER, path)

def ensure_favorite_column():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "ALTER TABLE trip_history ADD COLUMN is_favorite INTEGER DEFAULT 0"
        )
    except sqlite3.OperationalError:
        # Column already exists
        pass

    conn.commit()
    conn.close()
# ---------------- REGISTER API ----------------


@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    fullname = data["fullname"]
    email = data["email"]
    mobile = data["mobile"]
    password = data["password"]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=?", (email,))

    user = cursor.fetchone()

    if user:
        conn.close()
        return jsonify({"success": False, "message": "Email already exists"})

    cursor.execute(
        "INSERT INTO users(fullname,email,mobile,password) VALUES(?,?,?,?)",
        (fullname, email, mobile, password),
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})


# ---------------- LOGIN API ----------------


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data["email"]
    password = data["password"]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?", (email, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return jsonify({"success": True})

    return jsonify({"success": False})

@app.route("/generate-trip", methods=["POST"])
def generate_trip():

    data = request.get_json()

    source = data["source"]
    print(data)
    destination = data["destination"]

    start_date = data["startDate"]
    end_date = data["endDate"]

    budget = data["budget"]

    travellers = data["travellers"]

    interest = data["interest"]

    transport = data["transport"]

    hotel = data["hotel"]

    city_hotels = hotels_df[
        hotels_df["City"].str.lower() == destination.lower()
    ]

    city_places = places_df[
        places_df["City"].str.lower() == destination.lower()
    ]

    if city_hotels.empty:
        city_hotels = hotels_df

    if city_places.empty:
        city_places = places_df

    hotels = city_hotels.sample(
        min(3, len(city_hotels))
    )["Hotel_Name"].tolist()

    places = city_places.sample(
        min(4, len(city_places))
    )["Name"].tolist()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO trip_history
        (source, destination, start_date, end_date, budget,
         travellers, interest, transport, hotel)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        source,
        destination,
        start_date,
        end_date,
        budget,
        travellers,
        interest,
        transport,
        hotel
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "hotels": hotels,
        "places": places,
        "budget": random.randint(8000, 30000)
    })
    # ---------------- AI ITINERARY ----------------

@app.route("/ai-itinerary", methods=["POST"])
def ai_itinerary():

    data = request.get_json()

    destination = data["destination"]
    start_date = data["startDate"]
    end_date = data["endDate"]
    interest = data["interest"]
    travellers = int(data["travellers"])
    budget = int(data["budget"])

    # Get places for destination
    city_places = places_df[
        places_df["City"].str.lower() == destination.lower()
    ]

    # If destination is not found, use complete dataset
    if city_places.empty:
        city_places = places_df

    # Select maximum 8 places
    places = city_places.sample(
        min(8, len(city_places))
    )["Name"].tolist()

    # Create itinerary
    itinerary = []

    for i, place in enumerate(places):
        day = (i // 2) + 1

        if len(itinerary) < day:
            itinerary.append({
                "day": day,
                "morning": "",
                "evening": ""
            })

        if itinerary[day - 1]["morning"] == "":
            itinerary[day - 1]["morning"] = place
        else:
            itinerary[day - 1]["evening"] = place

    return jsonify({
        "success": True,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "interest": interest,
        "travellers": travellers,
        "budget": budget,
        "itinerary": itinerary
    })
@app.route("/trip-history")
def trip_history():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, source, destination, start_date, end_date,
               budget, travellers, interest, transport, hotel,
               created_at, is_favorite
        FROM trip_history
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    trips = []

    for row in rows:
      trips.append({
        "id": row[0],
        "source": row[1],
        "destination": row[2],
        "start_date": row[3],
        "end_date": row[4],
        "budget": row[5],
        "travellers": row[6],
        "interest": row[7],
        "transport": row[8],
        "hotel": row[9],
        "created_at": row[10],
        "is_favorite": row[11]
    })
    return jsonify(trips)
@app.route("/favorite-trip/<int:trip_id>", methods=["POST"])
def favorite_trip(trip_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE trip_history
        SET is_favorite = CASE
            WHEN is_favorite = 1 THEN 0
            ELSE 1
        END
        WHERE id = ?
        """,
        (trip_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})
@app.route("/delete-trip/<int:trip_id>", methods=["DELETE"])
def delete_trip(trip_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM trip_history WHERE id = ?",
        (trip_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})
ensure_favorite_column()


# ==================== WEATHER API ====================

import urllib.parse
import urllib.request
import json


@app.route("/api/weather")
def get_weather():

    city = request.args.get("city", "").strip()

    if not city:
        return jsonify({
            "error": "Please enter a city"
        }), 400

    try:
        # Open-Meteo Geocoding API
        geo_url = (
            "https://geocoding-api.open-meteo.com/v1/search?"
            + urllib.parse.urlencode({
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            })
        )

        with urllib.request.urlopen(geo_url, timeout=10) as response:
            geo_data = json.loads(response.read().decode("utf-8"))

        if not geo_data.get("results"):
            return jsonify({
                "error": "City not found"
            }), 404

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        weather_url = (
            "https://api.open-meteo.com/v1/forecast?"
            + urllib.parse.urlencode({
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "is_day,"
                    "precipitation,"
                    "weather_code,"
                    "wind_speed_10m"
                ),
                "daily": (
                    "weather_code,"
                    "temperature_2m_max,"
                    "temperature_2m_min,"
                    "precipitation_probability_max"
                ),
                "timezone": "auto",
                "forecast_days": 7
            })
        )

        with urllib.request.urlopen(weather_url, timeout=10) as response:
            weather_data = json.loads(
                response.read().decode("utf-8")
            )

        current = weather_data.get("current", {})
        daily = weather_data.get("daily", {})

        return jsonify({
            "success": True,

            "location": {
                "city": location.get("name"),
                "country": location.get("country"),
                "latitude": latitude,
                "longitude": longitude
            },

            "current": {
                "temperature": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "feels_like": current.get("apparent_temperature"),
                "wind_speed": current.get("wind_speed_10m"),
                "precipitation": current.get("precipitation"),
                "weather_code": current.get("weather_code"),
                "is_day": current.get("is_day")
            },

            "forecast": {
                "dates": daily.get("time", []),
                "weather_code": daily.get("weather_code", []),
                "max_temperature": daily.get(
                    "temperature_2m_max", []
                ),
                "min_temperature": daily.get(
                    "temperature_2m_min", []
                ),
                "rain_probability": daily.get(
                    "precipitation_probability_max", []
                )
            }
        })

    except Exception as e:

        print("Weather Error:", e)

        return jsonify({
            "error": "Unable to get weather right now"
        }), 500


# ==================== START FLASK SERVER ====================

if __name__ == "__main__":
    app.run(debug=True)