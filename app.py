from flask import Flask, render_template, request
import pickle
import os
import pandas as pd

app = Flask(__name__)

# Correct path
base_dir = os.path.dirname(__file__)
model_path = os.path.join(base_dir, "models", "model.pkl")

# Load model
model = pickle.load(open(model_path, "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        location = int(request.form["location"])
        hour = int(request.form["hour"])
        day = int(request.form["day"])

        input_df = pd.DataFrame([[location, hour, day]], columns=["PULocationID", "hour", "day"])
        prediction = model.predict(input_df)

        return render_template(
            "index.html",
            prediction=f"Predicted Demand: {int(prediction[0])}"
        )

    except Exception as e:
        return render_template(
            "index.html",
            prediction="Error in input"
        )

if __name__ == "__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
