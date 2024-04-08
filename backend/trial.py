import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
import numpy as np

data = pd.read_csv(r"C:\Users\Dr Poonam Pandey\Desktop\hackathon college\final.csv")

numerical_features = ['Age', 'Monthly_Income']
categorical_features = ['Gender', 'Level_of_Education']

data.columns = data.columns.astype(str)

encoder = OneHotEncoder(sparse=False)
encoded_data = pd.DataFrame(encoder.fit_transform(data[categorical_features]))

imputer = SimpleImputer(strategy='mean')
data_numerical = pd.DataFrame(imputer.fit_transform(data[numerical_features]))

data_with_imputation = pd.concat([data_numerical, encoded_data], axis=1)

target_variables = ['Utilities', 'Grocery_shopping',
                    'Takeaways/dining', 'Public Transportation', 'Vehicle Maintenance',
                    'Books_and_Supplies', 'Online_Courses/Subscriptions',
                    'Clothing', 'Entertainment', 'Health/Medical Expenses', 'Memberships',
                    'Mobile/broadband_Bills']

models = {}
for target in target_variables:
    X_train, X_test, y_train, y_test = train_test_split(data_with_imputation, data[target], test_size=0.2)
    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)
    models[target] = model

def predict_expenses(input_data):
    new_data_categorical = pd.DataFrame([input_data], columns=categorical_features)
    new_encoded_data = pd.DataFrame(encoder.transform(new_data_categorical))
    new_data_numerical = pd.DataFrame([input_data], columns=numerical_features)
    new_data = pd.concat([new_data_numerical, new_encoded_data], axis=1)

    predicted_expenses = {}
    for target, model in models.items():
        predicted_expenses[target] = model.predict(new_data)[0]
    return predicted_expenses

# Example input data received from the backend server
input_data = {'Gender': 'Male', 'Level_of_Education': 'Diploma', 'Age': 20, 'Monthly_Income': 700}

# Predict expenses based on the input data
predicted_expenses = predict_expenses(input_data)

# Print the predicted expenses
print("Predicted Expenses:")
for expense, amount in predicted_expenses.items():
    print(f"{expense}: ${amount:.2f}")

# Now you can send the predicted_expenses dictionary to your backend server
# using the appropriate method like HTTP POST request with the requests library.
# I can provide you with an example if needed.
