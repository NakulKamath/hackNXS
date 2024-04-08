sendDataToBackend(1000, 'UG', 20, 'Male');

function sendDataToBackend(pocketMoney, educationLevel, age, gender) {
    const data = {
        pocketMoney: pocketMoney,
        educationLevel: educationLevel,
        age: age,
        gender: gender
    };

    fetch('http://127.0.0.1:5000/process_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
        
    })
    .then(jsonData => {
        // Handle JSON response from backend
        console.log('Response from backend:', jsonData);
        // Process the response as needed
    })
    .catch(error => {
        // Handle error
        console.error('Error:', error);
    });
}