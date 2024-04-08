from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Load your CSV file
data = pd.read_csv(r"./final.csv")

# Define numerical and categorical features
numerical_features = ['Age', 'Monthly_Income']
categorical_features = ['Gender', 'Level_of_Education']

# Define encoder for categorical features
encoder = OneHotEncoder(sparse=True)

# Define imputer for numerical features
imputer = SimpleImputer(strategy='mean')

# One-hot encode categorical features
encoded_data = pd.DataFrame(encoder.fit_transform(data[categorical_features]))

# Impute missing values in numerical features
data_numerical = pd.DataFrame(imputer.fit_transform(data[numerical_features]))

# Concatenate numerical and encoded categorical features
data_with_imputation = pd.concat([data_numerical, encoded_data], axis=1)

# Define target variables
target_variables = ['Utilities', 'Grocery_shopping',
                    'Takeaways/dining', 'Public Transportation', 'Vehicle Maintenance',
                    'Books_and_Supplies', 'Online_Courses/Subscriptions',
                    'Clothing', 'Entertainment', 'Health/Medical Expenses', 'Memberships',
                    'Mobile/broadband_Bills']

# Create a dictionary to store models for each target variable
models = {}
# Train a model for each target variable
for target in target_variables:
    # Initialize and fit the model
    model = GradientBoostingRegressor()
    X_train, X_test, y_train, y_test = train_test_split(data_with_imputation, data[target], test_size=0.2)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    models[target] = model

class InputData:
    def __init__(self, pocket_money, education_level, age, gender):
        self.pocket_money = pocket_money
        self.education_level = education_level
        self.age = age
        self.gender = gender

class PredictionOutput:
    def __init__(self, predicted_expenses):
        self.predicted_expenses = predicted_expenses

def process_data(input_data):
    new_data_categorical = pd.DataFrame([[input_data.gender, input_data.education_level]], columns=categorical_features)
    new_encoded_data = pd.DataFrame(encoder.transform(new_data_categorical))
    new_data_numerical = pd.DataFrame([[input_data.age, input_data.pocket_money]], columns=numerical_features)
    new_data = pd.concat([new_data_numerical, new_encoded_data], axis=1)

    # Predict expenses for each target variable using the trained models
    predicted_expenses = {}
    for target, model in models.items():
        predicted_expenses[target] = model.predict(new_data)[0]

    return predicted_expenses

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # Extract features from request data
    pocket_money = data.get('pocket_money')
    education_level = data.get('education_level')
    age = data.get('age')
    gender = data.get('gender')

    # Create InputData object
    input_data = InputData(pocket_money, education_level, age, gender)

    # Process the data and make predictions
    predicted_expenses = process_data(input_data)

    # Return the predictions as JSON response
    return jsonify(PredictionOutput(predicted_expenses).__dict__)

if __name__ == '__main__':
    app.run(debug=True)
