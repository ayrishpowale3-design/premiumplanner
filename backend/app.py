from flask import Flask, send_from_directory, request, jsonify
import sqlite3
import os
import pandas as pd

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
        (fullname, email, mobile, password)
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
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return jsonify({"success": True})

    return jsonify({"success": False})


if __name__ == "__main__":
    app.run(debug=True)