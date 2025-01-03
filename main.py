from flask import Flask, request, jsonify
from flask_cors import CORS

from llm.analysis import RecipeModel
from utils.parser import parse_query

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})


# A POST endpoint that accepts JSON data
@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.get_json()  # Get the JSON data sent in the request body
    if data is None:
        return jsonify({'error': 'No JSON data provided'}), 400
    query = data['query']
    try:
        dish = parse_query(query)
        recipeModel = RecipeModel(dish)
        response = recipeModel.ask_query(query)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
