from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load dataset and model
df = pd.read_csv("mushrooms.csv")
model = joblib.load("mushroom_classifier.pkl")

# Store LabelEncoders for all features
label_encoders = {col: LabelEncoder().fit(df[col]) for col in df.columns}

# Create a readable name for each mushroom using key features
df["mushroom_name"] = df.apply(lambda row: f"{row['cap-shape']} {row['cap-color']} {row['gill-color']}", axis=1)
mushroom_list = df["mushroom_name"].unique().tolist()

@app.route('/')
def home():
    return render_template('index.html', mushrooms=mushroom_list)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        selected_mushroom = request.json.get("mushroom")

        if not selected_mushroom:
            return jsonify({"error": "No mushroom selected"}), 400

        # Find the matching row
        filtered_df = df[df["mushroom_name"] == selected_mushroom]

        if filtered_df.empty:
            return jsonify({"error": "Mushroom not found"}), 404

        # Drop unnecessary columns
        mushroom_data = filtered_df.iloc[0].drop(["class", "mushroom_name"])

        # Encode categorical values using LabelEncoders
        encoded_features = {col: label_encoders[col].transform([mushroom_data[col]])[0] for col in mushroom_data.index}

        # Convert to DataFrame
        input_data = pd.DataFrame([encoded_features], columns=mushroom_data.index)

        # Make prediction
        prediction = model.predict(input_data)[0]
        result = "Edible" if prediction == 1 else "Poisonous"

        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)