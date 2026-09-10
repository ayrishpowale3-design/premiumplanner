from flask import Flask, send_from_directory, request, jsonify
import sqlite3
import os
import pandas as pd
import urllib.parse
import urllib.request
import json

app = Flask(__name__)

# ============================================================
# FRONTEND
# ============================================================

FRONTEND_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "../frontend"
)

# ============================================================
# DATABASE
# ============================================================

DATABASE = "travelplanner.db"


# ============================================================
# DATASETS
# ============================================================

DATASET_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "datasets"
)

HOTEL_FILE = os.path.join(
    DATASET_FOLDER,
    "google_hotel_data_clean_v2.csv"
)

PLACE_FILE = os.path.join(
    DATASET_FOLDER,
    "Top Indian Places to Visit.csv"
)

try:
    hotels_df = pd.read_csv(HOTEL_FILE)
    places_df = pd.read_csv(PLACE_FILE)

    print("Datasets Loaded Successfully")
    print("Hotels:", len(hotels_df))
    print("Places:", len(places_df))

except Exception as e:
    print("Dataset Loading Error:", e)

    hotels_df = pd.DataFrame()
    places_df = pd.DataFrame()


# ============================================================
# DATABASE CREATION
# ============================================================

def create_database():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # ---------------- USERS TABLE ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT,
            email TEXT UNIQUE,
            mobile TEXT,
            password TEXT
        )
    """)

    # ---------------- TRIP HISTORY TABLE ----------------

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


# ============================================================
# FAVORITE COLUMN
# ============================================================

def ensure_favorite_column():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:

        cursor.execute(
            "ALTER TABLE trip_history "
            "ADD COLUMN is_favorite INTEGER DEFAULT 0"
        )

    except sqlite3.OperationalError:
        # Column already exists
        pass

    conn.commit()
    conn.close()


ensure_favorite_column()


# ============================================================
# PAGE ROUTES
# ============================================================

@app.route("/")
def index():

    return send_from_directory(
        FRONTEND_FOLDER,
        "index.html"
    )


@app.route("/login.html")
def login_page():

    return send_from_directory(
        FRONTEND_FOLDER,
        "login.html"
    )


@app.route("/register.html")
def register_page():

    return send_from_directory(
        FRONTEND_FOLDER,
        "register.html"
    )


@app.route("/home.html")
def home_page():

    return send_from_directory(
        FRONTEND_FOLDER,
        "home.html"
    )


@app.route("/plantrip.html")
def plantrip_page():

    return send_from_directory(
        FRONTEND_FOLDER,
        "plantrip.html"
    )


# ============================================================
# SERVE OTHER FRONTEND FILES
# ============================================================

@app.route("/<path:path>")
def static_files(path):

    return send_from_directory(
        FRONTEND_FOLDER,
        path
    )


# ============================================================
# REGISTER API
# ============================================================

@app.route("/register", methods=["POST"])
def register():

    try:

        data = request.get_json()

        fullname = data["fullname"]
        email = data["email"]
        mobile = data["mobile"]
        password = data["password"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Check whether email already exists

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        if user:

            conn.close()

            return jsonify({
                "success": False,
                "message": "Email already exists"
            })

        # Insert new user

        cursor.execute(
            """
            INSERT INTO users
            (fullname, email, mobile, password)
            VALUES (?, ?, ?, ?)
            """,
            (
                fullname,
                email,
                mobile,
                password
            )
        )

        conn.commit()
        conn.close()

        return jsonify({
            "success": True
        })

    except Exception as e:

        print("Register Error:", e)

        return jsonify({
            "success": False,
            "message": "Registration failed"
        }), 500


# ============================================================
# LOGIN API
# ============================================================

@app.route("/login", methods=["POST"])
def login():

    try:

        data = request.get_json()

        email = data["email"]
        password = data["password"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email=? AND password=?
            """,
            (
                email,
                password
            )
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            return jsonify({
                "success": True
            })

        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        })

    except Exception as e:

        print("Login Error:", e)

        return jsonify({
            "success": False,
            "message": "Login failed"
        }), 500


# ============================================================
# GENERATE TRIP API
# ============================================================

