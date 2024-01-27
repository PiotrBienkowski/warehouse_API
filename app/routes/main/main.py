from app import app
from datetime import datetime
from flask import jsonify

@app.route('/status')
def index():
    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"status": "ok", "current_time": formatted_now}), 201
