from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/predict', methods=['POST'])
def predict():
    return jsonify({'class_id': 'prueba_id', 'winner': 'prueba'})