import os
from flask import Flask, jsonify, send_from_directory, request
from pymongo import MongoClient

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('Sanatan', 'index.html')


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
