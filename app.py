from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import joblib

app = Flask(__name__)

# Load the trained model
model = load_model("flight_delay_model.h5")
scaler = joblib.load("scaler.pkl")

def round_to_nearest_hundred(time):
    hours = time // 100
    minutes = time % 100
    if minutes < 30:
        rounded_time = hours * 100
    else:
        rounded_time = (hours + 1) * 100
    return rounded_time

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            year = int(data.get('year'))
            month = int(data.get('month'))
            day = int(data.get('date'))
            dep_time = int(data.get('dept_time'))
            carrier = data.get('carrier')
            origin = data.get('origin')
            destination = data.get('destination')
            temp = float(data.get('temp'))
            dewp = float(data.get('dewp'))
            humid = float(data.get('humid'))
            wind_speed = float(data.get('wind_speed'))
            visib = float(data.get('visib'))

            # Round dept_time to the nearest hundred
            rounded_dept_time = round_to_nearest_hundred(dep_time)

            # Create a DataFrame for prediction
            input_data = pd.DataFrame({
                'year': [year],
                'month': [month],
                'day': [day],
                'dep_time': [rounded_dept_time],
                'carrier': [carrier],
                'origin': [origin],
                'dest': [destination],
                'temp': [temp],
                'dewp': [dewp],
                'humid': [humid],
                'wind_speed': [wind_speed],
                'visib': [visib]
            })

            # Preprocess the input data (handle missing values and one-hot encoding)
            categorical_cols = ['carrier', 'origin', 'dest']
            input_data = pd.get_dummies(input_data, columns=categorical_cols, drop_first=True)

            # Ensure all columns from training are present
            all_columns = scaler.mean_.shape[0]
            input_data = input_data.reindex(columns=range(all_columns), fill_value=0)

            # Scale the input data
            input_scaled = scaler.transform(input_data)

            # Reshape input for LSTM
            input_scaled = input_scaled.reshape((input_scaled.shape[0], 1, input_scaled.shape[1]))

            # Make prediction
            prediction = model.predict(input_scaled)
            delay_status = "Delayed" if prediction[0][0] > 0.5 else "Not Delayed"
            probability = float(prediction[0][0])

            return jsonify(delay_status=delay_status, probability=probability)  # Return as JSON response

        except Exception as e:
            return jsonify(error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)