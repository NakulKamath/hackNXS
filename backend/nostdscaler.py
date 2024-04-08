import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.impute import SimpleImputer 
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error
from sklearn.model_selection import GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def tune_hyperparameters(model, param_grid, X_train, y_train):
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring="neg_mean_squared_error")
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    return best_model

def build_student_spending_model(data_path, target_variables, independent_variables):
    data = pd.read_csv(data_path)
    target = data[target_variables]
    features = data[independent_variables]

    if features.isnull().sum().any() or target.isnull().sum().any():
        raise ValueError("Missing values found in the dataset. Please handle missing values before training the model.")

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    numeric_features = ['monthly_income', 'age']
    categorical_features = ['major_Biology', 'major_Computer Science', 'major_Economics', 'major_Engineering', 'major_Psychology']

    numeric_transformer = SimpleImputer(strategy='mean')

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])

    model = Pipeline(steps=[('preprocessor', preprocessor),
                            ('regressor', MultiOutputRegressor(RandomForestRegressor()))])

    param_grid = {
        'regressor__estimator__n_estimators': [100, 200, 300],
        'regressor__estimator__max_depth': [None, 10, 20],
        'regressor__estimator__min_samples_split': [2, 5, 10],
        'regressor__estimator__min_samples_leaf': [1, 2, 4],
        'regressor__estimator__bootstrap': [True, False]
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
    "age",
    "major_Biology", 
    "major_Computer Science", 
    "major_Economics", 
    "major_Engineering", 
    "major_Psychology"
]

model, mse, r2, mape = build_student_spending_model(data_path, target_variables, independent_variables)
