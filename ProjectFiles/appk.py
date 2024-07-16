from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the model
model = pickle.load(open('randoms.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        # Get form data
        step = float(request.form['step'])
        ty = float(request.form['type'])
        amount = float(request.form['amount'])
        oldbalanceorg = float(request.form['oldbalanceorg'])
        newbalanceorig = float(request.form['newbalanceorig'])
        oldbalancedest = float(request.form['oldbalancedest'])
        newbalancedest = float(request.form['newbalancedest'])

        # Create feature array
        features = np.array([[step, ty, amount, oldbalanceorg, newbalanceorig, oldbalancedest, newbalancedest]])

        # Predict
        prediction = model.predict(features)

        # Map prediction to result
        result = 'Fraud' if prediction[0] == 1 else 'Not Fraud'

        return render_template('result.html', prediction_text=result)
    return render_template('predict.html')

@app.route('/submit')
def submit():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=False)
