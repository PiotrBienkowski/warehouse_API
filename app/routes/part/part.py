from flask import request, jsonify
from app import app, mongo
from app.models.Part import Part

@app.route('/add_part', methods=['POST'])
def add_part():
    try:
        data = request.json
        Part.validate(data)
        print("Data validated, data:", data)
        new_part = Part(**data)
        print("New part created:", new_part.to_dict())
        mongo.db.parts.insert_one(new_part.to_dict())
        return jsonify({'msg': 'Part added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400