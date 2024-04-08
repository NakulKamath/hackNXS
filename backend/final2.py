import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
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

target_variables = ['Student_Accommodation', 'Utilities', 'Grocery_shopping',
                    'Takeaways/dining', 'Public Transportation', 'Vehicle Maintenance',
                    'Tuition Fees', 'Books_and_Supplies', 'Online_Courses/Subscriptions',
                    'Clothing', 'Entertainment', 'Health/Medical Expenses', 'Memberships',
                    'Mobile/broadband_Bills']

steps = [('imputer', SimpleImputer(strategy='mean')), ('model', RandomForestRegressor())]
pipeline = Pipeline(steps=steps)

def train_model(target):
    X_train, X_test, y_train, y_test = train_test_split(data_with_imputation, data[target], test_size=0.2)
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    return model

models = {}
for target in target_variables:
    X_train, X_test, y_train, y_test = train_test_split(data_with_imputation, data[target], test_size=0.2)
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    models[target] = model

print("----")
print("NEW DATA:")

new_data_categorical = pd.DataFrame([['Male', 'Graduate']], columns=categorical_features)
new_encoded_data = pd.DataFrame(encoder.transform(new_data_categorical))

new_data_numerical = pd.DataFrame([[20, 1000]],
                                  columns=numerical_features)

new_data = pd.concat([new_data_numerical, new_encoded_data], axis=1)
new_data.columns = new_data.columns.astype(str)

predicted_expenses = {}
for target, model in models.items():
    predicted_expenses[target] = model.predict(new_data)[0]
print("Predicted Expenses:")
for expense, amount in predicted_expenses.items():
    print(f"{expense}: ${amount:.2f}")