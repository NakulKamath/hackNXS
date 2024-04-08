from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

def process_data(pocket_money, education_level, age, gender):
  
    return {
        'pocket_money': pocket_money,
        'education_level': education_level,
        'age': age,
        'gender': gender
    }

@app.route('/process_data', methods=['POST'])
def receive_data():
    data = request.json
    print("Received data:", data)  # Print received data for debugging
    pocket_money = data.get('pocketMoney')
    education_level = data.get('educationLevel')
    age = data.get('age')
    gender = data.get('gender')

    # Pass the received data through the processing function
    processed_data = process_data(pocket_money, education_level, age, gender)

    # Return the processed data as JSON response
    return data

if __name__ == '_main_':
    app.run(debug=True)