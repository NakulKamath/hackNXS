import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR  
data = pd.read_csv(r"C:\Users\Dr Poonam Pandey\Desktop\hackathon college\hackathon dataset.csv")
independent_variables= ["age","gender","year_in_school","major","monthly_income","financial_aid","tuition","housing" ,"food", "transportation" , "books_supplies", "entertainment" , "personal_care", "technology" ,	"health_wellness","miscellaneous","preferred_payment_method" ]

target_variable = ["monthly_income","financial_aid","tuition","housing" ,"food", "transportation" , "books_supplies", "entertainment" , "personal_care", "technology" ,	"health_wellness","miscellaneous"]

X = data[independent_variables]
y = data[target_variable]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = SVR()
model.fit(X_train, y_train)

