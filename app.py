from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
cors = CORS(app)

# Load the model
with open('LinearRegressionModel.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the car data
car = pd.read_csv('Cleaned_Car_data.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    companies = sorted(car['company'].unique())
    car_models = sorted(car['name'].unique())
    years = sorted(car['year'].unique(), reverse=True)
    fuel_types = car['fuel_type'].unique()

    companies.insert(0, 'Select Company')
    return render_template('index.html', companies=companies, car_models=car_models, years=years, fuel_types=fuel_types)

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    try:
        data = request.get_json()
        company = data['company']
        car_model = data['car_model']
        year = int(data['year'])
        fuel_type = data['fuel_type']
        driven = int(data['kilo_driven'])

        if not company or not car_model or not year or not fuel_type or not driven:
            return jsonify({'error': 'Please provide all the required fields!'})

        prediction = model.predict(pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
                                                data=np.array([car_model, company, year, driven, fuel_type]).reshape(1, 5)))
        prediction_value = np.round(prediction[0], 2)

        if prediction_value < 0:
            return jsonify({'error': 'The prediction result is not valid. Please check the input values.'})
        
        return jsonify({'prediction': prediction_value})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_car_models', methods=['POST'])
@cross_origin()
def get_car_models():
    try:
        data = request.get_json()
        company = data.get('company')
        
        if not company:
            return jsonify({'models': []})

        models = car[car['company'] == company]['name'].unique().tolist()
        return jsonify({'models': models})

    except Exception as e:
        return jsonify({'error': str(e), 'models': []})

if __name__ == '__main__':
    app.run(debug=True)
