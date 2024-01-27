from app import app, mongo
from app.models.Part import Part
from app.utils.objectIdToStr import objectIdToStr
from bson import ObjectId
from flask import request, jsonify

# ----- CREATE -----
@app.route('/parts', methods=['POST'])
def add_part():
    try:
        data = request.json
        Part.validate(data, mongo)
        new_part = Part(**data)
        mongo.db.parts.insert_one(new_part.to_dict())
        return jsonify({'msg': 'Part added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ----- READ -----
@app.route('/parts', methods=['GET'])
def show_parts():
    parts = mongo.db.parts.find()
    parts_list = []
    for part in parts:
        part['_id'] = objectIdToStr(part['_id'])
        parts_list.append(part)
    return jsonify(parts_list), 200

# ----- UPDATE -----
@app.route('/parts/<id>', methods=['PUT'])
def update_part(id):
    try:
        object_id = ObjectId(id)
    except:
        return jsonify({'error': 'Invalid ObjectId'}), 400

    data = request.json
    try:
        Part.validate(data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    result = mongo.db.parts.update_one({'_id': object_id}, {"$set": data})
    if result.matched_count:
        return jsonify({'msg': 'Part updated successfully'}), 200
    else:
        return jsonify({'error': 'Part not found'}), 404
    
# ----- DELETE -----
@app.route('/parts/<id>', methods=['DELETE'])
def delete_part(id):
    try:
        object_id = ObjectId(id)
    except:
        return jsonify({'error': 'Invalid ObjectId'}), 400

    result = mongo.db.parts.delete_one({'_id': object_id})
    if result.deleted_count:
        return jsonify({'msg': 'Part deleted successfully'}), 200
    else:
        return jsonify({'error': 'Part not found'}), 404