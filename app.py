from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    analytics = [
        {"date": "2025-03-25", "likes": 120, "comments": 40},
        {"date": "2025-03-26", "likes": 200, "comments": 65},
        {"date": "2025-03-27", "likes": 300, "comments": 100},
        {"date": "2025-03-28", "likes": 250, "comments": 80},
        {"date": "2025-03-29", "likes": 400, "comments": 150},
    ]
    return jsonify({"analytics": analytics})

if __name__ == '__main__':
    app.run(debug=True)
