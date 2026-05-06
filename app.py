from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# LOAD MODEL + ENCODERS
model = joblib.load("model.pkl")
le_cloud = joblib.load("le_cloud.pkl")
le_season = joblib.load("le_season.pkl")
le_location = joblib.load("le_location.pkl")
le_target = joblib.load("le_target.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    try:
        # ===== GET NUMERIC VALUES =====
        temp = float(data.get('temp', 0))
        humidity = float(data.get('humidity', 0))
        wind = float(data.get('wind', 0))
        precip = float(data.get('precip', 0))
        pressure = float(data.get('pressure', 0))
        uv = float(data.get('uv', 0))
        visibility = float(data.get('visibility', 0))

        # ===== GET CATEGORICAL =====
        cloud = str(data.get('cloud', '')).strip().lower()
        season = str(data.get('season', '')).strip().title()
        location = str(data.get('location', '')).strip().lower()
        print("Received cloud:", cloud)
        print("Received season:", season)
        print("Received location:", location)

        print("Allowed cloud:", le_cloud.classes_)
        print("Allowed season:", le_season.classes_)
        print("Allowed location:", le_location.classes_)

        
        # ===== VALIDATION =====
        if cloud not in le_cloud.classes_:
            return jsonify({
                "weather_type": "ERROR",
                "confidence": 0,
                "message": f"Invalid Cloud: {cloud}"
            })

        if season not in le_season.classes_:
            return jsonify({
                "weather_type": "ERROR",
                "confidence": 0,
                "message": f"Invalid Season: {season}"
            })

        if location not in le_location.classes_:
            return jsonify({
                "weather_type": "ERROR",
                "confidence": 0,
                "message": f"Invalid Location: {location}"
            })

        # ===== ENCODE (SAFE) =====
        cloud_val = le_cloud.transform([cloud])[0]
        season_val = le_season.transform([season])[0]
        location_val = le_location.transform([location])[0]

        # ===== EXACT FEATURE ORDER =====
        features = np.array([[ 
            temp,
            humidity,
            wind,
            precip,
            cloud_val,
            pressure,
            uv,
            season_val,
            visibility,
            location_val
        ]])

        # ===== MODEL PREDICTION =====
        prediction = model.predict(features)[0]
        result = le_target.inverse_transform([prediction])[0]
        confidence = max(model.predict_proba(features)[0]) * 100

        # ===== HYBRID FIX =====
        if result == "Sunny":
            if humidity > 85 and precip > 60:
                result = "Rainy"
            elif visibility < 2:
                result = "Cloudy"
            elif temp < 0:
                result = "Snowy"

        return jsonify({
            "weather_type": result,
            "confidence": round(confidence, 2)
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "weather_type": "ERROR",
            "confidence": 0
        })

# RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)