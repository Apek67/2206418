from flask import Flask, jsonify, request
import requests
import time
from collections import deque

app = Flask(__name__)


WINDOW_SIZE = 10


NUMBER_SOURCES = {
    "primes": "https://thirdparty.com/primes",
    "fibonacci": "https://thirdparty.com/fibonacci",
    "even": "https://thirdparty.com/even",
    "random": "https://thirdparty.com/random"
}


MOCK_DATA = {
    "primes": {"numbers": [2, 3, 5, 7, 11]},
    "fibonacci": {"numbers": [0, 1, 1, 2, 3]},
    "even": {"numbers": [2, 4, 6, 8, 10]},
    "random": {"numbers": [9, 27, 14, 6, 19]}
}


number_window = deque(maxlen=WINDOW_SIZE)

@app.route('/evaluation-service/<numberid>', methods=['GET'])
def get_numbers(numberid):
    if numberid not in NUMBER_SOURCES:
        return jsonify({"error": "Invalid number ID"}), 400

    print(f"Fetching numbers from: {NUMBER_SOURCES[numberid]}") 

    try:
      
        response = requests.get(NUMBER_SOURCES[numberid], timeout=1)
        response.raise_for_status()
        data = response.json()
        print("API Response:", data)  

      
        if not isinstance(data, dict) or "numbers" not in data or not data["numbers"]:
            raise ValueError("Invalid or empty response")

        new_numbers = list(set(data["numbers"])) 
        new_numbers = [int(num) for num in new_numbers if isinstance(num, (int, float))]

        if not new_numbers:
            raise ValueError("No valid numbers received")

    except (requests.RequestException, ValueError) as e:
        print(f"API Request Failed: {e}")  
      
        new_numbers = MOCK_DATA.get(numberid, {}).get("numbers", [])

    prev_state = list(number_window)


    for num in new_numbers:
        if num not in number_window:
            number_window.append(num)

    curr_state = list(number_window)
    avg_value = round(sum(number_window) / len(number_window), 2) if number_window else 0

    print(f"Before Update: {prev_state}")  
    print(f"After Update: {curr_state}")   

    return jsonify({
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "numbers": new_numbers,
        "avg": avg_value
    })


@app.route('/add-number', methods=['POST'])
def add_number():
    data = request.get_json()
    num = data.get("number")

    if not isinstance(num, (int, float)):
        return jsonify({"error": "Invalid number"}), 400

    prev_state = list(number_window)
    number_window.append(num)
    curr_state = list(number_window)
    avg_value = round(sum(number_window) / len(number_window), 2) if number_window else 0

    return jsonify({
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "numbers": [num],
        "avg": avg_value
    })

if __name__ == '__main__':
    app.run(port=9876, debug=True)