@app.route("/generate-trip", methods=["POST"])
def generate_trip():

    try:

        data = request.get_json() or {}

        source = str(data.get("source", "")).strip()
        destination = str(data.get("destination", "")).strip()

        start_date = str(data.get("startDate", "")).strip()
        end_date = str(data.get("endDate", "")).strip()

        # ====================================================
        # SAFELY CONVERT BUDGET
        # ====================================================

        budget_value = data.get("budget", 0)

        if isinstance(budget_value, str):
            # Accept values such as 40000, 40,000, ₹40,000
            budget_value = budget_value.replace(",", "")
            budget_value = budget_value.replace("₹", "")
            budget_value = budget_value.strip()

        budget = int(float(budget_value))

        # ====================================================
        # SAFELY CONVERT TRAVELLERS
        # ====================================================

        travellers_value = data.get("travellers", 1)

        if isinstance(travellers_value, str):
            import re
            match = re.search(r"\d+", travellers_value)

            if match:
                travellers_value = match.group()
            else:
                travellers_value = 1

        travellers = int(travellers_value)

        interest = str(data.get("interest", "")).strip()
        transport = str(data.get("transport", "")).strip()
        hotel = str(data.get("hotel", "")).strip()

        print("Trip Request:")
        print(data)
        print("Processed Budget:", budget)
        print("Processed Travellers:", travellers)

        # ====================================================
        # FIND HOTELS
        # ====================================================

        if not hotels_df.empty:

            city_hotels = hotels_df[
                hotels_df["City"]
                .astype(str)
                .str.lower()
                == destination.lower()
            ]

        else:

            city_hotels = pd.DataFrame()

        if city_hotels.empty and not hotels_df.empty:
            city_hotels = hotels_df

        if not city_hotels.empty:

            hotels = city_hotels.sample(
                min(3, len(city_hotels))
            )["Hotel_Name"].tolist()

        else:

            hotels = []

        # ====================================================
        # FIND TOURIST PLACES
        # ====================================================

        if not places_df.empty:

            city_places = places_df[
                places_df["City"]
                .astype(str)
                .str.lower()
                == destination.lower()
            ]

        else:

            city_places = pd.DataFrame()

        if city_places.empty and not places_df.empty:
            city_places = places_df

        if not city_places.empty:

            places = city_places.sample(
                min(4, len(city_places))
            )["Name"].tolist()

        else:

            places = []

        # ====================================================
        # SAVE TRIP TO DATABASE
        # ====================================================

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO trip_history
            (
                source,
                destination,
                start_date,
                end_date,
                budget,
                travellers,
                interest,
                transport,
                hotel
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                source,
                destination,
                start_date,
                end_date,
                budget,
                travellers,
                interest,
                transport,
                hotel
            )
        )

        conn.commit()
        conn.close()

        # ====================================================
        # RETURN TRIP DATA
        # ====================================================

        return jsonify({

            "success": True,
            "source": source,
            "destination": destination,
            "startDate": start_date,
            "endDate": end_date,
            "travellers": travellers,
            "interest": interest,
            "transport": transport,
            "hotel": hotel,
            "hotels": hotels,
            "places": places,

            # Use the actual budget entered by the user
            "budget": budget

        })

    except Exception as e:

        print("Generate Trip Error:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ============================================================
# AI ITINERARY API
# ============================================================

@app.route("/ai-itinerary", methods=["POST"])
def ai_itinerary():

    try:

        data = request.get_json() or {}

        destination = str(data.get("destination", "")).strip()
        start_date = str(data.get("startDate", "")).strip()
        end_date = str(data.get("endDate", "")).strip()
        interest = str(data.get("interest", "")).strip()

        # ====================================================
        # SAFELY CONVERT TRAVELLERS
        # ====================================================

        travellers_value = data.get("travellers", 1)

        if isinstance(travellers_value, str):
            import re
            match = re.search(r"\d+", travellers_value)

            if match:
                travellers_value = match.group()
            else:
                travellers_value = 1

        travellers = int(travellers_value)

        # ====================================================
        # SAFELY CONVERT BUDGET
        # ====================================================

        budget_value = data.get("budget", 0)

        if isinstance(budget_value, str):
            budget_value = budget_value.replace(",", "")
            budget_value = budget_value.replace("₹", "")
            budget_value = budget_value.strip()

        budget = int(float(budget_value))

        print("AI Itinerary Request:")
        print(data)
        print("Processed Budget:", budget)
        print("Processed Travellers:", travellers)

        # ====================================================
        # GET PLACES FOR DESTINATION
        # ====================================================

        if not places_df.empty:

            city_places = places_df[
                places_df["City"]
                .astype(str)
                .str.lower()
                == destination.lower()
            ]

        else:

            city_places = pd.DataFrame()

        if city_places.empty and not places_df.empty:
            city_places = places_df

        # ====================================================
        # SELECT PLACES
        # ====================================================

        if not city_places.empty:

            places = city_places.sample(
                min(8, len(city_places))
            )["Name"].tolist()

        else:

            places = []

        # ====================================================
        # CREATE DAY-WISE ITINERARY
        # ====================================================

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

        # ====================================================
        # RETURN ITINERARY
        # ====================================================

        return jsonify({

            "success": True,
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
            "interest": interest,
            "travellers": travellers,

            # Use user's entered budget
            "budget": budget,

            "itinerary": itinerary

        })

    except Exception as e:

        print("AI Itinerary Error:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ============================================================
# TRIP HISTORY API
# ============================================================

@app.route("/trip-history")
def trip_history():

    try:

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                source,
                destination,
                start_date,
                end_date,
                budget,
                travellers,
                interest,
                transport,
                hotel,
                created_at,
                is_favorite
            FROM trip_history
            ORDER BY created_at DESC
            """
        )

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

    except Exception as e:

        print("Trip History Error:", e)

        return jsonify({
            "success": False,
            "message": "Unable to load trip history"
        }), 500


# ============================================================
# FAVORITE TRIP API
# ============================================================

@app.route(
    "/favorite-trip/<int:trip_id>",
    methods=["POST"]
)
def favorite_trip(trip_id):

    try:

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE trip_history
            SET is_favorite =
                CASE
                    WHEN is_favorite = 1 THEN 0
                    ELSE 1
                END
            WHERE id = ?
            """,
            (trip_id,)
        )

        conn.commit()
        conn.close()

        return jsonify({
            "success": True
        })

    except Exception as e:

        print("Favorite Trip Error:", e)

        return jsonify({
            "success": False
        }), 500


# ============================================================
# DELETE TRIP API
# ============================================================

@app.route(
    "/delete-trip/<int:trip_id>",
    methods=["DELETE"]
)
def delete_trip(trip_id):

    try:

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM trip_history
            WHERE id = ?
            """,
            (trip_id,)
        )

        conn.commit()
        conn.close()

        return jsonify({
            "success": True
        })

    except Exception as e:

        print("Delete Trip Error:", e)

        return jsonify({
            "success": False
        }), 500


# ============================================================
# WEATHER API
# ============================================================

@app.route("/api/weather")
def get_weather():

    city = request.args.get(
        "city",
        ""
    ).strip()

    if not city:

        return jsonify({
            "error": "Please enter a city"
        }), 400


    try:

        # ====================================================
        # OPEN-METEO GEOCODING API
        # ====================================================

        geo_url = (
            "https://geocoding-api.open-meteo.com/v1/search?"
            + urllib.parse.urlencode({
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            })
        )


        with urllib.request.urlopen(
            geo_url,
            timeout=10
        ) as response:

            geo_data = json.loads(
                response.read().decode("utf-8")
            )


        # City not found

        if not geo_data.get("results"):

            return jsonify({
                "error": "City not found"
            }), 404


        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]


        # ====================================================
        # OPEN-METEO WEATHER API
        # ====================================================

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


        with urllib.request.urlopen(
            weather_url,
            timeout=10
        ) as response:

            weather_data = json.loads(
                response.read().decode("utf-8")
            )


        current = weather_data.get(
            "current",
            {}
        )

        daily = weather_data.get(
            "daily",
            {}
        )


        # ====================================================
        # RETURN WEATHER DATA
        # ====================================================

        return jsonify({

            "success": True,

            "location": {

                "city": location.get("name"),

                "country": location.get("country"),

                "latitude": latitude,

                "longitude": longitude

            },

            "current": {

                "temperature":
                    current.get(
                        "temperature_2m"
                    ),

                "humidity":
                    current.get(
                        "relative_humidity_2m"
                    ),

                "feels_like":
                    current.get(
                        "apparent_temperature"
                    ),

                "wind_speed":
                    current.get(
                        "wind_speed_10m"
                    ),

                "precipitation":
                    current.get(
                        "precipitation"
                    ),

                "weather_code":
                    current.get(
                        "weather_code"
                    ),

                "is_day":
                    current.get(
                        "is_day"
                    )

            },

            "forecast": {

                "dates":
                    daily.get(
                        "time",
                        []
                    ),

                "weather_code":
                    daily.get(
                        "weather_code",
                        []
                    ),

                "max_temperature":
                    daily.get(
                        "temperature_2m_max",
                        []
                    ),

                "min_temperature":
                    daily.get(
                        "temperature_2m_min",
                        []
                    ),

                "rain_probability":
                    daily.get(
                        "precipitation_probability_max",
                        []
                    )

            }

        })


    except Exception as e:

        print("Weather Error:", e)

        return jsonify({
            "error": "Unable to get weather right now"
        }), 500


# ============================================================
# ATTRACTIONS API
# ============================================================

@app.route("/api/attractions")
def get_attractions():

    city = request.args.get(
        "city",
        ""
    ).strip()

    if not city:

        return jsonify({
            "success": False,
            "error": "Please enter a city"
        }), 400


    try:

        # ====================================================
        # FIND ATTRACTIONS
        # ====================================================

        if places_df.empty:

            city_places = pd.DataFrame()

        else:

            city_places = places_df[
                places_df["City"]
                .astype(str)
                .str.lower()
                == city.lower()
            ]


        attractions = []


        for _, place in city_places.iterrows():

            attractions.append({

                "name":
                    str(place["Name"]),

                "city":
                    str(place["City"]),

                "state":
                    str(place["State"])

            })


        return jsonify({

            "success": True,

            "city": city,

            "attractions": attractions

        })


    except Exception as e:

        print("Attractions Error:", e)

        return jsonify({

            "success": False,

            "error": "Unable to load attractions"

        }), 500


# ============================================================
# HOTELS API
# ============================================================

@app.route("/api/hotels")
def get_hotels():

    city = request.args.get(
        "city",
        ""
    ).strip()

    if not city:

        return jsonify({

            "success": False,

            "error": "Please enter a city"

        }), 400


    try:

        # ====================================================
        # FIND HOTELS
        # ====================================================

        if hotels_df.empty:

            city_hotels = pd.DataFrame()

        else:

            city_hotels = hotels_df[
                hotels_df["City"]
                .astype(str)
                .str.lower()
                == city.lower()
            ]


        hotels = []


        for _, hotel in city_hotels.iterrows():

            hotels.append({

                "name":
                    str(hotel["Hotel_Name"]),

                "city":
                    str(hotel["City"])

            })


        return jsonify({

            "success": True,

            "city": city,

            "hotels": hotels

        })


    except Exception as e:

        print("Hotels Error:", e)

        return jsonify({

            "success": False,

            "error": "Unable to load hotels"

        }), 500


# ============================================================
# TRANSPORT API
# ============================================================

@app.route("/api/transport")
def get_transport():

    source = request.args.get(
        "source",
        ""
    ).strip()

    destination = request.args.get(
        "destination",
        ""
    ).strip()


    if not destination:

        return jsonify({

            "success": False,

            "error": "Please enter destination city"

        }), 400


    # ========================================================
    # TRANSPORT OPTIONS
    # ========================================================

    transport = [

        {
            "type": "Bus",

            "icon": "🚌",

            "description":
                f"Bus services are available from "
                f"{source or 'your city'} to "
                f"{destination}."
        },

        {
            "type": "Train",

            "icon": "🚆",

            "description":
                f"Train services are available between "
                f"{source or 'your city'} and "
                f"{destination}."
        },

        {
            "type": "Flight",

            "icon": "✈️",

            "description":
                f"Flights may be available from "
                f"{source or 'your city'} to "
                f"{destination}."
        },

        {
            "type": "Taxi / Cab",

            "icon": "🚕",

            "description":
                f"Taxi and cab services are available "
                f"for travel to {destination}."
        }

    ]


    return jsonify({

        "success": True,

        "source": source,

        "destination": destination,

        "transport": transport

    })


# ============================================================
# START FLASK SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
    