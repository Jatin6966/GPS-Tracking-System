from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_location = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/update-location", methods=["POST"])
def update_location():
    data = request.get_json()

    user_id = data.get("user_id")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if not user_id or latitude is None or longitude is None:
        return jsonify({"error": "Missing location data"}), 400

    latest_location[user_id] = {
        "latitude": latitude,
        "longitude": longitude
    }

    print(f"{user_id}: {latitude}, {longitude}")

    return jsonify({"status": "success"})


@app.route("/location/<user_id>")
def get_location(user_id):
    location = latest_location.get(user_id)

    if location is None:
        return jsonify({"error": "No location available"}), 404

    return jsonify(location)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
