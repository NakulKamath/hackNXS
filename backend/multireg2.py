import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV

def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def tune_hyperparameters(model, param_grid, X_train, y_train):
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring="neg_mean_squared_error")
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    return best_model

def build_student_spending_model(data_path, target_variables, independent_variables, model_choice=RandomForestRegressor):
    data = pd.read_csv(data_path)

    if any(col not in data.columns for col in target_variables):
        raise ValueError("Missing target variables in data!")

    data = perform_feature_engineering(data)

    X = data[independent_variables]
    y = data[target_variables]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    imputer = SimpleImputer(strategy="mean")
    X_train = imputer.fit_transform(X_train)
    X_test = imputer.transform(X_test)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)


    model = model_choice()

    param_grid = {
        "n_estimators": [100, 200, 300],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "bootstrap": [True, False]
    }
    model = tune_hyperparameters(model, param_grid, X_train, y_train)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)

    print("Mean Squared Error:", mse)
    print("R-squared:", r2)
    print("Mean Absolute Percentage Error:", mape)

    return model, mse, r2, mape

data_path = r"C:\Users\Dr Poonam Pandey\Desktop\hackathon college\hackfinal.csv"
target_variables = [
    "food",
    "transportation",
    "health_wellness",
    "technology",
    "miscellaneous"
]
independent_variables = [
    "monthly_income",
    "financial_aid",
    "tuition",
    "housing",
    "major_Biology", 
    "major_Computer Science", 
    "major_Economics", 
    "major_Engineering", 
    "major_Psychology"
]

# Call the function to build the model and evaluate its performance
model, mse, r2, mape = build_student_spending_model(data_path, target_variables, independent_variables)

# Example input for prediction
example_input = {
    "monthly_income": 5000,
    "financial_aid": 1000,
    "tuition": 2000,
    "housing": 800,
    "major_Biology": 0,
    "major_Computer Science": 1,
    "major_Economics": 0,
    "major_Engineering": 0,
    "major_Psychology": 0
}

# Reshape input to match the model's expectations (1 sample, n_features)
input_array = np.array([[example_input[feature] for feature in independent_variables]])
# Perform prediction
predicted_expenses = model.predict(input_array)
print("Predicted expenses:")
for i, expense in enumerate(target_variables):
    print(f"{expense}: {predicted_expenses[0][i]}")
