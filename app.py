from flask import Flask, request, jsonify
import os
from hello import add

app = Flask(__name__)

@app.route('/add', methods=['GET'])
def add_endpoint():
    """API endpoint for add function"""
    x = request.args.get('x', type=float)
    y = request.args.get('y', type=float)
    
    if x is None or y is None:
        return jsonify({'error': 'Missing parameters x and y'}), 400
    
    result = add(x, y)
    return jsonify({'x': x, 'y': y, 'result': result})

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
